import os
import pygame
from config import BACKGROUND_IMAGE

class CustomRenderer:
    """Piirtää "custom difficulties" näkymän, tässä on kolme kenttää johon voi syöttää numeroita vaikeuden asettamiseen

    Attributes:
        _display: ikkuna johon näkymä piirretään
        fonts: lista pygame.font.Font():eista joita näkymä käyttää
        rect: kenttien vakio koko
        backround_image: taustakuva, ladataan assets kansiosta config.py BACKGROUND_IMAGE muuttujan nimellä
        width_info: leveyden määrävän kentän tiedot, muodossa [teksti, aktiivitila, sijainti]
        height_info: korkeuden määräävän kentän tiedot
        mines_info: miinojen lkm määräävän kentän tiedot
        colours: lista joistain näkymän käyttämistä väreistä
    """
    def __init__(self, display, difficulty):
        """Alustaa tiedot, jotka piirretään myöhemmin

        Args:
            display: ikkuna johon näkymä piirretään
            difficulty: vaikeus johon näkymä alussa defaultoituu
        """
        self._display = display
        if pygame.display.get_window_size() != (750,750):
            pygame.display.set_mode((750,750))
        self.fonts = [pygame.font.Font(None, 140), pygame.font.Font(None, 60), pygame.font.Font(None, 70)]
        self.rect = (200, 75)
        dirname = os.path.dirname(__file__)
        self.backround_image = pygame.image.load(
            os.path.join(dirname, "..", "assets", BACKGROUND_IMAGE))
        self.width_info = [str(difficulty[0]), False, (70, 250, self.rect[0], self.rect[1])]
        self.height_info = [str(difficulty[1]), False, (380, 250, self.rect[0], self.rect[1])]
        self.mines_info = [str(difficulty[2]), False, (70, 450, self.rect[0]*2, self.rect[1])]
        self.colours = [(10,10,10), (30,30,50)]

    def set_text(self, text, which):
        """Päivittää input kenttään uuden numeron, jos 

        Args:
            text: uusi numero
            which: mihin kenttään numero päivitetään
        """
        if which == 1 and self.width_info[1]:
            self.width_info[0] = text
        elif which == 2 and self.height_info[1]:
            self.height_info[0] = text
        elif which == 3 and self.mines_info[1]:
            self.mines_info[0] = text

    def set_active(self, which):
        """Asettaa määrätyn ruudun aktiiviseksi, tärkeätä jotta tietää mitä kenttää päivittää ja vaihtaa kentän väriä

        Args:
            which: mikä kenttä aktivoidaan
        """
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
        """Asettaessa renderin (set_renderer()) input_handleri kysyy kenttien sijainnit, jotta hiiren painalluksen voi tunnistaa

        Returns:
            list: lista kaikista kentistä, kentät esitetään listana jossa on teksti, aktiivitila ja sijainti
        """
        info = []
        info.append([self.width_info[0], self.width_info[1], pygame.Rect(self.width_info[2])])
        info.append([self.height_info[0], self.height_info[1], pygame.Rect(self.height_info[2])])
        info.append([self.mines_info[0], self.mines_info[1], pygame.Rect(self.mines_info[2])])
        return info

    def render(self):
        """Piirtää varsinaisen näkymän käyttäen tietojaan
        """
        backround_rect = self.backround_image.get_rect()
        self._display.blit(self.backround_image, backround_rect)
        
        esc_text = self.fonts[1].render("Esc to return", True, (10, 10, 10))
        self._display.blit(esc_text, (10, 10))

        title_text = self.fonts[0].render("Minesweeper", True, (60, 60, 60))
        self._display.blit(title_text, (60, 60))

        width_text = self.fonts[1].render("Width (1-38):", True, (255, 255, 255))
        self._display.blit(width_text, (70, 200))
        if self.width_info[1]:
            pygame.draw.rect(self._display, self.colours[1], self.width_info[2])
        else:
            pygame.draw.rect(self._display, self.colours[0], self.width_info[2])
        width_value = self.fonts[2].render(self.width_info[0], True, (200, 200, 200))
        self._display.blit(width_value, (80, 260))

        height_text = self.fonts[1].render("Height (1-18):", True, (255, 255, 255))
        self._display.blit(height_text, (380, 200))
        if self.height_info[1]:
            pygame.draw.rect(self._display, self.colours[1], self.height_info[2])
        else:
            pygame.draw.rect(self._display, self.colours[0], self.height_info[2])
        height_value = self.fonts[2].render(self.height_info[0], True, (200, 200, 200))
        self._display.blit(height_value, (390, 260))

        mines_text = self.fonts[1].render("Mines (1-684):", True, (255, 255, 255))
        self._display.blit(mines_text, (70, 400))
        if self.mines_info[1]:
            pygame.draw.rect(self._display, self.colours[1], self.mines_info[2])
        else:
            pygame.draw.rect(self._display, self.colours[0], self.mines_info[2])
        mines_value = self.fonts[2].render(self.mines_info[0], True, (200, 200, 200))
        self._display.blit(mines_value, (80, 460))

        start_text = self.fonts[0].render("Enter to start", True, (10,10,10))
        self._display.blit(start_text, (70, 600))
        start_text = self.fonts[0].render("Enter to start", True, (255,255,255))
        self._display.blit(start_text, (68, 598))

        pygame.display.update()
