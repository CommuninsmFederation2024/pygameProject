import pygame

WINDOW = {
    'width': 800,
    'height': 800
}

# quantity pixels
CELL_SIZE = 35

CELLS_COLORS = [
    '#AAD750',
    '#A1D14A'
]
SNAKE_COLORS = [
    '#4472E7',
    '#18439F'
]
HEIGHT_SNAKE = [
    int(CELL_SIZE // 2 * 0.9) * 2,
    int(CELL_SIZE // 2 * 0.5) * 2
]

SCREEN_COLOR = '#588A34'

SNAKE_LENGHT = 7

DIRS = [
    pygame.K_UP,
    pygame.K_RIGHT,
    pygame.K_DOWN,
    pygame.K_LEFT
]

REVERSE_DIRS = {
    pygame.K_UP: pygame.K_DOWN,
    pygame.K_RIGHT: pygame.K_LEFT,
    pygame.K_DOWN: pygame.K_UP,
    pygame.K_LEFT: pygame.K_RIGHT
}

SHIFT = {
    pygame.K_UP: (0, -1),
    pygame.K_RIGHT: (1, 0),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0)
}

IMGS_PATH = r'D:\PROJECT PYGAME\NEW2\FULL PROJECT'

SCORE_COLOR = 'WHITE'

SCORE_PATH = r'D:\PROJECT PYGAME\NEW2\FULL PROJECT'
SCORES_FILE_NAME = 'scores.txt'
SCORE_SPACE = 10  # px
