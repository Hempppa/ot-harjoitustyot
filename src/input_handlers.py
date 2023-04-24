import pygame

class DefaultLoop:
    def __init__(self, renderer, event_queue, clock, cell_size):
        self._renderer = renderer
        self._event_queue = event_queue
        self._clock = clock
        self._cell_size = cell_size
        self._rect_list = None

    def set_renderer(self, renderer):
        self._renderer = renderer
        self._rect_list = renderer.get_rect_info()

    def start(self):
        while True:
            events = self._handle_events()
            if events in (-1, 0, 1, 2):
                return events
            self._render()
            self._clock.tick(60)

    def _handle_events(self):
        for event in self._event_queue.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                #print(buttons)
                if event.button == 1:
                    return self.check_option_pressed(event.pos)
        return 10

    def check_option_pressed(self, pos):
        for rect in self._rect_list:
            if rect.collidepoint(pos):
                return self._rect_list.index(rect)
        return 10

    def _render(self):
        self._renderer.render()


class StartMenu(DefaultLoop):
    pass

class DifficultySelection(DefaultLoop):
    pass

class CustomDifficulty(DefaultLoop):
    def __init__(self, renderer, event_queue, clock, cell_size):
        super().__init__(renderer, event_queue, clock, cell_size)
        self.active = 0

    def start(self):
        while True:
            events = self._handle_events()
            if events == -1 or isinstance(events, list):
                return events
            self._render()
            self._clock.tick(60)

    def _handle_events(self):
        for event in self._event_queue.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                #print(buttons)
                if event.button == 1:
                    activated = self.check_option_pressed(event.pos)
                    self._renderer.set_active(activated)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return self.set_final_values()
                if self.active == 0:
                    continue
                if event.key == pygame.K_BACKSPACE:
                    shortened = self._rect_list [self.active-1][0][:-1]
                    self._rect_list [self.active-1][0] = shortened
                    self._renderer.set_text(shortened, self.active)
                self.set_int_value(event.unicode)
        return 10

    def set_final_values(self):
        grid_values = [1,1,1]
        rects = len(self._rect_list )
        for i in range(rects):
            if not (self._rect_list [i][0] == "" or self._rect_list [i][0] == "0"):
                grid_values[i] = int(self._rect_list [i][0])
        if grid_values[2] > grid_values[0]*grid_values[1]:
            grid_values[2] = grid_values[0]*grid_values[1]
        return grid_values

    def set_int_value(self, user_input):
        try:
            int(user_input)
        except ValueError:
            return
        if self.active == 1:
            limit = 38
        elif self.active == 2:
            limit = 18
        else:
            limit = 798
        new_value = int(self._rect_list [self.active-1][0] + user_input)
        if new_value > limit:
            self._rect_list [self.active-1][0] = str(limit)
            self._renderer.set_text(str(limit), self.active)
        else:
            self._rect_list [self.active-1][0] = str(new_value)
            self._renderer.set_text(str(new_value), self.active)

    def check_option_pressed(self, pos):
        rects = len(self._rect_list )
        clicked = False
        for i in range(rects):
            if self._rect_list [i][2].collidepoint(pos):
                self.active = i+1
                clicked = True
        if not clicked:
            self.active = 0
        return self.active


class GameLoop(DefaultLoop):
    def __init__(self, level, renderer, event_queue, clock, cell_size):
        self._level = level
        super().__init__(renderer, event_queue, clock, cell_size)

    def _handle_events(self):
        for event in self._event_queue.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_situation = self._level.cell_clicked(event.button, event.pos)
                if game_situation in (1, 0):
                    self._render()
                    #Pelin hidas "reagointi" johtuu tästä, edetään vasta kun MOUSEUP
                    #Kuitenkin ilman tätä peli hajoaa kun ei rekisteröi MOUSEUP
                    self.wait_for_mouse_button_up(event.button)
                    return game_situation
        return 10

    def wait_for_mouse_button_up(self, button):
        while True:
            event = self._event_queue.wait()
            if event.type == pygame.MOUSEBUTTONUP and event.button == button:
                break
