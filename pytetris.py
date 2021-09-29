import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 600
play_width = 250  # meaning 300 // 10 = 30 width per block
play_height = 500  # meaning 600 // 20 = 20 height per block
block_size = 25

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


# SHAPE FORMATS

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0),
                (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece():
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.shape_color = shape_colors[shapes.index(shapes)]
        self.rotation = 0


def create_grid(locked_positions={}):
    # gerar grid vazio
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    # checar se existe posição já preenchida
    for y, row in enumerate(grid):
        for x, _ in enumerate(row):
            if (x, y) in locked_positions:
                pos = locked_positions[(x, y)]
                grid[x][y] = pos

    return grid


def convert_shape_format(shape):
    pass


def valid_space(shape, grid):
    pass


def check_lost(positions):
    pass


def get_shape():
    return Piece(5, -1, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    pass


def draw_grid(surface, grid):
    for y, row in enumerate(grid):
        for x, color in enumerate(row):
            width = block_size
            height = block_size
            left = top_left_x + x * width
            top = top_left_y + y * height
            pygame.draw.rect(surface, color, (left, top, width, height))

    pygame.draw.rect(surface, (255, 0, 0),
                     (top_left_x, top_left_y, play_width, play_height))


def clear_rows(grid, locked):
    pass


def draw_next_shape(shape, surface):
    pass


def draw_window(surface):
    surface.fill((0, 0, 0))

    font = pygame.font.Font(pygame.font.get_default_font(), 60)
    label = font.render('Tetris', 1, (255, 255, 255))
    center = top_left_x + play_width / 2 - label.get_width() / 2
    surface.blit(center, 25)
    draw_grid(surface, grid)
    pygame.display.update()


def main(win):
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = True
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1

        draw_window(surface, grid)


def main_menu(window):
    main(window)
    pass


window = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(window)  # start game
