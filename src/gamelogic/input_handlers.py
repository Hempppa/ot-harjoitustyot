import time
import pygame

class DefaultLoop:
    """Pohja kaikille input_handlereille. Lukee käyttäjän syöttöjä. Valikko, jossa on rendererin
    määräämä lukema vaihtoehtoisia kenttiä

    Attributes:
        renderer: rendereri joka piirtää näkymän
        event_queue: EventQueue olio, joka hakee pygame.eventtejä
        clock: Clock olio, joka toimii kuin pygame.time.Clock
        rect_list: lista kentistä joilla näkymää käytetään
    """
    def __init__(self, renderer, event_queue, clock):
        """Alustetaan konstruktorilla attribuutit

        Args:
            renderer: rendereri jota käytetään
            event_queue: olio, jolla eventit haetaan
            clock: olio, jolla säädetään pelin fps
        """
        self._renderer = renderer
        self._event_queue = event_queue
        self._clock = clock
        self._rect_list = None

    def set_renderer(self, renderer):
        """Asettaa rendererin ja kenttien tiedot samaksi. Varatoimenpide

        Args:
            renderer: rendereri jota käytetään
        """
        self._renderer = renderer
        self._rect_list = renderer.get_rect_info()

    def start(self):
        """Looppi jolla peli pyörii. Joka kierros käsitellään tapahtumat ja piirretään näkymä.
        Jos tapahtumakäsittelyssä on muu kuin -1 - 5, suoritus jatkuu

        Returns:
            int: (-1, 0, 1, 2, 3, 4, 5)
            -1 pelistä poistuttiin, 5 palataan edelliseen näkymään, 0-4 valittiin jotain
        """
        while True:
            events = self._handle_events()
            if events in range(-1, 6):
                return events
            self._render()
            self._clock.tick(60)

    def _handle_events(self):
        """Hakee event_queuen tapahtumat ja suorittaa perustoiminnallisuuden.
        Pelistä voi poistua ruksista, palata edelliseen näkymään tai valita vaihtoehto kentistä

        Returns:
            int: välillä -1--5, jos hyväksytty syöte, 10 jos suoritusta jatketaan
        """
        for event in self._event_queue.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 5
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return self.check_option_pressed(event.pos)
        return 10

    def check_option_pressed(self, pos):
        """Tarkistaa mitä valikon kenttää on painettu

        Args:
            pos: painalluksen sijainti

        Returns:
            int: vaihtoehdon numeron jos sellaseen osuttiin, 10 jos ei
        """
        for rect in self._rect_list:
            if rect.collidepoint(pos):
                return self._rect_list.index(rect)
        return 10

    def _render(self):
        """Käskee piirtämään näkymän
        """
        self._renderer.render()

class MenuScreen(DefaultLoop):
    """Toimii hetkellä täysin kuin DefaultLoop 
    """

class CustomDifficulty(DefaultLoop):
    """Valikko, jossa on painettavien vaihtoehtojen sijaan kenttiä, joihin voi syöttää numeroita.

    Attributes:
        active: pitää kirjaa mihin kenttään syötetään: 0 jos mikään ei ole >0 muuten
    """
    def __init__(self, renderer, event_queue, clock):
        """Käytännössä sama kui DefaultLoop
        """
        super().__init__(renderer, event_queue, clock)
        self.active = 0

    def start(self):
        """Toimii kuin DefaultLoop, mutta hyväksytään, myös lista vaikeuden asetuksena

        Returns:
            events: -1, 5 tai lista intejä muodossa [x,y,mines]
        """
        while True:
            events = self._handle_events()
            if events in (-1,5) or isinstance(events, list):
                return events
            self._render()
            self._clock.tick(60)

    def _handle_events(self):
        """Erona DefaultLoopiin, kentän painaminen aktivoi sen, enterillä jatketaan,
        jos jokin kenttä on aktiivisena siihen voi kirjoittaa

        Returns:
            events: -1, 5, 10 tai lista intejä muodossa [x,y,mines]
        """
        for event in self._event_queue.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    activated = self.check_option_pressed(event.pos)
                    self._renderer.set_active(activated)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 5
                if event.key == pygame.K_RETURN:
                    return self.set_final_values()
                if self.active == 0:
                    continue
                if event.key == pygame.K_BACKSPACE:
                    shortened = self._rect_list[self.active-1][0][:-1]
                    self._rect_list[self.active-1][0] = shortened
                    self._renderer.set_text(shortened, self.active)
                else:
                    self.set_int_value(event.unicode)
        return 10

    def set_final_values(self):
        """Metodi, jolla tarkistetaan vielä, että miinoja ei ole liikaa ja minimiarvot [1,1,1]

        Returns:
            list: listan intejä muodossa [x,y,mines]
        """
        grid_values = [1,1,1]
        rects = len(self._rect_list )
        for i in range(rects):
            if not (self._rect_list [i][0] == "" or self._rect_list [i][0] == "0"):
                grid_values[i] = int(self._rect_list [i][0])
        if grid_values[2] > grid_values[0]*grid_values[1]:
            grid_values[2] = grid_values[0]*grid_values[1]
        return grid_values

    def set_int_value(self, user_input):
        """Käännetään käyttäjän syöte numeroksi jos mahdollista, päivitetään rendererille

        Args:
            user_input: käyttäjän painama nappi
        """
        try:
            int(user_input)
        except ValueError:
            return
        if self.active == 1:
            limit = 38
        elif self.active == 2:
            limit = 18
        else:
            limit = 684
        new_value = int(self._rect_list [self.active-1][0] + user_input)
        if new_value > limit:
            self._rect_list [self.active-1][0] = str(limit)
            self._renderer.set_text(str(limit), self.active)
        else:
            self._rect_list [self.active-1][0] = str(new_value)
            self._renderer.set_text(str(new_value), self.active)

    def check_option_pressed(self, pos):
        """Toimii samoin kuin DefaultLoop, mutta päivittää tiedon myös rendererille

        Args:
            pos: painalluksen sijainti

        Returns:
            int: painalluksen aktivoima ruutu
        """
        rects = len(self._rect_list )
        clicked = False
        for i in range(rects):
            if self._rect_list [i][2].collidepoint(pos):
                self.active = i+1
                clicked = True
        if not clicked:
            self.active = 0
        return self.active

