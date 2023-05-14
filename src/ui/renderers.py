import os
import pygame
from config import BACKGROUND_IMAGE

class MenuRenderer:
    """Piirtä alkunäkymän. Näkymässä on kolme vaihtoehtokenttää.

    Attributes:
        _display: ikkuna johon näkymä piirretään
        draw_object_list: lista näkymän osista jotka voi piirtää .blit() metodilla
        draw_rect_list: lista piirrettäviä pygame.Rect() oliota
        fonts: lista pygame.font.Font():eista joita näkymät käyttävät
        option_rect: kenttien vakio sijainti, jotta näytä voi siirtää yhdessä
    """
    def __init__(self, display, rect=(100,200,550,75), rect_colour=(100,100,100)):
        """Konstruktori, lataa taustakuvan ja alustaa joitain kaikille yhteisiä osia

        Args:
            display: pygame.display ikkuna johon näkymä piirretään
            rect: Vakio vaihtoehtokenttien arvot, jonka pohjalta kentät luodaan. Defaults to (100,200,550,75).
            rect_colour: Väri joilla vakiokentät piirretään. Defaults to (100,100,100).
        """
        self._display = display
        self.draw_object_list = []
        self.draw_rect_list = []
        self.fonts = [pygame.font.Font(None, 140), pygame.font.Font(None, 70), pygame.font.Font(None, 60), pygame.font.Font(None, 50)]
        dirname = os.path.dirname(__file__)
        backround_image = pygame.image.load(
            os.path.join(dirname, "..", "assets", BACKGROUND_IMAGE))
        backround_rect = backround_image.get_rect()
        self.draw_object_list.append([backround_image, backround_rect])
        self.option_rect = rect
        left = rect[0]
        top = rect[1]
        width = rect[2]
        height = rect[3]
        option_text_list = self.get_option_texts()
        for i in range(len(option_text_list)):
            self.draw_rect_list.append([pygame.Rect((left, top, width, height)), rect_colour])
            self.draw_object_list.append([option_text_list[i], (left+10, top+10)])
            top += 100
        self.draw_object_list.append([self.fonts[0].render("Minesweeper", True, (30, 30, 30)), (60, 60)])

    def get_option_texts(self):
        """Luo ja lisää listoihin näkymäkohtaisia objekteja

        Returns:
            list: Tämän listan tekstien pohjalle luodaan vaihtoehtokentät
        """
        texts = [self.fonts[1].render("Default difficulties", True, (255, 255, 255)),
                 self.fonts[1].render("Custom difficulty", True, (255, 255, 255)),
                 self.fonts[1].render("Leaderboard", True, (255, 255, 255))]
        return texts

    def get_rect_info(self):
        """Palauttaa vaihtoehtokenttiä edustavan listan pygame.Rect() oliota

        Returns:
            lista: lista Rect() oliota
        """
        return [rect[0] for rect in self.draw_rect_list]

    def render(self, scores=[]):
        """Piirtää näkymän listojen sisältöjen pohjalta

        Args:
            scores (list, optional): draw_object_list lisättävä, mutta erillinen osa. Hetkellä vain LB näkymän tulokset. Defaults to [].
        """
        if pygame.display.get_window_size() != (750,750):
            pygame.display.set_mode((750,750))

        self._display.blit(self.draw_object_list[0][0], self.draw_object_list[0][1])

        for rect, colour in self.draw_rect_list:
            pygame.draw.rect(self._display, colour, rect)

        for object, parameter in self.draw_object_list[1:]+scores:
            self._display.blit(object, parameter)

        pygame.display.update()

