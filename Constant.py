ROWS, COLS = 8,8
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS
LINE_WIDTH = 2
PADDING = SQUARE_SIZE //5
FPS = 60
DELAY = 200

#RGB
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHTGRAY = (211,211,211)
GREEN = (0, 128, 0)


# epsilon Greedy
epsilon_start = 1
epsilon_final = 0.01
epsiln_decay = 100