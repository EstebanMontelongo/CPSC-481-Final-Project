# prints a line of the chess board given the col position
def print_line(col, table_size):
    line_string = ''
    line_string += '│'
    for i in range(table_size):
        if i == col:
            line_string += '♛'
        else:
            line_string += '  '
        line_string += '│'

    for i in line_string:
        print("\u0332" + i, end='')
    print('')


# prints the chess board given the current state
def print_state(state, table_size):
    for col in state:
        print_line(col, table_size)
    print('')


# removes the queens that are under attack for displaying a solution
def remove_attacking_queens(state, table_size):
    state_copy = state.copy()
    for row in range(table_size):
        col = state[row]
        safe = True
        for row2 in range(row, table_size):
            # skip itself, since it can't attack itself
            if row2 == row:
                continue
            col2 = state[row2]
            # checks is other queens are under attack, if so remove the current queen
            if col == col2 or abs(row - row2) == abs(col - col2):
                state_copy[row] = -1
    return state_copy


# Check if queen is attacking other queens
def count_safe_queens(state, table_size):
    safe_queens = 0
    for row in range(table_size):
        col = state[row]
        safe = True
        for row2 in range(row, table_size):
            # skip itself, since it can't attack itself
            if row2 == row:
                continue
            col2 = state[row2]
            # checks is other queens are under attack, if so remove the current queen from count
            if col == col2 or abs(row - row2) == abs(col - col2):
                safe = False
                break
        if safe:
            safe_queens += 1
    return safe_queens
