import pygame

class DefaultLoop:
    def __init__(self, renderer, event_queue, clock, cell_size):
        self._renderer = renderer
        self._event_queue = event_queue
        self._clock = clock
        self._cell_size = cell_size

    def start(self):
        while True:
            events = self._handle_events()
            if events in (-1, 0, 1, 2):
                self._render()
                return events
            self._render()
            self._clock.tick(60)

    def _handle_events(self):
        for event in self._event_queue.get():
            #en tiedä miksi, mutta pylint sanoo näissä no-member errorin
            if event.type == pygame.QUIT: #pylint: disable=no-member
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN: #pylint: disable=no-member
                buttons = pygame.mouse.get_pressed()
                pos = pygame.mouse.get_pos()
                #print(buttons)
                if buttons[0]:
                    return self.check_button_pressed(pos)
        return 10

    def check_button_pressed(self, pos):
        rect_list = self._renderer.option_rect_list
        for rect in rect_list:
            if rect.collidepoint(pos):
                return rect_list.index(rect)
        return 10

    def _render(self):
        self._renderer.render()


class StartMenu(DefaultLoop):
    pass

class DifficultySelection(DefaultLoop):
    pass

class GameLoop(DefaultLoop):
    def __init__(self, level, renderer, event_queue, clock, cell_size):
        self._level = level
        super().__init__(renderer, event_queue, clock, cell_size)

    def _handle_events(self):
        for event in self._event_queue.get():
            #en tiedä miksi, mutta pylint sanoo näissä no-member errorin
            if event.type == pygame.QUIT: #pylint: disable=no-member
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN: #pylint: disable=no-member
                buttons = pygame.mouse.get_pressed(3)
                pos = pygame.mouse.get_pos()
                self._event_queue.wait()
                #print(buttons)
                game_situation = self._level.cell_clicked(buttons, pos)
                if isinstance(game_situation, int):
                    return game_situation
        return 10
