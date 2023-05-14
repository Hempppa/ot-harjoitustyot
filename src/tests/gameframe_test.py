import unittest
import pygame
from main import GameFrame
from gamelogic.input_handlers import GameLoop, MenuScreen, CustomDifficulty
from gamelogic.input_handlers import LeaderboardInput
from gamelogic.event_queue import EventQueue
from gamelogic.clock import Clock
from repository.leaderboard_repository import LeaderboardRepository
import database_connection
from initialize_database import initialize_database

class StubInputHandler():
    def __init__(self):
        self.called = False
        self.return_values = []

    def start(self):
        self.called = True
        return_value = self.return_values[0]
        self.return_values = self.return_values[1:]
        return return_value
    
    def add_return_value(self, value):
        self.return_values.append(value)
    
    def set_renderer(self, renderer):
        renderer.set_called()


class StubRenderer():
    def __init__(self, timeline, name):
        self.timeline = timeline
        self.name = name
        self.called = False

    def set_called(self):
        self.called = True
        self.timeline.append(self.name)

    def set_active(self, which):
        pass

    def set_level(self, level, size):
        pass

    def set_time(self, time):
        pass

    def set_scores(self, diff):
        pass

class StubRepo():
    def __init__(self):
        self.called = False
        self.scores = []

    def add_score(self, name, diff, time):
        self.scores.append((name, diff, time))
        self.called = True

