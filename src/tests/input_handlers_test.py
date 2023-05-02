import unittest
import pygame

from levelgeneration.level import Level
from gamelogic.input_handlers import DefaultLoop, GameLoop, CustomDifficulty, LeaderboardInput


class StubClock:
    def tick(self, fps):
        pass

    def get_ticks(self):
        0

class StubEvent:
    def __init__(self, event_type, key=None, pos=None):
        if event_type == pygame.KEYDOWN:
            if key == pygame.K_1:
                self.unicode = "1"
            elif key == pygame.K_a:
                self.unicode = "a"
        self.key = key
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
    def __init__(self, rects=None):
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
            
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(return_value, -1)

    def test_can_return_to_menu(self):
        events = [StubEvent(pygame.KEYDOWN, pygame.K_ESCAPE)]
        menu = DefaultLoop(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(return_value, 5)
    
    def test_first_option_works(self):
        events = [StubEvent(pygame.MOUSEBUTTONDOWN, 1, self.option_1_location)]
        menu = DefaultLoop(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            
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
            
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(return_value, 0)


class TestGameLoop(unittest.TestCase):
    def setUp(self):
        self.level_1 = Level(MINEFIELD_1, 50)
        self.level_2 = Level(MINEFIELD_2, 50)
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
            
        )
        return_value = game_loop.start()
        self.assertEqual(return_value[0], -1)

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
            
        )
        return_value = game_loop.start()
        self.assertEqual(return_value[0], 1)

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
            
        )
        return_value = game_loop.start()
        self.assertEqual(return_value[0], 0)

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
            
        )
        return_value = game_loop.start()
        self.assertEqual(return_value[0], 1)



