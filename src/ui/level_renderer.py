import pygame

class LevelRenderer:
    def __init__(self, display, level):
        self._display = display
        self._level = level

    def render(self):
        self._level.all_cells.draw(self._display)
        self._level.cell_covers.draw(self._display)
        self._level.flags.draw(self._display)
        pygame.display.update()