class TestGameFrame(unittest.TestCase):
    def setUp(self):
        self.visiting_timeline = []
        self.menu_renderer = StubRenderer(self.visiting_timeline, "menu")
        self.level_renderer = StubRenderer(self.visiting_timeline, "level")
        self.diff_renderer = StubRenderer(self.visiting_timeline, "diff")
        self.custom_renderer = StubRenderer(self.visiting_timeline, "custom")
        self.LB_renderer = StubRenderer(self.visiting_timeline, "LB")
        self.LBSelection_renderer = StubRenderer(self.visiting_timeline, "LBSelection")
        self.LBInput_renderer = StubRenderer(self.visiting_timeline, "LBInput")

        self.menu_screen = StubInputHandler()
        self.game_loop = StubInputHandler()
        self.custom_menu = StubInputHandler()
        self.leaderboard_input = StubInputHandler()

        self.leaderboard_repository = StubRepo()

        self.renderers = [self.menu_renderer,
                     self.level_renderer,
                     self.diff_renderer,
                     self.custom_renderer,
                     self.LB_renderer,
                     self.LBSelection_renderer,
                     self.LBInput_renderer]
        self.input_handlers = [self.menu_screen,
                          self.game_loop,
                          self.custom_menu,
                          self.leaderboard_input]
        
        self.game = GameFrame(self.input_handlers, self.renderers, self.leaderboard_repository)

    def test_only_main_menu_visited_when_quitting_first(self):
        self.menu_screen.add_return_value(-1)
        self.game.menu()

        visited_handlers = [self.menu_screen]
        visited_renderers = [self.menu_renderer]

        for renderer in self.renderers:
            if renderer in visited_renderers:
                self.assertEqual(renderer.called, True)
            else:
                self.assertEqual(renderer.called, False)

        for input_handler in self.input_handlers:
            if input_handler in visited_handlers:
                self.assertEqual(input_handler.called, True)
            else:
                self.assertEqual(input_handler.called, False)

    def test_can_quit_anywhere(self):
        self.menu_screen.add_return_value(-1) #menu
        self.menu_screen.add_return_value(0)
        self.menu_screen.add_return_value(-1) #diff
        self.menu_screen.add_return_value(1)
        self.custom_menu.add_return_value(-1) #custom
        self.menu_screen.add_return_value(0)
        self.menu_screen.add_return_value(1)
        self.game_loop.add_return_value((-1,0)) #gameloop
        self.menu_screen.add_return_value(0)
        self.menu_screen.add_return_value(1)
        self.game_loop.add_return_value((1,0))
        self.leaderboard_input.add_return_value(-1) #LBInput
        self.menu_screen.add_return_value(2)
        self.menu_screen.add_return_value(-1) #LBSelection
        self.menu_screen.add_return_value(2)
        self.menu_screen.add_return_value(0)
        self.menu_screen.add_return_value(-1) #LB

        #testi perustuu tähän, jos ei voisi poistua, niin testi jäisi ikuisesti pyörimään
        self.game.menu()
        self.game.menu()
        self.game.menu()
        self.game.menu()
        self.game.menu()
        self.game.menu()
        self.game.menu()

        visited_handlers = self.input_handlers
        visited_renderers = self.renderers

        for renderer in self.renderers:
            if renderer in visited_renderers:
                self.assertEqual(renderer.called, True)
            else:
                self.assertEqual(renderer.called, False)

        for input_handler in self.input_handlers:
            if input_handler in visited_handlers:
                self.assertEqual(input_handler.called, True)
            else:
                self.assertEqual(input_handler.called, False)

    def test_can_return_where_supposed_to(self):
        #not supposed to in menu, gameloop
        self.menu_screen.add_return_value(0) 
        self.menu_screen.add_return_value(5) #diff
        self.menu_screen.add_return_value(0)
        self.menu_screen.add_return_value(2)
        self.game_loop.add_return_value((1,0))
        self.leaderboard_input.add_return_value(5) #LBInput
        self.menu_screen.add_return_value(1)
        self.custom_menu.add_return_value(5) #Custom
        self.menu_screen.add_return_value(2)
        self.menu_screen.add_return_value(0)
        self.menu_screen.add_return_value(5) #LB
        self.menu_screen.add_return_value(5) #LBSelection
        self.menu_screen.add_return_value(-1)

        self.game.menu()

        visitings = ["menu", "diff", "menu", "diff", "level", "LBInput", "menu", "custom", "menu", "LBSelection", "LB", "LBSelection", "menu"]

        for i in range(len(visitings)):
            self.assertEqual(self.visiting_timeline[i], visitings[i])

    def test_esc_in_main_menu_wont_do_anything(self):
        self.menu_screen.add_return_value(5)
        self.menu_screen.add_return_value(-1)
        self.game.menu()

        visited_handlers = [self.menu_screen]
        visited_renderers = [self.menu_renderer]

        for renderer in self.renderers:
            if renderer in visited_renderers:
                self.assertEqual(renderer.called, True)
            else:
                self.assertEqual(renderer.called, False)

        for input_handler in self.input_handlers:
            if input_handler in visited_handlers:
                self.assertEqual(input_handler.called, True)
            else:
                self.assertEqual(input_handler.called, False)

    def test_esc_in_selection_will_return(self):
        self.menu_screen.add_return_value(0)
        self.menu_screen.add_return_value(5)
        self.menu_screen.add_return_value(0)
        self.menu_screen.add_return_value(-1)
        self.game_loop.add_return_value((-1,0))
        self.game.menu()

        visited_handlers = [self.menu_screen]
        visited_renderers = [self.menu_renderer, self.diff_renderer]

        for renderer in self.renderers:
            if renderer in visited_renderers:
                self.assertEqual(renderer.called, True)
            else:
                self.assertEqual(renderer.called, False)

        for input_handler in self.input_handlers:
            if input_handler in visited_handlers:
                self.assertEqual(input_handler.called, True)
            else:
                self.assertEqual(input_handler.called, False)

    def test_game_will_enter_game(self):
        self.menu_screen.add_return_value(0)
        self.menu_screen.add_return_value(0)
        self.game_loop.add_return_value((-1,0))
        self.game.menu()

        visited_handlers = [self.menu_screen, self.game_loop]
        visited_renderers = [self.menu_renderer, self.diff_renderer, self.level_renderer]

        for renderer in self.renderers:
            if renderer in visited_renderers:
                self.assertEqual(renderer.called, True)
            else:
                self.assertEqual(renderer.called, False)

        for input_handler in self.input_handlers:
            if input_handler in visited_handlers:
                self.assertEqual(input_handler.called, True)
            else:
                self.assertEqual(input_handler.called, False)

    def test_visiting_every_renderer(self):
        self.menu_screen.add_return_value(0)
        self.menu_screen.add_return_value(0)
        self.game_loop.add_return_value((1,0))
        self.leaderboard_input.add_return_value("name")
        self.menu_screen.add_return_value(5)
        self.menu_screen.add_return_value(2)
        self.menu_screen.add_return_value(5)
        self.menu_screen.add_return_value(1)
        self.custom_menu.add_return_value((16,16,1))
        self.game_loop.add_return_value((-1,0))

        self.game.menu()

        visited_handlers = self.input_handlers
        visited_renderers = self.renderers

        for renderer in self.renderers:
            if renderer in visited_renderers:
                self.assertEqual(renderer.called, True)
            else:
                self.assertEqual(renderer.called, False)

        for input_handler in self.input_handlers:
            if input_handler in visited_handlers:
                self.assertEqual(input_handler.called, True)
            else:
                self.assertEqual(input_handler.called, False)

    def test_will_save_score(self):
        self.menu_screen.add_return_value(0)
        self.menu_screen.add_return_value(0)
        self.game_loop.add_return_value((1,0))
        self.leaderboard_input.add_return_value("name")
        self.menu_screen.add_return_value(-1)

        self.game.menu()

        self.assertEqual(self.leaderboard_repository.scores[0], ("name", "Easy", 0))






