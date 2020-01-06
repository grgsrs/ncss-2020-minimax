from noughts_crosses import MAX_SCORE, MIN_SCORE, victory


def evaluate(board):
    """Return a value that is higher if the board is better for the 'O' player or lower otherwise."""
    if victory('O', board):
        return MAX_SCORE

    if victory('X', board):
        return MIN_SCORE

    return 0
