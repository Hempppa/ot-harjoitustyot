import pygame


class Renderer:
    def __init__(self, display, level):
        self._display = display
        self._level = level

    def render(self):
        self._level.all_other_cells.draw(self._display)
        self._level.cellCovers.draw(self._display)

        pygame.display.update()