class TestFrameAndRepo(unittest.TestCase):
    #Muuten sama kuin edellinen, mutta oikea repo käytössä
    def setUp(self):
        self.visiting_timeline = []
        self.menu_renderer = StubRenderer(self.visiting_timeline, "menu")
        self.level_renderer = StubRenderer(self.visiting_timeline, "level")
        self.diff_renderer = StubRenderer(self.visiting_timeline, "diff")
        self.custom_renderer = StubRenderer(self.visiting_timeline, "custom")
        self.LB_renderer = StubRenderer(self.visiting_timeline, "LB")
        self.LBSelection_renderer = StubRenderer(self.visiting_timeline, "LBSelection")
        self.LBInput_renderer = StubRenderer(self.visiting_timeline, "LBInput")

        self.menu_screen = StubInputHandler()
        self.game_loop = StubInputHandler()
        self.custom_menu = StubInputHandler()
        self.leaderboard_input = StubInputHandler()

        initialize_database()
        self.leaderboard_repository = LeaderboardRepository(database_connection.get_database_connection())

        self.renderers = [self.menu_renderer,
                     self.level_renderer,
                     self.diff_renderer,
                     self.custom_renderer,
                     self.LB_renderer,
                     self.LBSelection_renderer,
                     self.LBInput_renderer]
        self.input_handlers = [self.menu_screen,
                          self.game_loop,
                          self.custom_menu,
                          self.leaderboard_input]
        
        self.game = GameFrame(self.input_handlers, self.renderers, self.leaderboard_repository)


    def test_will_save_score_in_database(self):
        self.menu_screen.add_return_value(0)
        self.menu_screen.add_return_value(0)
        self.game_loop.add_return_value((1,0))
        self.leaderboard_input.add_return_value("name")
        self.menu_screen.add_return_value(-1)

        self.game.menu()

        self.assertEqual(len(self.leaderboard_repository.get_scores("Custom")), 1)
        self.assertEqual(self.leaderboard_repository.get_scores("Easy")[0], ("name", "Easy", 0))






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
            elif key == pygame.K_9:
                self.unicode = "9"
        self.key = key
        self.button = key
        self.pos = pos
        self.type = event_type

class StubEventQueue:
    def __init__(self, events=[]):
        self._events = events

    def add_event(self, event):
        self._events.append(event)
        self._events.append(StubEvent(None))

    def get(self):
        if len(self._events) == 0:
            return []
        return [self._events.pop()]
    
    def wait(self):
        if len(self._events) == 0:
            return
        return self._events.pop()


class StubRendererToo:
    def __init__(self, timeline, name, rects=None):
        self.timeline = timeline
        self.name = name
        self.rect_list = rects
        self.level = None

    def render(self):
        if len(self.timeline) == 0:
            self.timeline.append(self.name)
        if self.timeline[-1] != self.name:
            self.timeline.append(self.name)

    def get_rect_info(self):
        return self.rect_list
    
    def set_rects(self, rects):
        self.rect_list = rects
    
    def set_active(self, number):
        pass

    def set_text(self, text, number):
        pass

    def set_time(self, time):
        pass

    def set_level(self, level, size):
        self.level = level

    def get_level(self):
        return self.level

    def set_scores(self, diff):
        pass

