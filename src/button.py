import pygame as pg


class Button:
    def __init__(self, screen, text, textSize, width, height, left, top, color, background, hover):
        pg.init()
        self.screen = screen
        self.text = text
        self.width, self.height = width, height
        self.left, self.top = left, top
        self.color, self.background = color, background
        self.font = pg.font.Font('assets/font/font.ttf', textSize)

        self.text = self.font.render(self.text, True, self.color)
        self.textRect = pg.Rect(self.left, self.top, self.width, self.height)

        self.background = pg.image.load(background)
        self.background = pg.transform.scale(self.background, (width, height))

        self.flag_hover = False
        self.hover = pg.image.load(hover)
        self.hover = pg.transform.scale(self.hover, (width, height))

    def checkForInput(self, position):
        if position[0] in range(self.textRect.left, self.textRect.right) \
                and position[1] in range(self.textRect.top, self.textRect.bottom):
            self.flag_hover = True
            return True
        return False

    def draw(self, position):
        if position[0] in range(self.textRect.left, self.textRect.right) \
                and position[1] in range(self.textRect.top, self.textRect.bottom):
            self.screen.blit(self.hover, self.textRect)
            self.screen.blit(self.text, (self.left + (self.width // 2) - (self.text.get_width() // 2),
                                         self.top + (self.height // 2) - (self.text.get_height() // 2)))
        else:
            self.screen.blit(self.background, self.textRect)
            self.screen.blit(self.text, (self.left + (self.width // 2) - (self.text.get_width() // 2),
                                         self.top + (self.height // 2) - (self.text.get_height() // 2)))