class DiffRenderer(MenuRenderer):
    """Piirtää "default difficulties" näkymän. Valikossa on kolme vaihtoehtoa, Lähes sama kuin MenuRenderer
    """
    def __init__(self, display, rect=(100, 200, 550, 75), rect_colour=(50,50,50)):
        """Sama kuin MenuRenderer, mutta Esc to return teksti.
        """
        super().__init__(display, rect, rect_colour)
        self.draw_object_list.append([self.fonts[2].render("Esc to return", True, (10, 10, 10)), (10, 10)])

    def get_option_texts(self):
        """Sama kuin MenuRenderer luokan, mutta eri tekstit
        """
        texts = [self.fonts[1].render("Easy:       9x9/9", True, (255, 255, 255)),
                 self.fonts[1].render("Medium:  16x16/30", True, (255, 255, 255)),
                 self.fonts[1].render("Hard:       30x16/70", True, (255, 255, 255))]
        return texts

class LBSelectionRenderer(DiffRenderer):
    """Piirtää "leaderboard" näkymän, tästä voi valita minkä vaikeustason tuloksia halutaan nähdä. Neljä vaihtoehtokenttää.
    """
    def get_option_texts(self):
        """Sama kuin DiffRenderer, mutta eri tekstit ja yksi vaihtoehto lisää
        """
        texts = [self.fonts[1].render("All Scores", True, (255, 255, 255)),
                 self.fonts[1].render("Easy Scores", True, (255, 255, 255)),
                 self.fonts[1].render("Medium Scores", True, (255, 255, 255)),
                 self.fonts[1].render("Hard Scores", True, (255, 255, 255))]
        return texts
    

class LBRenderer(DiffRenderer):
    """Piirtää itse tulostaulun, tästä voi vain palata tai poistua pelistä. Ei vaihtoehtokenttiä

    Attributes:
        repo: Repository luokka josta tulokset haetaan
        score_list: Lista haetuista tuloksista
    """
    def __init__(self, display, repo, rect=(100, 210, 550, 75)):
        """Sama kuin DiffRenderer, mutta MenuRenderer render() metodissa mainitsemat tulokset.

        Args:
            display (_type_): _description_
            repo: Luokka josta .get_scores(diff) metodilla haetaan halutut tulokset
            rect: Vakio kenttä, mutta tällä kertaa tulostaulun taustalle. Defaults to (100, 210, 550, 75).
        """
        super().__init__(display, rect)
        self.repo = repo
        self.score_list = []
        self.set_scores(0)

    def get_option_texts(self):
        """Lisää listoihin näkymän osat, eli tulostaulun

        Returns:
            texts: palauttaa tyhjän, koska ei ole vaihtoehtokenttiä
        """
        self.draw_object_list.append([self.fonts[3].render(f"Username  |  Difficulty  |  Time", True, (255, 255, 255)), (self.option_rect[0]+10, self.option_rect[1]-10)])
        self.draw_rect_list.append([pygame.Rect(self.option_rect[0], self.option_rect[1]-20, self.option_rect[2], self.option_rect[3]+400), (100, 100, 100)])
        self.draw_rect_list.append([pygame.Rect(self.option_rect[0], self.option_rect[1]-20, self.option_rect[2], self.option_rect[3]-25), (30, 30, 30)])
        self.draw_rect_list.append([pygame.Rect(self.option_rect[0]+2, self.option_rect[1]-18, self.option_rect[2]-4, self.option_rect[3]-29), (100, 100, 100)])
        texts = []
        return texts
    
    def set_scores(self, diff):
        """Hakee self.reposta diff vaikeustason mukaiset tulokset ja lisää listaan

        Args:
            diff: vaikeustaso, jonka tulokset tulostaulun kuuluu näyttää
        """
        self.score_list = []
        scores = self.repo.get_scores(diff)
        for i in range(len(scores)):
            score = scores[i]
            self.score_list.append([self.fonts[3].render(score[0], True, (255, 255, 255)), (self.option_rect[0]+10, self.option_rect[1]+(i+1)*(40))])
            self.score_list.append([self.fonts[3].render(str(score[1]), True, (255, 255, 255)), (self.option_rect[0]+230, self.option_rect[1]+(i+1)*(40))])
            self.score_list.append([self.fonts[3].render(f"{score[2]:.2f}", True, (255, 255, 255)), (self.option_rect[0]+430, self.option_rect[1]+(i+1)*(40))])

    def render(self):
        """Muuten sama kuin DiffRender, mutta lisää listan tuloksista
        """
        super().render(self.score_list)


