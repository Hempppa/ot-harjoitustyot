import pygame
from main import GameFrame
from gamelogic.input_handlers import GameLoop, MenuScreen, CustomDifficulty
from gamelogic.input_handlers import LeaderboardInput
from gamelogic.event_queue import EventQueue
from gamelogic.clock import Clock
from repository.leaderboard_repository import LeaderboardRepository
import database_connection

from ui.renderers import MenuRenderer, LevelRenderer, DiffRenderer, CustomRenderer
from ui.renderers import LBInputRenderer, LBSelectionRenderer, LBRenderer

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Minesweeper")
    display = pygame.display.set_mode((750,750))
    leaderboard_repository = LeaderboardRepository(database_connection.get_database_connection())
    renderers = [
        MenuRenderer(display),
        LevelRenderer(display),
        DiffRenderer(display),
        CustomRenderer(display),
        LBRenderer(display, leaderboard_repository),
        LBSelectionRenderer(display),
        LBInputRenderer(display)
    ]
    input_handlers = [
        MenuScreen(None, EventQueue(), Clock()),
        GameLoop(None, None, EventQueue(), Clock()),
        CustomDifficulty(None, EventQueue(), Clock()),
        LeaderboardInput(None, EventQueue(), Clock())
    ]
    game = GameFrame(input_handlers, renderers, leaderboard_repository)
    game.menu()
