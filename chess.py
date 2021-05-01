from constants import *


# prints a line of the chess board given the col position
def print_line(col):
    line_string = ''
    line_string += '│'
    for i in range(TABLESIZE):
        if i == col:
            line_string += '♛'
        else:
            line_string += '  '
        line_string += '│'

    for i in line_string:
        print("\u0332" + i, end='')
    print('')


# prints the chess board given the current state
def print_state(state):
    for col in state:
        print_line(col)
    print('')


# removes the queens that are under attack for displaying a solution
def remove_attacking_queens(state):
    state_copy = state.copy()
    for row in range(TABLESIZE):
        pos = {tuple()}
        col = state[row]
        # find all squares the current queen attacks
        pos = find_queen_attack_squares(row, col, pos)

        for row2 in range(TABLESIZE):
            # skip itself, since it can't attack itself
            if row2 == row:
                continue
            col2 = state[row2]
            # checks is other queens are under attack, if so remove the current queen
            if (row2, col2) in pos:
                state_copy[row] = -1
    return state_copy


# check if the row/col position is on the board
def check_range(row, col):
    return 0 <= row < TABLESIZE and 0 <= col < TABLESIZE


# find and return all the row/col positions that the current queen is attacking
def find_queen_attack_squares(row, col, pos):
    for row_offset, col_offset in MOVES:
        new_row = row + row_offset
        new_col = col + col_offset
        while check_range(new_row, new_col):
            pos.add((new_row, new_col))
            new_row += row_offset
            new_col += col_offset
    return pos


# count the number of queens that are not being attacked
# Also known as fitness
def count_safe_queens(state):
    safeQueens = 0
    for row in range(TABLESIZE):
        pos = {tuple()}
        col = state[row]
        # find all squares the current queen attacks
        pos = find_queen_attack_squares(row, col, pos)

        safe = True
        for row2 in range(TABLESIZE):
            # skip itself, since it can't attack itself
            if row2 == row:
                continue
            col2 = state[row2]
            # checks is other queens are under attack, if so remove the current queen from count
            if (row2, col2) in pos:
                safe = False
                break
        if safe:
            safeQueens += 1
    return safeQueens