class LevelRenderer:
    """Piirtää varsinaisen pelinäkymän

    Attributes:
        _display: ikkuna johon näkymä piirretään
        _level: Level Luokan olio, joka sisältää kaikki piirrettävät Spritet
    """
    def __init__(self, display, level=None):
        """Vain levelin Spritet ja display tarvitaan

        Args:
            display: ikkuna johon näkymä piirretään
            level: Level olio
        """
        self._display = display
        self._level = level

    def set_level(self, level, size):
        """Asettaa näkymän koon ja halutun levelin

        Args:
            level: rendererin käyttämä Level olio
            size: näkymän koko
        """
        pygame.display.set_mode(size)
        self._level = level

    def get_level(self):
        """input_handleri set_rendererin mukana pyytää leveliä johon muutokset tehdään

        Returns:
            level: palauttaa rendererin käyttämän levelin
        """
        return self._level

    def render(self):
        """Piirtää display ikkunaan kaikki levelin spritet
        """
        self._level.all_cells.draw(self._display)
        self._level.cell_covers.draw(self._display)
        self._level.flags.draw(self._display)
        pygame.display.update()

class CustomRenderer(DiffRenderer):
    """Piirtää "custom difficulties" näkymän, tässä on kolme kenttää johon voi syöttää numeroita vaikeuden asettamiseen.

    Attributes:
        width_info: leveyden määrävän kentän tiedot, muodossa [teksti, aktiivitila, sijainti]
        height_info: korkeuden määräävän kentän tiedot
        mines_info: miinojen lkm määräävän kentän tiedot
        colours: värit joilla kentät piirretään
    """
    def __init__(self, display, rect=(70, 200, 200, 75)):
        """Sama kuin DiffRenderer, mutta info kentät ja kenttien värit, koska tätä kutsutaan vain kerran, kenttien arvot säilyvät
        """
        super().__init__(display, rect)
        self.width_info = ["16", False, (rect[0], rect[1]+50, rect[2], rect[3])]
        self.height_info = ["16", False, (rect[0]+310, rect[1]+50, rect[2], rect[3])]
        self.mines_info = ["30", False, (rect[0], rect[1]+250, rect[2]*2, rect[3])]
        self.colours = [(10,10,10), (30,30,50)]

    def get_option_texts(self):
        """Sama kuin aina, luodaan kentät, tekstit niiden sisään ja ylle, sekä "enter to start"

        Returns:
            list: tyhjä lista, koska muuten vaihtoehdot piirrettäisiin kuin muissa näkymissä
        """
        self.draw_object_list.append([self.fonts[1].render("16", True, (255, 255, 255)), (self.option_rect[0]+10, self.option_rect[1]+60)])
        self.draw_object_list.append([self.fonts[1].render("16", True, (255, 255, 255)), (self.option_rect[0]+320, self.option_rect[1]+60)])
        self.draw_object_list.append([self.fonts[1].render("30", True, (255, 255, 255)), (self.option_rect[0]+10, self.option_rect[1]+260)])
        self.draw_object_list.append([self.fonts[3].render("Width (1-38):", True, (255, 255, 255)), (self.option_rect[0], self.option_rect[1]+10)])
        self.draw_object_list.append([self.fonts[3].render("Height (1-18):", True, (255, 255, 255)), (self.option_rect[0]+310, self.option_rect[1]+10)])
        self.draw_object_list.append([self.fonts[3].render("Mines (1-684):", True, (255, 255, 255)), (self.option_rect[0], self.option_rect[1]+210)])
        self.draw_object_list.append([self.fonts[0].render("Enter to start", True, (10,10,10)), (70, 600)])
        self.draw_object_list.append([self.fonts[0].render("Enter to start", True, (255,255,255)), (68, 598)])
        self.draw_rect_list.append([pygame.Rect(self.option_rect[0], self.option_rect[1]+50, self.option_rect[2], self.option_rect[3]), (10, 10, 10)])
        self.draw_rect_list.append([pygame.Rect(self.option_rect[0]+310, self.option_rect[1]+50, self.option_rect[2], self.option_rect[3]), (10, 10, 10)])
        self.draw_rect_list.append([pygame.Rect(self.option_rect[0], self.option_rect[1]+250, self.option_rect[2]*2, self.option_rect[3]), (10, 10, 10)])
        texts = []
        return texts

    def set_text(self, text, which):
        """Päivittää haluttuun kenttään uuden numeron, jos se on aktiivinen

        Args:
            text: uusi numero
            which: mihin kenttään numero päivitetään
        """
        if which == 1 and self.width_info[1]:
            self.width_info[0] = text
            self.draw_object_list[1][0] = self.fonts[1].render(text, True, (255, 255, 255))
        elif which == 2 and self.height_info[1]:
            self.height_info[0] = text
            self.draw_object_list[2][0] = self.fonts[1].render(text, True, (255, 255, 255))
        elif which == 3 and self.mines_info[1]:
            self.mines_info[0] = text
            self.draw_object_list[3][0] = self.fonts[1].render(text, True, (255, 255, 255))

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
        """Sama kuin DiffRendererin, mutta muuttaa ensin kenttien värit infojen mukaiseksi
        """
        rect_info = self.get_rect_info()
        for i in range(len(rect_info)):
            if rect_info[i][1]:
                self.draw_rect_list[i][1] = self.colours[1]
            else:
                self.draw_rect_list[i][1] = self.colours[0]
        super().render()

