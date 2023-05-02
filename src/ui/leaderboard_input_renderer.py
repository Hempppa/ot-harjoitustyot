import os
import pygame
from config import BACKGROUND_IMAGE

class LBInputRenderer:
    """Piirtää voittoruudun, tässä on kenttä johon käyttäjä syöttää nimen

    Attributes:
        _display: ikkuna johon näkymä piirretään
        fonts: lista pygame.font.Font():eista joita näkymä käyttää
        rect: kenttien vakio koko
        time: aika joka pelaajalla kesti
        backround_image: taustakuva, ladataan assets kansiosta config.py BACKGROUND_IMAGE muuttujan nimellä
        username_info: nimen määrävän kentän tiedot, muodossa [teksti, aktiivitila, sijainti]
        colours: lista joistain näkymän käyttämistä väreistä
    """
    def __init__(self, display, time):
        """Alustaa attribuutteja, joita piirretään näkymään

        Args:
            display: ikkuna johon näkymä piirretään
            time: aika joka pelaajalla kesti, ilmoitetaan pelaajalle
        """
        self._display = display
        if pygame.display.get_window_size() != (750,750):
            pygame.display.set_mode((750,750))
        self.fonts = [pygame.font.Font(None, 140), pygame.font.Font(None, 60)]
        self.rect = (200, 75)
        self.time = time
        dirname = os.path.dirname(__file__)
        self.backround_image = pygame.image.load(
            os.path.join(dirname, "..", "assets", BACKGROUND_IMAGE))
        self.username_info = ["", False, (70, 450, self.rect[0]*2, self.rect[1])]
        self.colours = [(10,10,10), (30,30,50)]

    def set_text(self, text, which):
        """Päivittää nimen kenttään jos se on aktiivinen

        Args:
            text: päivitetty nimi
            which: jämä input_handlerista
        """
        if which == 1 and self.username_info[1]:
            self.username_info[0] = text

    def set_active(self, which):
        """Asettaa määrätyn kentän aktiiviseksi

        Args:
            which: kenttä joka asetetaan
        """
        if which == 1:
            self.username_info[1] = True
        else:
            self.username_info[1] = False

    def get_rect_info(self):
        """Palauttaa nimikentän tiedot

        Returns:
            list: lista nimikentän tiedoista, muodossa [nimi, aktiivisuus, sijainti]
        """
        info = []
        info.append([self.username_info[0], self.username_info[1], pygame.Rect(self.username_info[2])])
        return info

    def render(self):
        """Piirtää varsinaisen näkymän
        """
        backround_rect = self.backround_image.get_rect()
        self._display.blit(self.backround_image, backround_rect)

        esc_text = self.fonts[1].render("Esc to return", True, (10, 10, 10))
        self._display.blit(esc_text, (10, 10))

        title_text = self.fonts[0].render("Minesweeper", True, (60, 60, 60))
        self._display.blit(title_text, (60, 60))

        username_text = self.fonts[1].render(f"Time: {self.time:.2f}s", True, (200, 200, 200))
        self._display.blit(username_text, (70, 300))

        username_text = self.fonts[1].render("Username (max 8 char):", True, (200, 200, 200))
        self._display.blit(username_text, (70, 400))
        if self.username_info[1]:
            pygame.draw.rect(self._display, self.colours[1], self.username_info[2])
        else:
            pygame.draw.rect(self._display, self.colours[0], self.username_info[2])
        username_value = self.fonts[1].render(self.username_info[0], True, (200, 200, 200))
        self._display.blit(username_value, (80, 460))

        start_text = self.fonts[1].render("Enter to continue", True, (10,10,10))
        self._display.blit(start_text, (70, 600))
        start_text = self.fonts[1].render("Enter to continue", True, (255,255,255))
        self._display.blit(start_text, (68, 598))

        pygame.display.update()
