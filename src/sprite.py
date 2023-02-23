import pygame as pg
from src.settings import *


class Sprite:
    def __init__(self, screen, tileX, tileY):
        pg.init()
        self.screen = screen
        self.tileX, self.tileY = tileX, tileY
        self.board_size = [3, 175]
        self.font = pg.font.Font("assets/font/font.ttf", 25)
        self.get_starting_board()

    def get_starting_board(self):
        counter = 1
        self.board = []
        for x in range(self.board_size[0]):
            column = []
            for y in range(self.board_size[0]):
                column.append(counter)
                counter += self.board_size[0]
            self.board.append(column)
            counter -= self.board_size[0] * (self.board_size[0] - 1) + self.board_size[0] - 1

        self.board[self.board_size[0] - 1][self.board_size[0] - 1] = BLANK
        return self.board

    def load_sprites(self):
        image = pg.image.load("assets/images/tiles/normal_tile.png")
        self.image = pg.transform.scale(image, (self.board_size[1], self.board_size[1]))
        return self.image

    def get_left_top_of_tile(self, tileX, tileY):
        left = (self.tileX + 300) + (tileX * self.board_size[1]) + (tileX * 10)
        top = (self.tileY + 20) + (tileY * self.board_size[1]) + (tileY * 10)
        return left, top

    def draw_tile(self, tileX, tileY, adjX=0, adjY=0):
        # draw a tile at board coordinates tilex and tiley, optionally a few
        left, top = self.get_left_top_of_tile(tileX, tileY)

        self.str_array = str(self.board[tileX][tileY])
        self.text_rect = pg.Rect(left + adjX, top + adjY, self.board_size[1], self.board_size[1])
        self.text_array = self.font.render(self.str_array, True, "white")

        self.screen.blit(self.image, self.text_rect)
        self.screen.blit(self.text_array, (left + (self.board_size[1] // 2) - (self.text_array.get_width() // 2),
                                           top + (self.board_size[1] // 2) - (self.text_array.get_height() // 2)))

    def draw_tiles(self):
        for x in range(self.board_size[0]):
            for y in range(self.board_size[0]):
                if self.board[x][y]:
                    self.draw_tile(x, y)

    def draw(self):
        self.load_sprites()
        self.draw_tiles()
