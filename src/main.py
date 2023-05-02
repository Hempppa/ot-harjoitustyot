import pygame
from levelgeneration.map_generator import MapGen
from levelgeneration.level import Level
from gamelogic.input_handlers import GameLoop, MenuScreen, CustomDifficulty
from gamelogic.input_handlers import LeaderboardInput
from gamelogic.event_queue import EventQueue
from gamelogic.clock import Clock
from repository.leaderboard_repository import LeaderboardRepository
import database_connection

from ui.level_renderer import LevelRenderer
from ui.menu_renderer import MenuRenderer
from ui.difficulty_menu_renderer import DiffRenderer
from ui.custom_menu_renderer import CustomRenderer
from ui.leaderboard_input_renderer import LBInputRenderer
from ui.leaderboard_selection_renderer import LBSelectionRenderer
from ui.leaderboard_renderer import LBRenderer

CELL_SIZE = 50
EASY_DIFF = (9,9,9)
MEDIUM_DIFF = (16,16,30)
HARD_DIFF = (30,16,70)

class GameFrame():
    """Sovelluksen runko. Tämä luokka hoitaa siirtymisen sovelluksen näkymien välillä 
       ja tallentaa tietokantaan suorituksia

    Attributes:
        menu_screen: Luokka, joka toteuttaa valikon, jossa on renderin määräämät vaihtoehdot
        game_loop: Luokka, joka toteuttaa Level olion mukaisen pelin
        custom_menu: Luokka, joka toteuttaa "cutom difficulties" näkymän
        leaderboard_input: Luokka, joka toteuttaa pelin voittoruudun
        leaderboard_repository: Luokka, joka tallentaa ja lukee tietokantaa
    """
    def __init__(self):
        """Alustaa pelin toteutukseen tarvittavat luokat ja pygamen
        """
        pygame.init()
        pygame.display.set_caption("Minesweeper")
        self.display = pygame.display.set_mode((750,750))
        self.menu_screen = MenuScreen(None, EventQueue(), Clock())
        self.game_loop = GameLoop(None, None, EventQueue(), Clock())
        self.custom_menu = CustomDifficulty(None, EventQueue(), Clock())
        self.leaderboard_input = LeaderboardInput(None, EventQueue(), Clock())

        connection = database_connection.get_database_connection()
        self.leaderboard_repository = LeaderboardRepository(connection)

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
                return_case = self.enter_leaderboard()
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
            self.menu_screen.set_renderer(MenuRenderer(self.display))
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
            self.menu_screen.set_renderer(DiffRenderer(self.display))
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
            self.custom_menu.set_renderer(CustomRenderer(self.display, MEDIUM_DIFF))
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

        pygame.display.set_mode((grid_x*CELL_SIZE, grid_y*CELL_SIZE))
        renderer = LevelRenderer(self.display, level)
        self.game_loop.set_renderer(renderer)

        end_condition = self.game_loop.start()
        if end_condition[0] == -1:
            return -1
        if end_condition[0] == 0:
            pygame.time.wait(3000)
        elif end_condition[0] == 1:
            pygame.time.wait(1000)
            #leaderboard toiminnallisuus
            is_saved = self.save_game_score((grid_x,grid_y,mines), end_condition[1])
            if is_saved in (-1,5):
                return is_saved
            renderer = LBRenderer(self.display, is_saved, self.leaderboard_repository)
            self.menu_screen.set_renderer(renderer)
            self.menu_screen.start()
        return 5

    def save_game_score(self, difficulty, time):
        """Luetaan käyttäjänimi ja tallennetaan tiedot tietokantaan

        Args:
            difficulty int: voitetun pelin vaikeustaso
            time float: peliin kulunut aika

        Returns:
            mahdollisia (-1,0,1,2,3,5):
                -1 poistutaan pelistä, 5 poistutaan alkunäkymään, 0-3 tallennettiin tulos
        """
        self.leaderboard_input.set_renderer(LBInputRenderer(self.display, time))
        username = self.leaderboard_input.start()
        if username in (-1,5):
            return username
        if difficulty == EASY_DIFF:
            diff = 1
        elif difficulty == MEDIUM_DIFF:
            diff = 2
        elif difficulty == HARD_DIFF:
            diff = 3
        else:
            diff = 0
        self.leaderboard_repository.add_score(username, diff, time)
        return diff

    def enter_leaderboard(self):
        """Alkunäkymästä voi myös siirtyä katsomaan tulostaulua,
        ensin valitaan kuitenkin mitkä tulokset näytetään

        Returns:
            int: -1 tai 5, -1 poistutaan pelistä, 5 palataan alkunäkymään
        """
        while True:
            self.menu_screen.set_renderer(LBSelectionRenderer(self.display))
            select = self.menu_screen.start()
            if select in (-1,5):
                return select
            renderer = LBRenderer(self.display, select, self.leaderboard_repository)
            self.menu_screen.set_renderer(renderer)
            returnal = self.menu_screen.start()
            if returnal == 5:
                continue
            return -1

if __name__ == "__main__":
    game = GameFrame()
    game.menu()
