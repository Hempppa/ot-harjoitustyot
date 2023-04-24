import os
import pygame

class DiffRenderer:
    def __init__(self, display):
        self._display = display
        pygame.display.set_mode((750,750))
        self.base_font = pygame.font.Font(None, 80)
        self.title_font = pygame.font.Font(None, 140)
        self.option_rect = (100, 200, 550, 75)
        dirname = os.path.dirname(__file__)
        self.backround_image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "backround.png"))
        self.backround_rect = self.backround_image.get_rect()
        self.option_rect_list = []
        self.options = 3
        left = self.option_rect[0]
        top = self.option_rect[1]
        width = self.option_rect[2]
        height = self.option_rect[3]
        for i in range(self.options):
            self.option_rect_list.append(pygame.Rect((left, top, width, height)))
            top += 100

    def get_rect_info(self):
        return self.option_rect_list

    def render(self):
        self._display.blit(self.backround_image, self.backround_rect)

        title_text = self.title_font.render("Minesweeper", True, (30, 30, 30))
        self._display.blit(title_text, (60, 60))

        pygame.draw.rect(self._display, (100, 100, 100), self.option_rect_list[0])
        easy_text = self.base_font.render("Easy:       9x9/10", True, (255, 255, 255))
        self._display.blit(easy_text, (self.option_rect[0] +10, self.option_rect_list[0].y+10))

        pygame.draw.rect(self._display, (100, 100, 100), self.option_rect_list[1])
        medium_text = self.base_font.render("Medium:  16x16/40", True, (255, 255, 255))
        self._display.blit(medium_text, (self.option_rect[0] +10, self.option_rect_list[1].y+10))

        pygame.draw.rect(self._display, (100, 100, 100), self.option_rect_list[2])
        hard_text = self.base_font.render("Hard:       30x16/99", True, (255, 255, 255))
        self._display.blit(hard_text, (self.option_rect[0] +10, self.option_rect_list[2].y+10))

        pygame.display.update()
