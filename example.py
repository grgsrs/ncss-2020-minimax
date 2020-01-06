
MAX_DEPTH = 3


def evaluate(board):
    """Return a value that is higher if the board is better for the 'O' player or lower otherwise."""
    return board.count('O') - board.count('X')
