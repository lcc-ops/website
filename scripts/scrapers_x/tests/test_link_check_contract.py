"""Contract tests for scripts/check/link_check.mjs.

Reads the script as text and asserts key invariants. Catches drift between
the link checker and astro.config.mjs without booting up Node.

These tests do *not* execute the .mjs file — they assume the file is in a
self-describing form (hardcoded SITE_URL, embedded STATIC_ROUTES, output path
matches scripts/check/_out_linkcheck.txt).
"""
from __future__ import annotations

from pathlib import Path

SITE_URL = "https://kuajinglab.xyz"
REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT = REPO_ROOT / "scripts" / "check" / "link_check.mjs"


def _read() -> str:
    assert SCRIPT.exists(), f"link_check.mjs not found at {SCRIPT}"
    return SCRIPT.read_text(encoding="utf-8")


def test_link_check_uses_canonical_site_url() -> None:
    src = _read()
    assert SITE_URL in src, "SITE_URL fallback must match astro.config.mjs"


def test_link_check_writes_to_expected_output_path() -> None:
    src = _read()
    assert "_out_linkcheck.txt" in src, "Output path constant drift"


def test_link_check_has_static_routes_constant() -> None:
    src = _read()
    assert "STATIC_ROUTES" in src, "Static-routes array drift"


def test_link_check_is_diagnostic_always_exits_zero() -> None:
    src = _read()
    # Link checker must not fail builds; the contract is "always exit 0".
    assert "process.exit(0)" in src or "exit 0" in src


def test_link_check_uses_node_builtin_fetch() -> None:
    src = _read()
    # No new deps allowed — reject any of the well-known HTTP libs.
    for banned in ("node-fetch", "axios", "got", "undici", "request"):
        assert banned not in src, f"new HTTP dep sneaked in: {banned}"
    # But Node 20+ fetch must be in use.
    assert "fetch(" in src
