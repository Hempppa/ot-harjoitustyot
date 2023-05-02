import os
import pygame
from config import BACKGROUND_IMAGE

class MenuRenderer:
    """Piirtä alkunäkymän. Tässä on kolme vaihtoehtoa mihin siirtyä seuraavaksi

    Attributes:
        _display: ikkuna johon näkymä piirretään
        fonts: lista pygame.font.Font():eista joita näkymä käyttää
        option_rect: kenttien vakio sijainti
        backround_image: taustakuva, ladataan assets kansiosta config.py BACKGROUND_IMAGE muuttujan nimellä
        option_rect_list: lista vaihtoehto kentistä
        options: vaihtoehtojen lkm
    """
    def __init__(self, display):
        """Alustaa tietoja, mm. lataa taustakuvan, määrittää fontteja ja vaihtoehtokenttiä jne.

        Args:
            display: ikkuna johon näkymä piirretään
        """
        self._display = display
        if pygame.display.get_window_size() != (750,750):
            pygame.display.set_mode((750,750))
        self.fonts = [pygame.font.Font(None, 140), pygame.font.Font(None, 70), pygame.font.Font(None, 60)]
        self.option_rect = (100, 200, 550, 75)
        dirname = os.path.dirname(__file__)
        self.backround_image = pygame.image.load(
            os.path.join(dirname, "..", "assets", BACKGROUND_IMAGE))
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
        """Palauttaa vaihtoehtokenttiä edustavan listan pygame.Rect() oliota

        Returns:
            lista: lista Rect() oliota
        """
        return self.option_rect_list

    def render(self):
        """Piirtää näkymän
        """
        self._display.blit(self.backround_image, self.backround_rect)

        title_text = self.fonts[0].render("Minesweeper", True, (30, 30, 30))
        self._display.blit(title_text, (60, 60))

        pygame.draw.rect(self._display, (100, 100, 100), self.option_rect_list[0])
        diff_text = self.fonts[1].render("Default difficulties", True, (255, 255, 255))
        self._display.blit(diff_text, (self.option_rect[0] +10, self.option_rect_list[0].y+10))

        pygame.draw.rect(self._display, (100, 100, 100),self.option_rect_list[1])
        custom_text = self.fonts[1].render("Custom difficulty", True, (255, 255, 255))
        self._display.blit(custom_text, (self.option_rect[0] +10, self.option_rect_list[1].y+10))

        pygame.draw.rect(self._display, (100, 100, 100),self.option_rect_list[2])
        leaderboard_text = self.fonts[1].render("Leaderboard", True, (255, 255, 255))
        self._display.blit(leaderboard_text, (self.option_rect[0]+10, self.option_rect_list[2].y+10))

        pygame.display.update()
