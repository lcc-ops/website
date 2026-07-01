from _lib.score import score_topic, SCORE_THRESHOLD


def test_score_zero_when_no_interactions():
    assert score_topic(likes=0, replies=0, quotes=0, reposts=0) == 0


def test_score_weights():
    """replies weight 3, likes and quotes weight 2, reposts weight 1."""
    assert score_topic(likes=10, replies=0, quotes=0, reposts=0) == 20
    assert score_topic(likes=0, replies=10, quotes=0, reposts=0) == 30
    assert score_topic(likes=0, replies=0, quotes=10, reposts=0) == 20
    assert score_topic(likes=0, replies=0, quotes=0, reposts=10) == 10


def test_score_combined():
    """A 5/3/2/2 mix -> 5*2 + 3*3 + 2*2 + 2*1 = 25."""
    assert score_topic(likes=5, replies=3, quotes=2, reposts=2) == 25


def test_threshold_default():
    """SCORE_THRESHOLD is 6 to filter single-engagement spam."""
    assert SCORE_THRESHOLD == 6