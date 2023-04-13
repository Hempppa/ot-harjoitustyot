import pygame
import os


class MenuRenderer:
    def __init__(self, display):
        self._display = display

        # for startmenu renderer
        self.base_font = pygame.font.Font(None, 80)
        self.title_font = pygame.font.Font(None, 140)
        self.option_rect = (100, 200, 550, 75)
        dirname = os.path.dirname(__file__)
        self.backround_image = pygame.image.load(os.path.join(dirname, "..", "assets", "backround.png"))
        self.backround_rect = self.backround_image.get_rect()
        self.option_rect_list = []
        self.options = 3
        for i in range(self.options):
            self.option_rect_list.append(pygame.Rect(
                self.option_rect[0], self.option_rect[1]+100*i, self.option_rect[2], self.option_rect[3]))

    def startRender(self):
        self._display.blit(self.backround_image, self.backround_rect)

        title_text = self.title_font.render("Minesweeper", True, (30, 30, 30))
        self._display.blit(title_text, (60, 60))

        pygame.draw.rect(self._display, (100, 100, 100), self.option_rect_list[0])
        diff_text = self.base_font.render("Default difficulties", True, (255, 255, 255))
        self._display.blit(diff_text, (self.option_rect.x +10, self.option_rect_list[0].y+10))

        pygame.draw.rect(self._display, (100, 100, 100),self.option_rect_list[1])
        custom_text = self.base_font.render("Custom difficulty", True, (255, 255, 255))
        self._display.blit(custom_text, (self.option_rect.x +10, self.option_rect_list[1].y+10))

        pygame.draw.rect(self._display, (100, 100, 100), self.option_rect_list[2])
        leaderboard_text = self.base_font.render("Leaderboard", True, (255, 255, 255))
        self._display.blit(leaderboard_text, (self.option_rect.x+10, self.option_rect_list[2].y+10))

        pygame.display.update()
