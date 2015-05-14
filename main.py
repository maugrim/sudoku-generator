#!/usr/bin/env python
"""
Playground for generating valid Sudoku boards (Russel's interview question.)
"""
import argparse
import random
import logging
import math

def candidates_for(board, n, dimension, x, y):
    """
    Given a point on an existing board, return the set of numbers
    which could be placed there without violating constraints.
    """
    candidates = set(xrange(n))

    # elements on the same row
    for val in board[y]:
        candidates.discard(val)

    # elements in the same column
    for row in board:
        candidates.discard(row[x])

    # elements in the same box
    box_x, box_y = int(x / dimension), int(y / dimension)
    y_range = range(box_y * dimension, (box_y + 1) * dimension)
    x_range = range(box_x * dimension, (box_x + 1) * dimension)
    for y in y_range:
        row = board[y]
        for x in x_range:
            candidates.discard(row[x])

    return candidates

def next_slot(n, x, y):
    """
    Given coordinates (x, y) on a board of size N, return the
    coordinates of the next slot to be filled (left-to-right,
    top-to-bottom).
    """
    if x == n - 1: # wrap to next row
        return (0, y + 1)
    else:
        return (x + 1, y)

def complete_board(board, n, dimension, x, y, shuffle=True):
    """
    Produces a completion of the current board which has been filled
    left-to-right, top-to-bottom, up to but not including point (x, y).
    """
    candidates = candidates_for(board, n, dimension, x, y)
    if shuffle:
        candidates = list(candidates)
        random.shuffle(candidates)

    for val in candidates:
        board[y][x] = val
        new_x, new_y = next_slot(n, x, y)
        if new_y > y:
            logging.info("Beginning to attempt row %s.", new_y)
        if new_y >= n: # we're done
            return board
        else:
            completion = complete_board(board, n, dimension, new_x, new_y)
            if completion:
                return completion
            else:
                board[y][x] = None
                logging.debug("Failed to place %s in slot (%s, %s); available candidates are %s.", val, x, y, candidates)


    # nothing worked
    logging.debug("Gave up on filling slot (%s, %s) with candidates %s; backtracking.", x, y, candidates)
    return None

def generate_board(dimension, **kwargs):
    """
    Generates a random valid Sudoku board of the given dimension using
    backtracking. The board will be represented as a list of length
    dimension ** 2 containing ordered nested lists of length dimension ** 2
    representing each row.
    """
    # board elements contain None when they are not yet determined
    n = dimension ** 2
    empty_board = [[None for _ in range(n)] for _ in range(n)]
    return complete_board(empty_board, n, dimension, 0, 0, **kwargs)

def format_board(board, dimension):
    "Returns a formatted representation of the board, one row per line."
    value_length = int(math.ceil(math.log10(dimension ** 2)))
    def format_value(val):
        return str(val).rjust(value_length)
    return "\n".join("[{}]".format(", ".join(map(format_value, row))) for row in board)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("dimension", type=int, help="The dimension of the board (e.g. 3 makes a 9x9 board.)")
    parser.add_argument('--verbose', '-v', action='count', help="Whether to include verbose debugging output.")
    parser.add_argument('--shuffle', action='store_true', help="Whether to generate a random board or just a valid one.")
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    board = generate_board(args.dimension, shuffle=args.shuffle)
    if not board:
        print "Couldn't generate a valid board."
    else:
        print format_board(board, args.dimension)
