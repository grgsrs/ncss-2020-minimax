from __future__ import print_function

import importlib
import sys


GOAL = 4  # The length of a sequence of Os or Xs required for victory
COLUMNS = 5
ROWS = 5

NO_MOVE = COLUMNS * ROWS

MAX_DEPTH = 5


def make_board():
    """Return a new, empty, board."""
    return ['.'] * COLUMNS * ROWS


def minimax(player, evaluate, board, alpha, beta, depth):
    """Return an evaluation of the specified board for the given player."""
    if depth == 0 or victory('O', board) or victory('X', board) or '.' not in board:
        # We have reached the maximum depth or there are no more legal moves.
        return evaluate(board)

    new_board = make_board()

    for move in range(COLUMNS * ROWS):
        if is_legal_move(player, move, board, new_board):
            val = minimax('X' if player == 'O' else 'O', evaluate, new_board, alpha, beta, depth - 1)

            if player == 'O':
                if val > alpha:
                    alpha = val
            else:  # player must be 'X'
                if val < beta:
                    beta = val

            if alpha >= beta:
                return alpha if player == 'O' else beta

    return alpha if player == 'O' else beta


def print_board(board):
    for row in range(0, COLUMNS * ROWS, COLUMNS):
        print(''.join(board[row:row+COLUMNS]))
    print()


def is_legal_move(player, pos, board, new_board):
    """Return True and populate new_board if pos is a legal move."""
    if board is not new_board:
        for i, v in enumerate(board):
            new_board[i] = v

    if board[pos] == '.':
        if board is not new_board:
            new_board[pos] = player
        return True

    return False


def one_move(player, evaluate, board):
    """Return the move of the given player."""
    alpha = -2**32 - 1
    beta = 2**32 - 1
    move = NO_MOVE
    new_board = make_board()

    for i in range(COLUMNS * ROWS):
        if is_legal_move(player, i, board, new_board):
            val = minimax('X' if player == 'O' else 'O', evaluate, new_board, alpha, beta, MAX_DEPTH)

            if player == 'O':
                if val > alpha:
                    alpha = val
                    move = i
            else:  # player must be 'X'
                if val < beta:
                    beta = val
                    move = i

    if move != NO_MOVE:
        board[move] = player
    return move


def victory(player, board):
    """Return True if the specified player is victorious"""
    goal = player * GOAL

    for row in range(0, COLUMNS*ROWS, COLUMNS):
        if goal in ''.join(board[row:row+COLUMNS]):
            return True

    rotated = list(board[c + r] for c in range(COLUMNS) for r in range(0, COLUMNS * ROWS, COLUMNS))
    for row in range(0, COLUMNS * ROWS, COLUMNS):
        if goal in ''.join(rotated[row:row + COLUMNS]):
            return True

    return False


def play_game(evaluate1, name1, evaluate2, name2):
    """Play a game of noughts and crosses."""
    board = make_board()
    moves = 0

    while moves < COLUMNS * ROWS:
        one_move('O', evaluate1, board)
        print_board(board)
        if victory('O', board):
            return name1

        one_move('X', evaluate2, board)
        print_board(board)
        if victory('X', board):
            return name2

        moves += 2

    return 'no-one'


def default_evaluate(board):
    """Return a value that is higher if the board is better for the 'O' player or lower otherwise."""
    if victory('O', board):
        return 1

    if victory('X', board):
        return -1

    return 0


def main():
    if not (1 <= len(sys.argv) <= 3):
        sys.stderr.write("usage: python %s [PLAYER1_MODULE] [PLAYER2_MODULE]" % (sys.argv[0],))
        sys.exit(1)

    if len(sys.argv) == 1:
        name1 = 'Default O'
        evaluate1 = default_evaluate
    else:
        name1 = sys.argv[1]
        evaluate1 = importlib.import_module(name1).evaluate

    if len(sys.argv) == 3:
        name2 = sys.argv[2]
        evaluate2 = importlib.import_module(name2).evaluate
    else:
        name2 = 'Default X'
        evaluate2 = default_evaluate

    winner = play_game(evaluate1, name1, evaluate2, name2)
    print("The winner was: %s" % (winner,))


if __name__ == "__main__":
    main()
