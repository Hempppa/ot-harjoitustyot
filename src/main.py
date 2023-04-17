#import time
import pygame
from map_generator import MapGen
from level import Level
from input_handlers import GameLoop, StartMenu, DifficultySelection, CustomDifficulty
from event_queue import EventQueue
from clock import Clock

from ui.level_renderer import LevelRenderer
from ui.menu_renderer import MenuRenderer
from ui.difficulty_menu_renderer import DiffRenderer
from ui.custom_menu_renderer import CustomRenderer

CELL_SIZE = 50

class GameEngine():
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((750, 750))
        pygame.display.set_caption("Minesweeper")
        self.event_queue = EventQueue()
        self.clock = Clock()
        self.start_menu = StartMenu(None, self.event_queue, self.clock, CELL_SIZE)
        self.difficulties = DifficultySelection(None, self.event_queue, self.clock, CELL_SIZE)
        self.custom_menu = CustomDifficulty(None, self.event_queue, self.clock, CELL_SIZE)

    def start_game_loop(self, grid_x, grid_y, mines):
        mine_field = MapGen(grid_x, grid_y, mines)
        # Paires the numbers with matching sprites
        level = Level(mine_field.field, CELL_SIZE)
        pygame.display.set_mode((grid_x*CELL_SIZE, grid_y*CELL_SIZE))
        renderer = LevelRenderer(self.display, level)
        game_loop = GameLoop(level, renderer, self.event_queue, self.clock, CELL_SIZE)
        return game_loop.start()

    def enter_start_menu(self):
        self.start_menu.set_renderer(MenuRenderer(self.display))
        return self.start_menu.start()

    def selected_difficulties(self, selection):
        if selection == 0:
            self.difficulties.set_renderer(DiffRenderer(self.display))
            diff = self.difficulties.start()
            selected = (16,16,40)
            if diff == -1:
                return -1
            if diff == 0:
                # easy
                selected = (9,9,10)
            elif diff == 1:
                # medium
                pass
            elif diff == 2:
                # hard
                selected = (30,16,99)
        elif selection == 1:
            self.custom_menu.set_renderer(CustomRenderer(self.display))
            selected = self.custom_menu.start()
        return selected

    def menu(self):
        while True:
            option_select = self.enter_start_menu()
            if option_select == -1:
                break
            if option_select in (0,1):
                selected = self.selected_difficulties(option_select)
                if selected == -1:
                    break
                (grid_x, grid_y, mines) = selected
            # elif option_select == 2: leaderboard
            else:
                continue
            end_condition = self.start_game_loop(grid_x, grid_y, mines)
            if end_condition == -1:
                break
            if end_condition == 0:
                pygame.time.wait(3000)
            elif end_condition == 1:
                pygame.time.wait(1000) #input leaderboard myöhemmin

if __name__ == "__main__":
    game = GameEngine()
    game.menu()
