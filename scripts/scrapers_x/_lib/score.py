"""Pure scoring for X.com topic candidates.

Mirrors the SQL expression used in SKILL.md Step 2:

    (likes * 2) + (replies * 3) + (quotes * 2) + reposts

Reply weight is highest because comment threads on AI-monetization posts
tend to surface real numbers ("made $X from Y"). Like/quote weight 2 each.
Repost weight 1 to dampen viral-but-shallow posts.
"""

from __future__ import annotations

SCORE_THRESHOLD: int = 6


def score_topic(
    likes: int = 0,
    replies: int = 0,
    quotes: int = 0,
    reposts: int = 0,
) -> int:
    return likes * 2 + replies * 3 + quotes * 2 + reposts