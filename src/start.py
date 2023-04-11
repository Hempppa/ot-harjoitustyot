import pygame

class Start:
    def __init__(self, startRenderer, event_queue, clock, cell_size):
        self._renderer = startRenderer
        self._event_queue = event_queue
        self._clock = clock
        self._cell_size = cell_size
        self.start_rect = pygame.Rect(200,200,140,34)

    def start(self):
        while True:
            events = self._handle_events()
            if type(events) == bool:
                return events
            self._render()
            self._clock.tick(60)

    def _handle_events(self):
        for event in self._event_queue.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                buttons = pygame.mouse.get_pressed(3)
                pos = pygame.mouse.get_pos()
                if buttons[0]:
                    if self.start_rect.collidepoint(pos):
                        return True


    def _render(self):
        self._renderer.render()