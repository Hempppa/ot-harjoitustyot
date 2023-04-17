import os
import pygame

#ei vielä käytetä missään
class CustomRenderer:
    def __init__(self, display):
        self._display = display
        pygame.display.set_mode((750,750))
        self.fonts = [pygame.font.Font(None, 140), pygame.font.Font(None, 70)]
        self.rect = (200, 75)
        dirname = os.path.dirname(__file__)
        self.backround_image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "backround.png"))
        self.width_info = ["16", False, (70, 250, self.rect[0], self.rect[1])]
        self.height_info = ["16", False, (380, 250, self.rect[0], self.rect[1])]
        self.mines_info = ["40", False, (70, 450, self.rect[0]*2, self.rect[1])]
        self.colours = [(10,10,10), (30,30,50)]

    def set_text(self, text, which):
        if which == 1 and self.width_info[1]:
            self.width_info[0] = text
        elif which == 2 and self.height_info[1]:
            self.height_info[0] = text
        elif which == 3 and self.mines_info[1]:
            self.mines_info[0] = text

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

    def get_rect_info(self):
        info = []
        info.append([self.width_info[0], self.width_info[1], pygame.Rect(self.width_info[2])])
        info.append([self.height_info[0], self.height_info[1], pygame.Rect(self.height_info[2])])
        info.append([self.mines_info[0], self.mines_info[1], pygame.Rect(self.mines_info[2])])
        return info

    def render(self):
        backround_rect = self.backround_image.get_rect()
        self._display.blit(self.backround_image, backround_rect)

        title_text = self.fonts[0].render("Minesweeper", True, (30, 30, 30))
        self._display.blit(title_text, (60, 60))

        width_text = self.fonts[1].render("Width (1-38):", True, (255, 255, 255))
        self._display.blit(width_text, (70, 200))
        if self.width_info[1]:
            pygame.draw.rect(self._display, self.colours[1], self.width_info[2])
        else:
            pygame.draw.rect(self._display, self.colours[0], self.width_info[2])
        width_value = self.fonts[1].render(self.width_info[0], True, (200, 200, 200))
        self._display.blit(width_value, (80, 260))

        height_text = self.fonts[1].render("Height (1-18):", True, (255, 255, 255))
        self._display.blit(height_text, (380, 200))
        if self.height_info[1]:
            pygame.draw.rect(self._display, self.colours[1], self.height_info[2])
        else:
            pygame.draw.rect(self._display, self.colours[0], self.height_info[2])
        height_value = self.fonts[1].render(self.height_info[0], True, (200, 200, 200))
        self._display.blit(height_value, (390, 260))

        mines_text = self.fonts[1].render("Mines (1-798):", True, (255, 255, 255))
        self._display.blit(mines_text, (70, 400))
        if self.mines_info[1]:
            pygame.draw.rect(self._display, self.colours[1], self.mines_info[2])
        else:
            pygame.draw.rect(self._display, self.colours[0], self.mines_info[2])
        mines_value = self.fonts[1].render(self.mines_info[0], True, (200, 200, 200))
        self._display.blit(mines_value, (80, 460))

        start_text = self.fonts[0].render("Enter to start", True, (10,10,10))
        self._display.blit(start_text, (70, 600))
        start_text = self.fonts[0].render("Enter to start", True, (255,255,255))
        self._display.blit(start_text, (68, 598))

        pygame.display.update()
