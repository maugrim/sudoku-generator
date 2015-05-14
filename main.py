#!/usr/bin/env python
"""
Playground for generating valid Sudoku boards (Russel's interview question.)
"""
import argparse
import random

def union(*iterables):
    "Return a set that is the union of all the given iterables."
    results = set()
    for iterable in iterables:
        results.update(iterable)
    return results

def candidates_for(board, n, dimension, x, y):
    """
    Given a point on an existing board, return the set of numbers
    which could be placed there without violating constraints.
    """
    row_elements = board[y]
    column_elements = (row[x] for row in board)

    def box_elements(board, dimension, x, y):
        "Returns all of the numbers in the same box as (x, y)."
        box_x, box_y = int(x / dimension), int(y / dimension)
        for y in range(box_y * dimension, (box_y + 1) * dimension):
            row = board[y]
            for x in range(box_x * dimension, (box_x + 1) * dimension):
                yield row[x]

    existing = union(row_elements, column_elements, box_elements(board, dimension, x, y))
    return filter(lambda x: x not in existing, range(n))

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

def complete_board(board, n, dimension, x, y):
    """
    Produces a completion of the current board which has been filled
    left-to-right, top-to-bottom, up to but not including point (x, y).
    """
    candidates = candidates_for(board, n, dimension, x, y)
    random.shuffle(candidates)

    for val in candidates:
        board[y][x] = val
        new_x, new_y = next_slot(n, x, y)
        if new_y >= n: # we're done
            return board
        else:
            completion = complete_board(board, n, dimension, new_x, new_y)
            if completion:
                return completion
            else:
                board[y][x] = None

    # nothing worked
    return None

def generate_board(dimension):
    """
    Generates a random valid Sudoku board of the given dimension using
    backtracking. The board will be represented as a list of length
    dimension ** 2 containing ordered nested lists of length dimension ** 2
    representing each row.
    """
    # board elements contain None when they are not yet determined
    n = dimension ** 2
    empty_board = [[None for _ in range(n)] for _ in range(n)]
    return complete_board(empty_board, n, dimension, 0, 0)

def format_board(board):
    "Returns a formatted representation of the board, one row per line."
    return "\n".join("[{}]".format(", ".join(map(str, row))) for row in board)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("dimension", type=int, help="The dimension of the board (e.g. 3 makes a 9x9 board.)")
    args = parser.parse_args()
    board = generate_board(args.dimension)
    if not board:
        print "Couldn't generate a valid board."
    else:
        print format_board(board)
