from datetime import datetime, timezone

from _lib.db import utcnow_iso, now_minus_seconds_iso


def test_utcnow_iso_format():
    """ISO-8601 UTC string ending in Z with second precision."""
    s = utcnow_iso()
    # 2026-07-02T12:34:56Z
    assert s.endswith("Z")
    assert len(s) == 20
    parsed = datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    assert parsed.tzinfo is not None


def test_now_minus_seconds_iso():
    """3600 seconds earlier than now."""
    s = now_minus_seconds_iso(3600)
    parsed = datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    delta = datetime.now(timezone.utc) - parsed
    # allow 5s drift for slow tests
    assert 3595 <= delta.total_seconds() <= 3605