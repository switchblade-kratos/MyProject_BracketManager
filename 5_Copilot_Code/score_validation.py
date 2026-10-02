def validate_score(score_a, score_b, is_knockout):
    """Validate two match scores and return the winner, or Draw."""
    for score in (score_a, score_b):
        if isinstance(score, bool) or not isinstance(score, int):
            raise ValueError("Scores must be non-negative integers.")
        if score < 0:
            raise ValueError("Scores must be non-negative integers.")

    if is_knockout and score_a == score_b:
        raise ValueError("Knockout matches cannot end in a tie; provide a tiebreaker result.")

    if score_a > score_b:
        return "A"
    if score_b > score_a:
        return "B"
    return "Draw"