class TestCustomDifficulty(unittest.TestCase):
    def setUp(self) -> None:
        self.missed_click = (10,10)
        self.option_1_location = (80, 260)
        self.option_2_location = (390, 260)
        self.option_3_location = (80, 460)
        self.renderer = StubRenderer([["16", False, pygame.rect.Rect(70, 250, 200, 75)],
                                      ["16", False, pygame.rect.Rect(380, 250, 200, 75)], 
                                      ["30", False, pygame.rect.Rect(70, 450, 400, 75)]])

    def test_can_quit_the_game(self):
        events = [StubEvent(pygame.QUIT)]
        menu = CustomDifficulty(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(return_value, -1)

    def test_can_return_to_menu(self):
        events = [StubEvent(pygame.KEYDOWN, pygame.K_ESCAPE)]
        menu = CustomDifficulty(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(return_value, 5)

    def test_can_enter_with_default_values(self):
        events = [StubEvent(pygame.KEYDOWN, pygame.K_RETURN)]
        menu = CustomDifficulty(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(menu.active, 0)
        self.assertEqual(return_value, [16,16,30])
    
    def test_first_option_works(self):
        events = [StubEvent(pygame.KEYDOWN, pygame.K_RETURN),
                  StubEvent(pygame.KEYDOWN, pygame.K_BACKSPACE),
                  StubEvent(pygame.MOUSEBUTTONDOWN, 1, self.option_1_location)]
        menu = CustomDifficulty(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(menu.active, 1)
        self.assertEqual(return_value, [1,16,16])

    def test_second_option_works(self):
        events = [StubEvent(pygame.KEYDOWN, pygame.K_RETURN),
                  StubEvent(pygame.KEYDOWN, pygame.K_BACKSPACE),
                  StubEvent(pygame.MOUSEBUTTONDOWN, 1, self.option_2_location)]
        menu = CustomDifficulty(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(menu.active, 2)
        self.assertEqual(return_value, [16,1,16])

    def test_third_option_works(self):
        events = [StubEvent(pygame.KEYDOWN, pygame.K_RETURN),
                  StubEvent(pygame.KEYDOWN, pygame.K_BACKSPACE),
                  StubEvent(pygame.MOUSEBUTTONDOWN, 1, self.option_3_location)]
        menu = CustomDifficulty(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(menu.active, 3)
        self.assertEqual(return_value, [16,16,3])

    def test_missed_click_does_not_affect(self):
        events = [StubEvent(pygame.KEYDOWN, pygame.K_RETURN),
                  StubEvent(pygame.KEYDOWN, pygame.K_BACKSPACE),
                  StubEvent(pygame.MOUSEBUTTONDOWN, 1, self.missed_click)]
        menu = CustomDifficulty(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(menu.active, 0)
        self.assertEqual(return_value, [16,16,30])

    def test_wrong_button_does_not_affect(self):
        events = [StubEvent(pygame.KEYDOWN, pygame.K_RETURN),
                  StubEvent(pygame.KEYDOWN, pygame.K_BACKSPACE),
                  StubEvent(pygame.MOUSEBUTTONDOWN, 2, self.option_2_location)]
        menu = CustomDifficulty(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(menu.active, 0)
        self.assertEqual(return_value, [16,16,30])

    def test_cannot_go_lower_than_one(self):
        events = [StubEvent(pygame.KEYDOWN, pygame.K_RETURN),
                  StubEvent(pygame.KEYDOWN, pygame.K_BACKSPACE),
                  StubEvent(pygame.KEYDOWN, pygame.K_BACKSPACE),
                  StubEvent(pygame.KEYDOWN, pygame.K_BACKSPACE),
                  StubEvent(pygame.MOUSEBUTTONDOWN, 1, self.option_3_location),
                  StubEvent(pygame.KEYDOWN, pygame.K_BACKSPACE),
                  StubEvent(pygame.KEYDOWN, pygame.K_BACKSPACE),
                  StubEvent(pygame.KEYDOWN, pygame.K_BACKSPACE),
                  StubEvent(pygame.MOUSEBUTTONDOWN, 1, self.option_2_location),
                  StubEvent(pygame.KEYDOWN, pygame.K_BACKSPACE),
                  StubEvent(pygame.KEYDOWN, pygame.K_BACKSPACE),
                  StubEvent(pygame.KEYDOWN, pygame.K_BACKSPACE),
                  StubEvent(pygame.MOUSEBUTTONDOWN, 1, self.option_1_location)]
        menu = CustomDifficulty(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(return_value, [1,1,1])

    def test_cannot_over_limits(self):
        events = [StubEvent(pygame.KEYDOWN, pygame.K_RETURN),
                  StubEvent(pygame.KEYDOWN, pygame.K_1),
                  StubEvent(pygame.KEYDOWN, pygame.K_1),
                  StubEvent(pygame.KEYDOWN, pygame.K_1),
                  StubEvent(pygame.MOUSEBUTTONDOWN, 1, self.option_3_location),
                  StubEvent(pygame.KEYDOWN, pygame.K_1),
                  StubEvent(pygame.KEYDOWN, pygame.K_1),
                  StubEvent(pygame.KEYDOWN, pygame.K_1),
                  StubEvent(pygame.MOUSEBUTTONDOWN, 1, self.option_2_location),
                  StubEvent(pygame.KEYDOWN, pygame.K_1),
                  StubEvent(pygame.KEYDOWN, pygame.K_1),
                  StubEvent(pygame.KEYDOWN, pygame.K_1),
                  StubEvent(pygame.MOUSEBUTTONDOWN, 1, self.option_1_location)]
        menu = CustomDifficulty(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(return_value, [38,18,684])

    def test_cannot_have_more_mines_than_cells(self):
        events = [StubEvent(pygame.KEYDOWN, pygame.K_RETURN),
                  StubEvent(pygame.KEYDOWN, pygame.K_1),
                  StubEvent(pygame.KEYDOWN, pygame.K_1),
                  StubEvent(pygame.KEYDOWN, pygame.K_1),
                  StubEvent(pygame.MOUSEBUTTONDOWN, 1, self.option_3_location)]
        menu = CustomDifficulty(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(return_value, [16,16,(16*16)])

    def test_cannot_input_non_integer(self):
        events = [StubEvent(pygame.KEYDOWN, pygame.K_RETURN),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.MOUSEBUTTONDOWN, 1, self.option_1_location)]
        menu = CustomDifficulty(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(menu.active, 1)
        self.assertEqual(return_value, [16,16,30])

class TestLeaderboardInput(unittest.TestCase):
    def setUp(self) -> None:
        self.missed_click = (10,10)
        self.option_location = (80, 460)
        self.renderer = StubRenderer([["", False, pygame.Rect(70, 450, 400, 75)]])

    def test_can_quit_the_game(self):
        events = [StubEvent(pygame.QUIT)]
        menu = LeaderboardInput(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(return_value, -1)

    def test_can_enter_with_default_values(self):
        events = [StubEvent(pygame.KEYDOWN, pygame.K_RETURN)]
        menu = LeaderboardInput(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(menu.active, 0)
        self.assertEqual(return_value, "")
    
    def test_text_option_works(self):
        events = [StubEvent(pygame.KEYDOWN, pygame.K_RETURN),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.MOUSEBUTTONDOWN, 1, self.option_location)]
        menu = LeaderboardInput(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(menu.active, 1)
        self.assertEqual(return_value, "a")

    def test_cannot_input_longer_than_limit(self):
        events = [StubEvent(pygame.KEYDOWN, pygame.K_RETURN),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.MOUSEBUTTONDOWN, 1, self.option_location)]
        menu = LeaderboardInput(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(return_value, "aaaaaaaa")

    def test_can_remove_letters(self):
        events = [StubEvent(pygame.KEYDOWN, pygame.K_RETURN),
                  StubEvent(pygame.KEYDOWN, pygame.K_BACKSPACE),
                  StubEvent(pygame.KEYDOWN, pygame.K_BACKSPACE),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.MOUSEBUTTONDOWN, 1, self.option_location)]
        menu = LeaderboardInput(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(return_value, "aaa")

    def test_can_return_to_not_save_score(self):
        events = [StubEvent(pygame.KEYDOWN, pygame.K_RETURN),
                  StubEvent(pygame.KEYDOWN, pygame.K_ESCAPE),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.MOUSEBUTTONDOWN, 1, self.option_location)]
        menu = LeaderboardInput(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(return_value, 5)

    def test_cannot_add_unless_activated(self):
        events = [StubEvent(pygame.KEYDOWN, pygame.K_RETURN),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.MOUSEBUTTONDOWN, 1, self.option_location),
                  StubEvent(pygame.KEYDOWN, pygame.K_a)]
        menu = LeaderboardInput(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(menu.active, 1)
        self.assertEqual(return_value, "a")

    def test_misclick_does_not_affect(self):
        events = [StubEvent(pygame.KEYDOWN, pygame.K_RETURN),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.MOUSEBUTTONDOWN, 1, self.missed_click)]
        menu = LeaderboardInput(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(menu.active, 0)
        self.assertEqual(return_value, "")

    def test_wrong_button_doent_activate(self):
        events = [StubEvent(pygame.KEYDOWN, pygame.K_RETURN),
                  StubEvent(pygame.KEYDOWN, pygame.K_a),
                  StubEvent(pygame.MOUSEBUTTONDOWN, 2, self.option_location)]
        menu = LeaderboardInput(
            self.renderer,
            StubEventQueue(events),
            StubClock(),
            
        )
        menu.set_renderer(self.renderer)
        return_value = menu.start()
        self.assertEqual(menu.active, 0)
        self.assertEqual(return_value, "")