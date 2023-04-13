import pygame


class GameLoop:
    def __init__(self, level, renderer, event_queue, clock, cell_size):
        self._level = level
        self._renderer = renderer
        self._event_queue = event_queue
        self._clock = clock
        self._cell_size = cell_size

    def start(self):
        while True:
            end_condition = self._handle_events()
            if type(end_condition) == int:
                return end_condition
            self._render()
            self._clock.tick(60)

    def _handle_events(self):
        for event in self._event_queue.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                buttons = pygame.mouse.get_pressed(3)
                pos = pygame.mouse.get_pos()
                game_situation = self._level.cellClicked(buttons, pos)
                if type(game_situation) == int:
                    return game_situation

    def _render(self):
        self._renderer.render()
