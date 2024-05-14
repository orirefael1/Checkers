import numpy as np
import pygame
import time

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
LINE_WIDTH = 2
SQUARE_SIZE = 100
PADDING = SQUARE_SIZE //5
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 480



# window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


#RGB
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHTGRAY = (211,211,211)
GREEN = (0, 128, 0)
BROWN = (193, 154, 107)
BRONZE = (110, 77, 37)



class Graphics:
    def __init__(self, win, board):
        pygame.init()
        self.board = board
        rows, cols = board.shape
        self.win = win
        self.rows = rows
        self.cols = cols
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))


    def draw_Lines(self):
        for i in range(ROWS):
            pygame.draw.line(self.win, BLACK, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE , WIDTH), width=LINE_WIDTH)
            pygame.draw.line(self.win, BLACK, (0, i * SQUARE_SIZE), (HEIGHT, i * SQUARE_SIZE ), width=LINE_WIDTH)


    def draw_all_pieces(self, board):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] !=0 :
                    self.draw_pieces(board)


    def draw_board(self):
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(self.window, WHITE, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


    def drawPiece(self, window, color, col, row, queen = False):
        if not queen:
            radius = SQUARE_SIZE // 2 - 12
            x = SQUARE_SIZE * col + SQUARE_SIZE // 2
            y = SQUARE_SIZE * row + SQUARE_SIZE // 2
            pygame.draw.circle(window, color, (x, y), radius)  
        else:
            radius = SQUARE_SIZE // 2 - 12
            x = SQUARE_SIZE * col + SQUARE_SIZE // 2
            y = SQUARE_SIZE * row + SQUARE_SIZE // 2
            pygame.draw.circle(window, color, (x, y), radius)  
            pygame.draw.circle(window, RED, (x, y), radius - 25)  


    def draw_pieces(self, board):
        for col in range(8):
            for row in range(8):
                if board[row][col] == 1:
                    Graphics.drawPiece(self, self.window, WHITE, col, row)
                if board[row][col] == 2:
                    Graphics.drawPiece(self, self.window, BRONZE, col, row)
                if board[row][col] == 3:
                    Graphics.drawPiece(self, self.window, WHITE, col, row, True)
                if board[row][col] == 4:
                    Graphics.drawPiece(self, self.window, BRONZE, col, row, True)


    def calc_pos(self, row_col):
        row, col = row_col
        y = row * SQUARE_SIZE + SQUARE_SIZE//2
        x = col * SQUARE_SIZE + SQUARE_SIZE//2
        return x, y


    def calc_base_pos(self, row_col):
        row, col = row_col
        y = row * SQUARE_SIZE
        x = col * SQUARE_SIZE
        return x, y


    def calc_row_col(self, pos):
        x, y = pos
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE
        return row, col


    def calc_color(self, player):
        if player == 1:
            return WHITE
        elif player == 2:
            return BLACK
        else:
            return LIGHTGRAY

    def draw(self, board):
        self.win.fill(BLACK)
        self.draw_board()
        self.draw_all_pieces(board)

    def draw_square(self, row_col, color):
        pos = self.calc_base_pos(row_col)
        pygame.draw.rect(self.win, color, (*pos, SQUARE_SIZE, SQUARE_SIZE))

    def blink(self, row_col, color):
        row, col = row_col
        player = self.board[row][col]
        for i in range (2):
            self.draw_square((row, col), color)
            if player:
                self.draw_piece((row ,col), player) 
            pygame.display.update()
            time.sleep(0.2)
            self.draw_square((row, col), LIGHTGRAY)
            if player:
                self.draw_piece((row,col), player) 
            pygame.display.update()
            time.sleep(0.2)



    