class LBInputRenderer(CustomRenderer):
    """Piirtää voittoruudun, tässä on kenttä johon käyttäjä syöttää nimen. Sama kuin CustomRenderer, ainoastaan kenttiä on yksi.

    Attributes:
        time: aika joka pelissä kesti
        username_info: Toimii samoin kuin CustomRendererin infot
    """
    def __init__(self, display, rect=(70, 450, 400, 75)):
        """Miltein sama kuin CustomRendereri, infoja on vain yksi ja time
        """
        self.time = 0
        super().__init__(display, rect)
        self.username_info = ["", False, rect]

    def get_option_texts(self):
        """Lisätään listoihin kenttä, sen teksti, aika ja enter to continue

        Returns:
            list: tyhjä, jotta kenttä piirrettäisiin eri tavalla kuin muut
        """
        self.draw_object_list.append([self.fonts[2].render("", True, (255, 255, 255)), (self.option_rect[0]+10, self.option_rect[1]+10)])
        self.draw_object_list.append([self.fonts[2].render("Username (max 8 char):", True, (200, 200, 200)), (self.option_rect[0], self.option_rect[1]-50)])
        self.draw_object_list.append([self.fonts[1].render(f"Time: {self.time:.2f}s", True, (200, 200, 200)), (self.option_rect[0], self.option_rect[1]-150)])
        self.draw_object_list.append([self.fonts[1].render("Enter to continue", True, (10,10,10)), (70, 600)])
        self.draw_object_list.append([self.fonts[1].render("Enter to continue", True, (255,255,255)), (68, 598)])
        self.draw_rect_list.append([pygame.Rect(self.option_rect[0], self.option_rect[1], self.option_rect[2], self.option_rect[3]), (10, 10, 10)])
        texts = []
        return texts
    
    def set_time(self, time):
        """Päivittää pelissä kestäneen ajan

        Args:
            time: pelissä kestänyt aika
        """
        self.time = time
        self.draw_object_list[3][0] = self.fonts[1].render(f"Time: {self.time:.2f}s", True, (200, 200, 200))

    def set_text(self, text, which):
        """Päivittää nimen kenttään jos se on aktiivinen

        Args:
            text: päivitetty nimi
            which: kenttä jota päivitetään
        """
        if which == 1 and self.username_info[1]:
            self.username_info[0] = text
            self.draw_object_list[1][0] = self.fonts[2].render(text, True, (255, 255, 255))

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