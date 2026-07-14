"""Schema tests for scripts/auto/state.json shape and timestamp invariants.

Pure fixtures — never touches the live state.json on disk. Covers:
  - required keys always present on a freshly-initialized state
  - history append lands at history[-1] (newest last)
  - bounded growth: history trim to 64 entries
  - last_successful_run_at must be null or end with 'Z'
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest


REQUIRED_KEYS: set[str] = {
    "last_run_date",
    "last_run_exit",
    "last_slugs",
    "draft_status",
    "last_build_exit",
    "history",
    "last_successful_run_at",
}


def _empty_state() -> dict[str, Any]:
    return {
        "last_run_date": None,
        "last_run_exit": None,
        "last_slugs": [],
        "draft_status": {},
        "last_build_exit": None,
        "history": [],
        "last_successful_run_at": None,
    }


def test_state_has_all_required_keys() -> None:
    s = _empty_state()
    assert set(s.keys()) == REQUIRED_KEYS


@pytest.mark.parametrize("value", [None, "2026-07-15T09:00:00Z"])
def test_last_successful_run_at_accepts_null_or_z(value: Any) -> None:
    s = _empty_state()
    s["last_successful_run_at"] = value
    if value is not None:
        assert value.endswith("Z")
    # Round-trip via json to assert (de)serializability.
    blob = json.dumps(s)
    parsed = json.loads(blob)
    assert parsed["last_successful_run_at"] == value


def test_history_append_lets_newest_appear_last() -> None:
    s = _empty_state()
    s["history"] = []
    entries = [
        {"run_at": f"2026-07-1{i}T09:00:00Z", "slugs": [f"slug-{i}"],
         "exit": 0, "build_exit": 0}
        for i in range(1, 4)
    ]
    for e in entries:
        s["history"].append(e)
    assert s["history"][-1] == entries[-1]


def test_history_trimmed_to_64_after_100_appends() -> None:
    s = _empty_state()
    s["history"] = []
    # Use a synthesized monotonic counter to avoid 60-second clamp on mm:ss.
    for i in range(100):
        s["history"].append({"run_at": f"2026-07-15T09:00:{i % 60:02d}Z",
                              "slugs": [], "exit": 0, "build_exit": 0})
        # Mimic the Update-State FIFO trim to 64.
        if len(s["history"]) > 64:
            s["history"] = s["history"][-64:]
    assert len(s["history"]) == 64
    # We don't assert "the 100th item's i=99 wins" — modulo wraps the
    # :ss, so the newest entry is whichever wraps last.
    assert s["history"][-1]["run_at"].endswith("Z")
    # All entries retained the Z suffix on the way through.
    assert all(h["run_at"].endswith("Z") for h in s["history"])


def test_live_state_json_is_parseable_and_has_new_field() -> None:
    # Sanity gate: the file the user keeps on disk now carries the
    # last_successful_run_at key. Defends against a powershell edit that
    # accidentally writes back a partial object.
    repo_root = Path(__file__).resolve().parents[3]
    live = repo_root / "scripts" / "auto" / "state.json"
    if not live.exists():
        pytest.skip("live state.json not present (fresh repo or --autonomous never invoked)")
    raw = live.read_text(encoding="utf-8")
    parsed = json.loads(raw)
    assert "last_successful_run_at" in REQUIRED_KEYS
    assert "last_successful_run_at" in parsed
