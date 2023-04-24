import unittest
import pygame

from level import Level
from input_handlers import DefaultLoop, GameLoop


class StubClock:
    def tick(self, fps):
        pass

    def get_ticks(self):
        0

class StubEvent:
    def __init__(self, event_type, key=None, pos=None):
        self.button = key
        self.pos = pos
        self.type = event_type

class StubEventQueue:
    def __init__(self, events):
        self._events = events

    def get(self):
        if len(self._events) == 0:
            return []
        return [self._events.pop()]
    
    def wait(self):
        if len(self._events) == 0:
            return
        return self._events.pop()


class StubRenderer:
    def __init__(self, rects):
        self.rect_list = rects

    def render(self):
        pass

    def get_rect_info(self):
        return self.rect_list
    
    def set_active(self, number):
        pass

    def set_text(self, text, number):
        pass

MINEFIELD_1 = [[1, 1, 1],
               [1, 9, 1],
               [1, 1, 1]]
MINEFIELD_2 = [[0, 0, 0],
               [0, 0, 0],
               [0, 0, 0]]

CELL_SIZE = 50


class TestDefaultLoop(unittest.TestCase):
    def setUp(self) -> None:
        self.missed_click = (10,10)
        self.option_1_location = (125, 225)
        self.option_2_location = (125, 325)
        self.option_3_location = (125, 425)
        self.renderer = StubRenderer([pygame.rect.Rect(100, 200, 550, 75),
                                      pygame.rect.Rect(100, 300, 550, 75), 
                                      pygame.rect.Rect(100, 400, 550, 75)])

    def test_can_quit_the_game(self):
        events = [StubEvent(pygame.QUIT)]
        menu = DefaultLoop(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            CELL_SIZE
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(return_value, -1)
    
    def test_first_option_works(self):
        events = [StubEvent(pygame.MOUSEBUTTONDOWN, 1, self.option_1_location)]
        menu = DefaultLoop(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            CELL_SIZE
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(return_value, 0)

    def test_second_option_works(self):
        events = [StubEvent(pygame.MOUSEBUTTONDOWN, 1, self.option_2_location)]
        menu = DefaultLoop(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            CELL_SIZE
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(return_value, 1)

    def test_third_option_works(self):
        events = [StubEvent(pygame.MOUSEBUTTONDOWN, 1, self.option_3_location)]
        menu = DefaultLoop(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            CELL_SIZE
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(return_value, 2)

    def test_missed_click_does_not_affect(self):
        events = [
            StubEvent(pygame.MOUSEBUTTONDOWN, 1, self.option_1_location),
            StubEvent(pygame.MOUSEBUTTONDOWN, 1, self.missed_click)
        ]
        menu = DefaultLoop(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            CELL_SIZE
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(return_value, 0)

    def test_wrong_button_does_not_affect(self):
        events = [
            StubEvent(pygame.MOUSEBUTTONDOWN, 1, self.option_1_location),
            StubEvent(pygame.MOUSEBUTTONDOWN, 2, self.option_2_location)
        ]
        menu = DefaultLoop(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            CELL_SIZE
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(return_value, 0)


class TestGameLoop(unittest.TestCase):
    def setUp(self):
        self.level_1 = Level(MINEFIELD_1, CELL_SIZE)
        self.level_2 = Level(MINEFIELD_2, CELL_SIZE)
        self.renderer = StubRenderer([["16", False, pygame.rect.Rect(70, 250, 200, 75)],
                                      ["16", False, pygame.rect.Rect(380, 250, 200, 75)], 
                                      ["40", False, pygame.rect.Rect(70, 450, 400, 75)]])

    def test_can_quit_the_game(self):
        events = [StubEvent(pygame.QUIT)]
        game_loop = GameLoop(
            self.level_1,
            StubRenderer(None),
            StubEventQueue(events),
            StubClock(),
            CELL_SIZE
        )
        return_value = game_loop.start()
        self.assertEqual(return_value, -1)

    def test_can_complete_empty_level(self):
        events = [
            StubEvent(pygame.MOUSEBUTTONUP, 1, (25,25)),
            StubEvent(pygame.MOUSEBUTTONDOWN, 1, (25,25))
        ]
        game_loop = GameLoop(
            self.level_2,
            StubRenderer(None),
            StubEventQueue(events),
            StubClock(),
            CELL_SIZE
        )
        return_value = game_loop.start()
        self.assertEqual(return_value, 1)

    def test_can_fail_level(self):
        events = [
            StubEvent(pygame.MOUSEBUTTONUP, 1, (75,75)),
            StubEvent(pygame.MOUSEBUTTONDOWN, 1, (75,75))
        ]
        game_loop = GameLoop(
            self.level_1,
            StubRenderer(None),
            StubEventQueue(events),
            StubClock(),
            CELL_SIZE
        )
        return_value = game_loop.start()
        self.assertEqual(return_value, 0)

    def test_flagged_cells_work(self):
        events = [
            StubEvent(pygame.MOUSEBUTTONUP, 1, (125,125)),
            StubEvent(pygame.MOUSEBUTTONDOWN, 1, (25,25)),
            StubEvent(pygame.MOUSEBUTTONDOWN, 1, (25,75)),
            StubEvent(pygame.MOUSEBUTTONDOWN, 1, (25,125)),
            StubEvent(pygame.MOUSEBUTTONDOWN, 1, (75,25)),
            StubEvent(pygame.MOUSEBUTTONDOWN, 1, (75,75)),
            StubEvent(pygame.MOUSEBUTTONDOWN, 1, (75,125)),
            StubEvent(pygame.MOUSEBUTTONDOWN, 1, (125,25)),
            StubEvent(pygame.MOUSEBUTTONDOWN, 1, (125,75)),
            StubEvent(pygame.MOUSEBUTTONDOWN, 1, (125,125)),
            StubEvent(pygame.MOUSEBUTTONDOWN, 3, (75,75))
        ]
        game_loop = GameLoop(
            self.level_1,
            StubRenderer(None),
            StubEventQueue(events),
            StubClock(),
            CELL_SIZE
        )
        return_value = game_loop.start()
        self.assertEqual(return_value, 1)