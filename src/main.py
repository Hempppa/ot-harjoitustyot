import pygame
from levelgeneration.map_generator import MapGen
from levelgeneration.level import Level

CELL_SIZE = 50
EASY_DIFF = (9,9,9)
MEDIUM_DIFF = (16,16,30)
HARD_DIFF = (30,16,70)

class GameFrame():
    """Sovelluksen runko. Tämä luokka hoitaa siirtymisen sovelluksen näkymien välillä 
       ja tallentaa tietokantaan suorituksia

    Attributes:
        renderers: rendererit, joita input_handlereille annetaan
        menu_screen: Luokka, joka toteuttaa valikon, jossa on renderin määräämät vaihtoehdot
        game_loop: Luokka, joka toteuttaa Level olion mukaisen pelin
        custom_menu: Luokka, joka toteuttaa "cutom difficulties" näkymän
        leaderboard_input: Luokka, joka toteuttaa pelin voittoruudun
        leaderboard_repository: Luokka, joka tallentaa ja lukee tietokantaa
    """
    def __init__(self, input_handlers, renderers, leaderboard_repo):
        """Tallennetaan annetut tiedot. input_handlerit erikseen selvyyden vuoksi,
        rendereitä on liikaa tähän

        Args:
            input_handlers: Luokat jotka lukevat syötteitä
            renderers: Luokat jotka määräävät näkymän
            leaderboard_repo: Luokka joka tallentaa ja lukee tietokantaa
        """
        self.renderers = renderers

        self.menu_screen = input_handlers[0]
        self.game_loop = input_handlers[1]
        self.custom_menu = input_handlers[2]
        self.leaderboard_input = input_handlers[3]

        self.leaderboard_repository = leaderboard_repo

    def menu(self):
        """Aloittaa sovelluksen toteutuksen, tästä poistuessa peli suljetaan
        """
        while True:
            option_select = self.enter_start_menu()
            if option_select == -1:
                break
            if option_select in (0,1):
                selected = self.selected_difficulties(option_select)
                if selected == -1:
                    break
                if selected == 5:
                    continue
                (grid_x, grid_y, mines) = selected
            elif option_select == 2:
                return_case = self.leaderboard_selection()
                if return_case == -1:
                    break
                continue
            end_condition = self.start_game_loop(grid_x, grid_y, mines)
            if end_condition == -1:
                break

    def enter_start_menu(self):
        """Pelin alkunäkymä

        Returns:
            selected: palautus on joku int (-1,0,1,2,5). 
                      -1 on ruksin painallus, 5 on esc ja 0-2 on valikon vaihtoehdot
        """
        while True:
            self.menu_screen.set_renderer(self.renderers[0])
            selected = self.menu_screen.start()
            if selected == 5:
                continue
            return selected

    def selected_difficulties(self, selection):
        """Seuraava vaihe pelin käynnistyksessä, tässä valitaan vaikeus. 

        Args:
            selection int: joko 0 tai 1, 0 on vakiovaikeus ja 1 custom

        Returns:
            selected tuple(x,y,mines): palauttaa tässä muodossa kentän koon ja miinojen määrän
        """
        if selection == 0:
            self.menu_screen.set_renderer(self.renderers[2])
            diff = self.menu_screen.start()
            selected = MEDIUM_DIFF
            if diff in (-1,5):
                return diff
            if diff == 0:
                # easy
                selected = EASY_DIFF
            elif diff == 1:
                # medium
                selected = MEDIUM_DIFF
            elif diff == 2:
                # hard
                selected = HARD_DIFF
        elif selection == 1:
            self.renderers[3].set_active(0)
            self.custom_menu.set_renderer(self.renderers[3])
            selected = self.custom_menu.start()
        return selected

    def start_game_loop(self, grid_x, grid_y, mines):
        """selected_difficulties jälkeinen luokka, luodaan haluttu kartta ja siirrytään pelin
        toteutukseen jos vaikeus saatiin valittua. Jos peli päättyy voittoon, tulos tallennetaan
        tietokantaan

        Args:
            grid_x int: leveys 1-38 ruutua
            grid_y int: korkeus 1-18 ruutua
            mines int: miinoja 1-684, kuitenkin < grid_x*gird_y

        Returns:
            int: -1 tai 5, -1 poistuu pelistä ja 5 palaa alkunäkymään
        """
        mine_field = MapGen(grid_x, grid_y, mines)
        level = Level(mine_field.field, CELL_SIZE)

        self.renderers[1].set_level(level, (grid_x*CELL_SIZE, grid_y*CELL_SIZE))
        self.game_loop.set_renderer(self.renderers[1])

        end_condition = self.game_loop.start()
        if end_condition[0] == -1:
            return -1
        if end_condition[0] == 0:
            pygame.time.wait(3000)
        elif end_condition[0] == 1:
            pygame.time.wait(1000)
            is_saved = self.save_game_score((grid_x,grid_y,mines), end_condition[1])
            if is_saved in (-1,5):
                return is_saved
            return self.enter_leaderboard(is_saved)
        return 5

    def save_game_score(self, difficulty, time):
        """Luetaan käyttäjänimi ja tallennetaan tiedot tietokantaan

        Args:
            difficulty: voitetun pelin vaikeustaso
            time: peliin kulunut aika

        Returns:
            mahdollisia (-1,0,1,2,3,5):
                -1 poistutaan pelistä, 5 poistutaan alkunäkymään, 0-3 tallennettiin tulos
        """
        self.renderers[6].set_active(0)
        self.renderers[6].set_time(time)
        self.leaderboard_input.set_renderer(self.renderers[6])
        username = self.leaderboard_input.start()
        if username in (-1,5):
            return username
        if difficulty == EASY_DIFF:
            diff = "Easy", 1
        elif difficulty == MEDIUM_DIFF:
            diff = "Medium", 2
        elif difficulty == HARD_DIFF:
            diff = "Hard", 3
        else:
            diff = "Custom", 0
        self.leaderboard_repository.add_score(username, diff[0], time)
        return diff[1]

    def leaderboard_selection(self):
        """Alkunäkymästä voi myös siirtyä katsomaan tulostaulua,
        ensin valitaan kuitenkin mitkä tulokset näytetään

        Returns:
            int: -1 tai 5, -1 poistutaan pelistä, 5 palataan alkunäkymään
        """
        while True:
            self.menu_screen.set_renderer(self.renderers[5])
            select = self.menu_screen.start()
            if select in (-1,5):
                return select
            returnal = self.enter_leaderboard(select)
            if returnal == 5:
                continue
            return -1

    def enter_leaderboard(self, difficulty):
        """Siirrytään difficultyn osoittamana tulostauluun

        Args:
            difficulty: vaikeustaso, jonka tulokset näytetään

        Returns:
            int: -1 tai 5, -1 poistutaan pelistä, 5 palataan edelliseen näkymään
        """
        if difficulty == 1:
            diff = "Easy"
        elif difficulty == 2:
            diff = "Medium"
        elif difficulty == 3:
            diff = "Hard"
        else:
            diff = "Custom"
        self.renderers[4].set_scores(diff)
        self.menu_screen.set_renderer(self.renderers[4])
        return self.menu_screen.start()
