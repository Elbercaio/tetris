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
# TODO: guardar peça, drop instantaneo, checkar formula de score, leaderboard
#       visuais melhores, som, .exe
"""
10 x 40 grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
block_size = 20
col_number = 10
row_number = 20
play_width = block_size * col_number
play_height = block_size * row_number
s_width = play_width + 400
s_height = play_height + 100
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS

S = [['......',
      '......',
      '...00.',
      '..00..',
      '......',
      '......'],
     ['......',
      '..0...',
      '..00..',
      '...0..',
      '......',
      '......']]

Z = [['......',
      '......',
      '.00...',
      '..00..',
      '......',
      '......'],
     ['......',
      '...0..',
      '..00..',
      '..0...',
      '......',
      '......']]

Hero = [['......',  # I
         '..0...',
         '..0...',
         '..0...',
         '..0...',
         '......'],
        ['......',
         '......',
         '.0000.',
         '......',
         '......',
         '......']]

Smashboy = [['......',  # O
             '......',
             '..00..',
             '..00..',
             '......',
             '......']]

J = [['......',
      '......',
      '..0...',
      '..000.',
      '......',
      '......', ],
     ['......',
      '..00..',
      '..0...',
      '..0...',
      '......',
      '......'],
     ['......',
      '......',
      '.000..',
      '...0..',
      '......',
      '......'],
     ['......',
      '...0..',
      '...0..',
      '..00..',
      '......',
      '.......']]

L = [['......',
      '......',
      '...0..',
      '.000..',
      '......',
      '......'],
     ['......',
      '..0...',
      '..0...',
      '..00..',
      '......',
      '......'],
     ['......',
      '......',
      '.000..',
      '.0....',
      '......',
      '......'],
     ['......',
      '..00..',
      '...0..',
      '...0..',
      '......',
      '......']]

T = [['......',
      '..0...',
      '.000..',
      '......',
      '......',
      '......'],
     ['......',
      '..0...',
      '..00..',
      '..0...',
      '......',
      '......'],
     ['......',
      '......',
      '.000..',
      '..0...',
      '......',
      '......'],
     ['......',
      '..0...',
      '.00...',
      '..0...',
      '......',
      '......']]

shapes = [S, Z, Hero, Smashboy, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0),
                (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece():
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions={}):
    # gerar grid vazio
    grid = [[(0, 0, 0) for _ in range(col_number)] for _ in range(row_number)]

    # checar se existe posição já preenchida
    for y, row in enumerate(grid):
        for x, _ in enumerate(row):
            if (x, y) in locked_positions:
                pos = locked_positions[(x, y)]
                grid[y][x] = pos

    return grid


def convert_shape_format(shape):
    positions = []
    form = shape.shape[shape.rotation % len(shape.shape)]

    for y, line in enumerate(form):
        row = list(line)
        for x, col in enumerate(row):
            if col == '0':
                positions.append((shape.x + x, shape.y + y))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_pos = [(j, i) for j in range(col_number)
                    for i in range(row_number) if grid[i][j] == (0, 0, 0)]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(surface, text, size=40, color=(255, 255, 255)):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    label = font.render(text, 1, color)
    center_x = top_left_x + play_width / 2 - label.get_width() / 2
    center_y = top_left_y + play_height / 2 - label.get_height() / 2
    surface.blit(label, (center_x, center_y))


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y
    for y, row in enumerate(grid):
        start_pos_row = (sx, sy + y * block_size)
        end_pos_row = (sx + play_width, sy + y * block_size)
        pygame.draw.line(surface, (128, 128, 128), start_pos_row, end_pos_row)
        for x, col in enumerate(row):
            start_pos_col = (sx + x * block_size, sy)
            end_pos_col = (sx + x * block_size, sy + play_height)
            pygame.draw.line(surface, (128, 128, 128), start_pos_col,
                             end_pos_col)


def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            idx = i
            for j, _ in enumerate(row):
                try:
                    del locked[(j, i)]
                except Exception:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < idx:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc


def draw_next_shape(surface, shape):
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    label = font.render('Próxima peça', 1, (255, 255, 255))

    sx = top_left_x + play_width + 45
    sy = top_left_y + play_height / 2 - 100
    surface.blit(label, (sx - 15, sy - 30))
    form = shape.shape[shape.rotation % len(shape.shape)]

    for y, line in enumerate(form):
        row = list(line)
        for x, col in enumerate(row):
            if col == '0':
                rect = (sx + x * block_size, sy + y * block_size,
                        block_size, block_size)
                pygame.draw.rect(surface, shape.color, rect, 0)


def draw_window(surface, grid, score=0, highscore=0):
    surface.fill((0, 0, 0))

    font = pygame.font.Font(pygame.font.get_default_font(), 60)
    label = font.render('Tetris', 1, (255, 255, 255))
    center = top_left_x + play_width / 2 - label.get_width() / 2
    surface.blit(label, (center, 25))
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            width = block_size
            height = block_size
            left = top_left_x + x * width
            top = top_left_y + y * height
            pygame.draw.rect(surface, col, (left, top, width, height))

    draw_grid(surface, grid)
    pygame.draw.rect(surface, (255, 0, 0),
                     (top_left_x, top_left_y, play_width, play_height), 5)

    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    sx = top_left_x + play_width + 45
    sy = top_left_y + play_height / 2 + 160
    label = font.render(f'Pontuação: {score}', 1, (255, 255, 255))
    surface.blit(label, (sx - 15, sy - 30))
    label = font.render(f'Recorde: {highscore}', 1, (255, 255, 255))
    surface.blit(label, (sx - 10, sy - 10))


def update_score(nscore):  # criar leaderboard
    score = max_score()

    with open('leaderboard.txt') as f:
        if nscore > score:
            f.write(str(nscore))
        else:
            f.write(str(score))


def max_score():
    with open('leaderboard.txt') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return int(score)


def main(win):
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.4
    level_time = 0
    highscore = max_score()
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.001

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

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

        shape_pos = convert_shape_format(current_piece)
        for pos in shape_pos:
            x, y = pos
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                x, y = pos
                locked_positions[(x, y)] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(window, grid, score, highscore)
        draw_next_shape(window, next_piece)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(window, "Derrota", 40, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)


def main_menu(window):
    run = True
    while run:
        window.fill((0, 0, 0))
        draw_text_middle(window, 'Aperte qualquer tecla para jogar', 20,
                         (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if (event.type == pygame.KEYDOWN
                    or event.type == pygame.MOUSEBUTTONDOWN):
                main(window)

    pygame.display.quit()


window = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(window)  # start game
