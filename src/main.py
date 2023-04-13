import pygame
import time
from mapGenerator import mapGen
from level import Level
from start import Start
from default_menu import DefaultLoop
from game_loop import GameLoop
from event_queue import EventQueue
from clock import Clock

from ui.level_renderer import LevelRenderer
from ui.menu_renderer import MenuRenderer
from ui.difficulty_menu_renderer import DiffRenderer

CELL_SIZE = 50


def main():
    pygame.init()

    display = pygame.display.set_mode((750, 750))
    pygame.display.set_caption("Minesweeper")

    event_queue = EventQueue()
    menu_renderer = MenuRenderer(display)
    clock = Clock()
    start = Start(menu_renderer, event_queue, clock, CELL_SIZE)

    difficulty_renderer = DiffRenderer(display)
    difficulties = DefaultLoop(difficulty_renderer, event_queue, clock, CELL_SIZE)

    while True:
        grid_x = 16
        grid_y = 16
        mines = 40
        display = pygame.display.set_mode((750, 750))
        option_select = start.start()
        if option_select == -1:
            break
        elif option_select == 0:
            diff = difficulties.start()
            if diff == -1:
                break
            elif diff == 0:
                # easy
                grid_x = 9
                grid_y = 9
                mines = 10
            elif diff == 1:
                # medium
                pass
            elif diff == 2:
                # hard
                grid_x = 30
                grid_y = 16
                mines = 99
        elif option_select == 1:
            continue
        # elif option_select == 2: leaderboard
        else:
            continue

        # This part starts the actual game
        # returns a number table
        mineField = mapGen(grid_x, grid_y, mines)
        display_height = len(mineField.field) * CELL_SIZE
        display_width = len(mineField.field[0]) * CELL_SIZE
        # Paires the numbers with matching sprites
        level = Level(mineField.field, CELL_SIZE)
        display = pygame.display.set_mode((display_width, display_height))
        level_renderer = LevelRenderer(display, level)
        game_loop = GameLoop(level, level_renderer, event_queue, clock, CELL_SIZE)

        end_condition = game_loop.start()
        level_renderer.render()
        if end_condition == -1:
            break
        elif end_condition == 0:
            time.sleep(3)
        # elif end_condition == 1: input leaderboard


if __name__ == "__main__":
    main()
