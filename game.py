import sys, random
import pygame as pg
from src.sprite import Sprite
from src.score import Score
from src.button import Button
from src.settings import *


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption("SLIDING PUZZLE")
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.font = pg.font.Font('assets/font/font.ttf', BASIC_FONT_SIZE)
        self.clock = pg.time.Clock()

        self.sprite = Sprite(self.screen, 1, 1)
        self.score = Score(self.screen, self.font)

        self.slide_to = None
        self.flag_hover = False

        self.start_button = Button(self.screen, None, 0, 250, 100, 10, 20, "white",
                                   "assets/images/buttons/normal.png", "assets/images/buttons/pressed.png")
        self.x3_button    = Button(self.screen, "3x3", 35, 250, 100, 10, 475, "white",
                                   "assets/images/buttons/void_normal.png", "assets/images/buttons/void_pressed.png")
        self.x4_button    = Button(self.screen, "4x4", 35, 250, 100, 10, 360, "white",
                                   "assets/images/buttons/void_normal.png", "assets/images/buttons/void_pressed.png")
        self.x5_button    = Button(self.screen, "5x5", 35, 250, 100, 10, 245, "white",
                                   "assets/images/buttons/void_normal.png", "assets/images/buttons/void_pressed.png")

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

            elif event.type == pg.MOUSEBUTTONDOWN:
                self.mouse_position = pg.mouse.get_pos()
                if self.start_button.checkForInput(self.mouse_position):
                    self.flag_hover = True
                    self.generate_new_puzzle(100)
                    self.get_starting_board_complete_flag = True
                    self.flag_hover = False
                elif self.x3_button.checkForInput(self.mouse_position):
                    self.get_size(3)
                elif self.x4_button.checkForInput(self.mouse_position):
                    self.get_size(4)
                elif self.x5_button.checkForInput(self.mouse_position):
                    self.get_size(5)

            elif event.type == pg.KEYDOWN:
                # check if the user pressed a key to slide a tile
                if event.key in (pg.K_LEFT, pg.K_a) and self.is_valid_move(self.get_starting_board, LEFT):
                    self.slide_to = LEFT
                elif event.key in (pg.K_RIGHT, pg.K_d) and self.is_valid_move(self.get_starting_board, RIGHT):
                    self.slide_to = RIGHT
                elif event.key in (pg.K_UP, pg.K_w) and self.is_valid_move(self.get_starting_board, UP):
                    self.slide_to = UP
                elif event.key in (pg.K_DOWN, pg.K_s) and self.is_valid_move(self.get_starting_board, DOWN):
                    self.slide_to = DOWN

                self.make_move_if_valid_move(self.get_starting_board, self.slide_to)
                self.win_condition()

    def get_size(self, board_size):
        if board_size == 3:
            self.sprite.board_size[0] = 3
            self.sprite.board_size[1] = TILE_SIZE
        if board_size == 4:
            self.sprite.board_size[0] = 4
            self.sprite.board_size[1] = (TILE_SIZE * 3) / 4.1
        if board_size == 5:
            self.sprite.board_size[0] = 5
            self.sprite.board_size[1] = (TILE_SIZE * 3) / 5.1
        self.update()

    def get_blank_position(self, board):
        # Return the x and y of board coordinates of the blank space.
        for x in range(self.sprite.board_size[0]):
            for y in range(self.sprite.board_size[0]):
                if board[x][y] == BLANK:
                    return x, y

    def make_move(self, board, move):
        # This function does not check if the move is valid.
        blankX, blankY = self.get_blank_position(board)
        if move == UP:
            board[blankX][blankY], board[blankX][blankY + 1] = board[blankX][blankY + 1], board[blankX][blankY]
        elif move == DOWN:
            board[blankX][blankY], board[blankX][blankY - 1] = board[blankX][blankY - 1], board[blankX][blankY]
        elif move == LEFT:
            board[blankX][blankY], board[blankX + 1][blankY] = board[blankX + 1][blankY], board[blankX][blankY]
        elif move == RIGHT:
            board[blankX][blankY], board[blankX - 1][blankY] = board[blankX - 1][blankY], board[blankX][blankY]

    def is_valid_move(self, board, move):
        blankX, blankY = self.get_blank_position(board)
        return (move == UP and blankY != len(board[1]) - 1)   or (move == DOWN and blankY != 0) or \
               (move == LEFT and blankX != len(board[0]) - 1) or (move == RIGHT and blankX != 0)

    def make_move_if_valid_move(self, board, direction):
        if self.is_valid_move(board, direction):
            self.make_move(board, direction)

    def get_random_move(self, board, lastMove=None):
        # start with a full list of all four moves
        valid_moves = [UP, DOWN, LEFT, RIGHT]
        if lastMove == UP or not self.is_valid_move(board, DOWN):
            valid_moves.remove(DOWN)
        if lastMove == DOWN or not self.is_valid_move(board, UP):
            valid_moves.remove(UP)
        if lastMove == LEFT or not self.is_valid_move(board, RIGHT):
            valid_moves.remove(RIGHT)
        if lastMove == RIGHT or not self.is_valid_move(board, LEFT):
            valid_moves.remove(LEFT)
        # return a random move from the list of remaining moves
        return random.choice(valid_moves)

    def generate_new_puzzle(self, num_slides):
        last_move = None
        for i in range(num_slides):
            move = self.get_random_move(self.get_starting_board, last_move)
            self.make_move(self.get_starting_board, move)
            self.draw()
            pg.time.wait(10)  # pause 10 milliseconds for effect
        self.score.start_timer = True
        self.score.time = 0
        return self.get_starting_board

    def win_condition(self):
        if self.get_starting_board == self.get_starting_board_complete and self.get_starting_board_complete_flag:
            self.get_starting_board_complete_flag = False
            self.score.start_timer = False
            self.score.update()

    def draw(self):
        self.mouse_position = pg.mouse.get_pos()

        self.screen.fill(BACKGROUND_COLOR)

        self.start_button.draw(self.mouse_position)
        self.x3_button.draw(self.mouse_position)
        self.x4_button.draw(self.mouse_position)
        self.x5_button.draw(self.mouse_position)

        self.sprite.draw()
        self.score.draw()
        pg.display.flip()

    def update(self):
        self.get_starting_board_complete_flag = False
        self.get_starting_board_complete = self.sprite.get_starting_board()
        self.get_starting_board = self.sprite.get_starting_board()

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.events()
            self.draw()
            self.score.timer()


if __name__ == '__main__':
    game = Game()
    game.update()
    game.run()