class TestWholeGame(unittest.TestCase):
    #Testejä vain pari, koska tässä testataan vaan, että luokat toimii yhdessä eikä itse luokkien toimintaa
    #Myöskin vaikeata testata, voin vain seurata missä rendrereissä on käyty ja en voi kunnolla ennakoida pelin kulkua
    def setUp(self):
        self.visiting_timeline = []
        self.menu_renderer = StubRendererToo(self.visiting_timeline, "menu",
                                          [pygame.rect.Rect(100, 200, 550, 75),pygame.rect.Rect(100, 300, 550, 75), pygame.rect.Rect(100, 400, 550, 75)])
        self.level_renderer = StubRendererToo(self.visiting_timeline, "level")
        self.diff_renderer = StubRendererToo(self.visiting_timeline, "diff",
                                          [pygame.rect.Rect(100, 200, 550, 75),pygame.rect.Rect(100, 300, 550, 75), pygame.rect.Rect(100, 400, 550, 75)])
        self.custom_renderer = StubRendererToo(self.visiting_timeline, "custom",
                                            [["16", False, pygame.rect.Rect(70, 250, 200, 75)],["16", False, pygame.rect.Rect(380, 250, 200, 75)], ["30", False, pygame.rect.Rect(70, 450, 400, 75)]])
        self.LB_renderer = StubRendererToo(self.visiting_timeline, "LB", [])
        self.LBSelection_renderer = StubRendererToo(self.visiting_timeline, "LBSelection",
                                                 [pygame.rect.Rect(100, 200, 550, 75),pygame.rect.Rect(100, 300, 550, 75), pygame.rect.Rect(100, 400, 550, 75),pygame.rect.Rect(100, 500, 550, 75)] )
        self.LBInput_renderer = StubRendererToo(self.visiting_timeline, "LBInput",
                                             [["", False, pygame.Rect(70, 450, 400, 75)]])
        
        self.menu_events = StubEventQueue()
        self.game_events = StubEventQueue()
        self.custom_events = StubEventQueue()
        self.leaderboard_events = StubEventQueue()

        self.menu_screen = MenuScreen(None, self.menu_events, StubClock())
        self.game_loop = GameLoop(None, None, self.game_events, StubClock())
        self.custom_menu = CustomDifficulty(None, self.custom_events, StubClock())
        self.leaderboard_input = LeaderboardInput(None, self.leaderboard_events, StubClock())

        self.leaderboard_repository = LeaderboardRepository(database_connection.get_database_connection())

        self.renderers = [self.menu_renderer,
                     self.level_renderer,
                     self.diff_renderer,
                     self.custom_renderer,
                     self.LB_renderer,
                     self.LBSelection_renderer,
                     self.LBInput_renderer]
        self.input_handlers = [self.menu_screen,
                          self.game_loop,
                          self.custom_menu,
                          self.leaderboard_input]
        
        self.game = GameFrame(self.input_handlers, self.renderers, self.leaderboard_repository)

    def test_can_quit_game(self):
        self.menu_events.add_event(StubEvent(pygame.QUIT))

        self.game.menu()

        visitings = ["menu"]

        for i in range(len(self.visiting_timeline)):
            self.assertEqual(self.visiting_timeline[i], visitings[i])

    def test_can_start_game(self):
        self.game_events.add_event(StubEvent(pygame.QUIT))
        self.menu_events.add_event(StubEvent(pygame.MOUSEBUTTONDOWN, 1, (105,205)))
        self.menu_events.add_event(StubEvent(pygame.MOUSEBUTTONDOWN, 1, (105,205)))


        self.game.menu()

        visitings = ["menu", "diff", "level"]

        for i in range(len(visitings)):
            self.assertEqual(self.visiting_timeline[i], visitings[i])
    
    def test_can_play_game(self):
        self.menu_events.add_event(StubEvent(pygame.QUIT))
        self.game_events.add_event(StubEvent(pygame.MOUSEBUTTONUP, 1, (25,25)))
        self.game_events.add_event(StubEvent(pygame.MOUSEBUTTONDOWN, 1, (25,25)))
        self.custom_events.add_event(StubEvent(pygame.KEYDOWN, pygame.K_RETURN))
        self.custom_events.add_event(StubEvent(pygame.KEYDOWN, pygame.K_9))
        self.custom_events.add_event(StubEvent(pygame.KEYDOWN, pygame.K_9))
        self.custom_events.add_event(StubEvent(pygame.KEYDOWN, pygame.K_9))
        self.custom_events.add_event(StubEvent(pygame.MOUSEBUTTONDOWN, 1, (75,455)))
        self.menu_events.add_event(StubEvent(pygame.MOUSEBUTTONDOWN, 1, (105,305)))

        self.game.menu()

        visitings = ["menu", "custom", "level", "menu"]

        for i in range(len(visitings)):
            self.assertEqual(self.visiting_timeline[i], visitings[i])

    def test_can_open_leaderboard_and_return(self):
        self.menu_events.add_event(StubEvent(pygame.QUIT))
        self.menu_events.add_event(StubEvent(pygame.KEYDOWN, pygame.K_ESCAPE))
        self.menu_events.add_event(StubEvent(pygame.KEYDOWN, pygame.K_ESCAPE))
        self.menu_events.add_event(StubEvent(pygame.MOUSEBUTTONDOWN, 1, (105,205)))
        self.menu_events.add_event(StubEvent(pygame.MOUSEBUTTONDOWN, 1, (105,405)))

        self.game.menu()

        visitings = ["menu", "LBSelection", "LB", "LBSelection", "menu"]

        for i in range(len(visitings)):
            self.assertEqual(self.visiting_timeline[i], visitings[i])