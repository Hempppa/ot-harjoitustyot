import os
import pygame

#ei vielä käytetä missään
class DiffRenderer:
    def __init__(self, display):
        self._display = display
        self.fonts = [pygame.font.Font(None, 140), pygame.font.Font(None, 80)]
        self.rect = (200, 75)
        dirname = os.path.dirname(__file__)
        self.backround_image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "backround.png"))
        self.width_info = ["", False]
        self.height_info = ["", False]
        self.mines_info = ["", False]
        self.colours = [(10,10,10), (30,30,50)]

    def set_text(self, text, which):
        if which == 1 and self.width_info[1]:
            self.width = text
        elif which == 2 and self.height_info[1]:
            self.height = text
        elif which == 3 and self.mines_info[1]:
            self.mines = text

    def set_active(self, which):
        if which == 1:
            self.width_info[1] = True
            self.height_info[1] = False
            self.mines_info[1] = False
        elif which == 2:
            self.width_info[1] = False
            self.height_info[1] = True
            self.mines_info[1] = False
        elif which == 3:
            self.width_info[1] = False
            self.height_info[1] = False
            self.mines_info[1] = True
        else:
            self.width_info[1] = False
            self.height_info[1] = False
            self.mines_info[1] = False

    def render(self):
        backround_rect = self.backround_image.get_rect()
        self._display.blit(self.backround_image, backround_rect)

        title_text = self.fonts[0].render("Minesweeper", True, (30, 30, 30))
        self._display.blit(title_text, (60, 60))

        width_text = self.fonts[1].render("Width:", True, (255, 255, 255))
        self._display.blit(width_text, (100, 200))
        if self.width_info[1]:
            pygame.draw.rect(self._display, self.colours[1], (100, 300, self.rect[0], self.rect[1]))
        else:
            pygame.draw.rect(self._display, self.colours[0], (100, 300, self.rect[0], self.rect[1]))
        width_value = self.fonts[1].render(self.width_info[0], True, (200, 200, 200))
        self._display.blit(width_value, (105, 305))

        height_text = self.fonts[1].render("Height:", True, (255, 255, 255))
        self._display.blit(height_text, (300, 200))
        if self.height_info[1]:
            pygame.draw.rect(self._display, self.colours[1], (300, 300, self.rect[0], self.rect[1]))
        else:
            pygame.draw.rect(self._display, self.colours[0], (300, 300, self.rect[0], self.rect[1]))
        height_value = self.fonts[1].render(self.height_info[0], True, (200, 200, 200))
        self._display.blit(height_value, (305, 305))

        mines_text = self.fonts[1].render("Mines:", True, (255, 255, 255))
        self._display.blit(mines_text, (100, 400))
        if self.mines_info[1]:
            pygame.draw.rect(self._display, self.colours[1], (100, 500, self.rect[0], self.rect[1]))
        else:
            pygame.draw.rect(self._display, self.colours[0], (100, 500, self.rect[0], self.rect[1]))
        height_value = self.fonts[1].render(self.height_info[0], True, (200, 200, 200))
        self._display.blit(height_value, (105, 505))

        pygame.display.update()
