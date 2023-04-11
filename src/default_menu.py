import pygame

class DefaultLoop:
    def __init__(self, startRenderer, event_queue, clock, cell_size):
        self._renderer = startRenderer
        self._event_queue = event_queue
        self._clock = clock
        self._cell_size = cell_size
        self._option_rect = pygame.Rect(150,200,250,75)
        self._renderer.option_rect = self._option_rect

    def start(self):
        while True:
            events = self._handle_events()
            if type(events) == int:
                return events
            self._render()
            self._clock.tick(60)

    def _handle_events(self):
        for event in self._event_queue.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                buttons = pygame.mouse.get_pressed(3)
                pos = pygame.mouse.get_pos()
                if buttons[0]:
                    for i in range(len(self._renderer.option_rect_list)):
                        if self._renderer.option_rect_list[i].collidepoint(pos):
                            return i


    def _render(self):
        self._renderer.render()