#import time
import pygame
from map_generator import MapGen
from level import Level
from input_handlers import GameLoop, StartMenu, DifficultySelection
from event_queue import EventQueue
from clock import Clock

from ui.level_renderer import LevelRenderer
from ui.menu_renderer import MenuRenderer
from ui.difficulty_menu_renderer import DiffRenderer

CELL_SIZE = 50

class GameEngine():
    def __init__(self):
        #sama pylint errori taas, en tiiä miksi
        pygame.init() #pylint: disable=no-member
        self.display = pygame.display.set_mode((750, 750))
        pygame.display.set_caption("Minesweeper")

    def enter_diff_selection(self):
        event_queue2 = EventQueue()
        clock2 = Clock()
        renderer2 = DiffRenderer(self.display)
        difficulties = DifficultySelection(renderer2, event_queue2, clock2, CELL_SIZE)
        diff = difficulties.start()
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
        return selected

    def start_game_loop(self, grid_x, grid_y, mines):
        mine_field = MapGen(grid_x, grid_y, mines)
        # Paires the numbers with matching sprites
        level = Level(mine_field.field, CELL_SIZE)
        pygame.display.set_mode((grid_x*CELL_SIZE, grid_y*CELL_SIZE))
        event_queue3 = EventQueue()
        clock3 = Clock()
        renderer3 = LevelRenderer(self.display, level)
        game_loop = GameLoop(level, renderer3, event_queue3, clock3, CELL_SIZE)
        return game_loop.start()

    def enter_main_menu(self):
        event_queue1 = EventQueue()
        clock1 = Clock()
        renderer1 = MenuRenderer(self.display)
        start_menu = StartMenu(renderer1, event_queue1, clock1, CELL_SIZE)
        return start_menu.start()

    def menu(self):
        while True:
            option_select = self.enter_main_menu()
            if option_select == -1:
                break
            if option_select == 0:
                selected = self.enter_diff_selection()
                if selected == -1:
                    break
                (grid_x, grid_y, mines) = selected
            elif option_select == 1:
                continue
            # elif option_select == 2: leaderboard
            else:
                continue
            end_condition = self.start_game_loop(grid_x, grid_y, mines)
            if end_condition == -1:
                break
            if end_condition == 0:
                pygame.time.wait(3000)
            # elif end_condition == 1: input leaderboard

if __name__ == "__main__":
    game = GameEngine()
    game.menu()
