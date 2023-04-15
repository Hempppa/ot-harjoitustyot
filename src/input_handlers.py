import pygame

class DefaultLoop:
    def __init__(self, renderer, event_queue, clock, cell_size):
        self._renderer = renderer
        self._event_queue = event_queue
        self._clock = clock
        self._cell_size = cell_size

    def set_renderer(self, renderer):
        self._renderer = renderer

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
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                button = event.__dict__['button']
                pos = pygame.mouse.get_pos()
                #print(buttons)
                if button == 1:
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
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                button = event.__dict__['button']
                pos = pygame.mouse.get_pos()
                #Pelin hidas "reagointi" johtuu tästä, edetään vasta kun MOUSEUP
                #Kuitenkin ilman tätä peli hajoaa kun ei rekisteröi MOUSEUP
                self.wait_for_mouse_button_up(button)
                game_situation = self._level.cell_clicked(button, pos)
                if game_situation in (1, 0):
                    return game_situation
        return 10

    def wait_for_mouse_button_up(self, button):
        while True:
            event = self._event_queue.wait()
            if event.type == pygame.MOUSEBUTTONUP and event.__dict__['button'] == button:
                break
