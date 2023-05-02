import os
import pygame
from config import BACKGROUND_IMAGE

class LBRenderer:
    """Piirtää itse tulostaulun, tästä voi vain palata tai poistua pelistä

    Attributes:
        _display: ikkuna johon näkymä piirretään
        fonts: lista pygame.font.Font():eista joita näkymä käyttää
        option_rect: kenttien vakio sijainti
        backround_image: taustakuva, ladataan assets kansiosta config.py BACKGROUND_IMAGE muuttujan nimellä
        scores: näytettävät tulokset
    """
    def __init__(self, display, diff, repo):
        """Alustaa attribuutteja, lataa myös tietokannasta tulokset

        Args:
            display: ikkuna johon näkymä piirretään
            diff: vaikeustaso jolla tulokset haetaan
            repo: Luokka jolla tietokannasta haetaan
        """
        self._display = display
        if pygame.display.get_window_size() != (750,750):
            pygame.display.set_mode((750,750))
        self.fonts = [pygame.font.Font(None, 140), pygame.font.Font(None, 50), pygame.font.Font(None, 60)]
        dirname = os.path.dirname(__file__)
        self.backround_image = pygame.image.load(
            os.path.join(dirname, "..", "assets", BACKGROUND_IMAGE))
        self.backround_rect = self.backround_image.get_rect()
        self.option_rect = (100, 210, 550, 75)
        self.scores = repo.get_scores(diff)

    def get_rect_info(self):
        """Toiminnallisuus jota input_handleri vaatii, tyhjä koska ei ole vaihtoehtoja

        Returns:
            list: tyhjä lista
        """
        return []

    def render(self):
        """Piirtää näkymän
        """
        self._display.blit(self.backround_image, self.backround_rect)

        esc_text = self.fonts[2].render("Esc to return", True, (10, 10, 10))
        self._display.blit(esc_text, (10, 10))

        title_text = self.fonts[0].render("Minesweeper", True, (60, 60, 60))
        self._display.blit(title_text, (60, 60))

        base_rect = pygame.Rect(self.option_rect[0], self.option_rect[1]-20, 550, 450)
        pygame.draw.rect(self._display, (100, 100, 100), base_rect)
        pygame.draw.line(self._display, (30, 30, 30), (100, 190), (650, 190), 3)
        pygame.draw.line(self._display, (30, 30, 30), (100, 190), (100, 240), 3)
        pygame.draw.line(self._display, (30, 30, 30), (650, 190), (650, 240), 3)
        pygame.draw.line(self._display, (30, 30, 30), (100, 240), (650, 240), 3)
        score_text = self.fonts[1].render(f"Username  |  Difficulty  |  Time", True, (255, 255, 255))
        self._display.blit(score_text, (self.option_rect[0]+10, self.option_rect[1]-10))

        for i in range(len(self.scores)):
            score = self.scores[i]
            text = f"{score[0]:5}{score[1]:10}{float(score[2]):.2f}"
            #print(text)
            username_text = self.fonts[1].render(score[0], True, (255, 255, 255))
            self._display.blit(username_text, (self.option_rect[0]+10, self.option_rect[1]+(i+1)*(40)))

            diff_text = self.fonts[1].render(score[1], True, (255, 255, 255))
            self._display.blit(diff_text, (self.option_rect[0]+230, self.option_rect[1]+(i+1)*(40)))
        
            time_text = self.fonts[1].render(f"{float(score[2]):.2f}", True, (255, 255, 255))
            self._display.blit(time_text, (self.option_rect[0]+430, self.option_rect[1]+(i+1)*(40)))

        pygame.display.update()
