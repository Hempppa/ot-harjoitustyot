import pygame
import time
from mapGenerator import mapGen
from level import Level
from game_loop import GameLoop
from event_queue import EventQueue
from renderer import Renderer
from clock import Clock

CELL_SIZE = 50

def main():
    #returns a number table
    mineField = mapGen()
    display_height = len(mineField.field) * CELL_SIZE
    display_width = len(mineField.field[0]) * CELL_SIZE
    #Paires the numbers with matching sprites
    level = Level(mineField.field, CELL_SIZE)

    display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Minesweeper")

    event_queue = EventQueue()
    renderer = Renderer(display, level)
    clock = Clock()
    game_loop = GameLoop(level, renderer, event_queue, clock, CELL_SIZE)

    pygame.init()
    game_loop.start()
    renderer.render()
    time.sleep(3)

if __name__ == "__main__":
    main()