class LeaderboardInput(CustomDifficulty):
    """Perii CustomDifficultyn, toimii lähes samoin,
    mutta syötekenttiä on yksi ja se ottaa myös tekstiä
    """
    def start(self):
        """mahdollistaa myös merkkijonon palauttamisen

        Returns:
            int or str: -1,5 tai käyttäjän syöttämä nimi
        """
        while True:
            events = self._handle_events()
            if events in (-1,5) or isinstance(events, str):
                return events
            self._render()
            self._clock.tick(60)

    def _handle_events(self):
        """Lähes sama kuin CustomDifficulty, mutta käsitellään myös kirjaimia

        Returns:
            int or str: -1, 5, 10 tai käyttäjänimi
        """
        for event in self._event_queue.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                #print(buttons)
                if event.button == 1:
                    activated = self.check_option_pressed(event.pos)
                    self._renderer.set_active(activated)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 5
                if event.key == pygame.K_RETURN:
                    return self._rect_list[self.active-1][0]
                if self.active == 0:
                    continue
                if event.key == pygame.K_BACKSPACE:
                    shortened = self._rect_list[self.active-1][0][:-1]
                    self._rect_list[self.active-1][0] = shortened
                    self._renderer.set_text(shortened, self.active)
                elif len(self._rect_list[self.active-1][0]) < 8:
                    self._rect_list[self.active-1][0] += event.unicode
                    self._renderer.set_text(self._rect_list[self.active-1][0], self.active)
        return 10

class GameLoop(DefaultLoop):
    """Pelin sisällä syötteiden lukemiseen

    Attributes:
        level: kenttä, josta poistetaan ja johon lisätään Spritejä
    """
    def __init__(self, level, renderer, event_queue, clock):
        """DefaultLoop, mutta asetetaan myös leveli

        Args:
            level: kenttä johon tehdään muutoksia
        """
        self._level = level
        super().__init__(renderer, event_queue, clock)

    def set_renderer(self, renderer):
        """Samalla kun asetetaan rendereri varman päälle,
        niin otetaan myös rendererin leveli käyttöön

        Args:
            renderer: rendereri (ja sen leveli) jota käytetään
        """
        self._renderer = renderer
        self._level = self._renderer.get_level()

    def start(self):
        """DefaultLoop, mutta vahinkojen estämiseksi ei voida palata edelliseen näkymään,
        myöskin otetaan aikaa joka pelaamiseen kestää

        Returns:
            int: -1, 0 tai 1: -1 pelistä poistuttiin, 0 peli hävittiin, 1 peli voitettiin 
        """
        start_time = time.time()
        while True:
            events = self._handle_events()
            if events in (-1, 0, 1):
                end_time = time.time()
                return events, (end_time-start_time)
            self._render()
            self._clock.tick(60)

    def _handle_events(self):
        """Käsittelee pelin tapahtumia, pelistä voi poistua ruksista tai avata tai liputtaa ruutuja

        Returns:
            int: -1, 0 ja 1, kuvaavat pelin lopetustilannetta, 10 peli jatkuu
        """
        for event in self._event_queue.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_situation = self._level.cell_clicked(event.button, event.pos)
                if game_situation in (1, 0):
                    self._render()
                    return game_situation
        return 10
