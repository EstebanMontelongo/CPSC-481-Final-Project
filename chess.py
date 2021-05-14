import pygame as p


# This code logic I got from this youtube video https://www.youtube.com/watch?v=EnYui0e73Rs
def print_board(state):
    # Initializing game constants
    global WIDTH, HEIGHT, DIMENSIONS, SQ_SIZE, MAX_FPS, IMAGES

    DIMENSIONS = len(state)
    WIDTH = HEIGHT = 768
    SQ_SIZE = HEIGHT // DIMENSIONS
    MAX_FPS = 15
    IMAGES = {'bQ': p.transform.scale(p.image.load("images/bQ.png"), (SQ_SIZE, SQ_SIZE))}
    # Initialize game stuff
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState(state)
    running = True

    # Loop & draw board until user presses exit
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def draw_game_state(screen, gs):
    # draw squares on the board
    draw_board(screen, )
    # draw pieces on the board
    draw_pieces(screen, gs.board)


def draw_board(screen):
    colors = [p.Color((240, 217, 181)), p.Color((181, 136, 99))]

    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


class GameState:
    def __init__(self, state):
        self.state = state
        self.board = set_state(self.state)


def set_state(state):
    b_size = len(state)
    board = [[[] for i in range(b_size)] for i in range(b_size)]

    for row in range(len(board)):
        for col in range(len(board[0])):
            if col == state[row]:
                board[row][col] = 'bQ'
            else:
                board[row][col] = '--'
    return board


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
