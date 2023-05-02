import os
import pygame
from config import HIGHLIGHT_IMAGE

dirname = os.path.dirname(__file__)


class Highlight(pygame.sprite.Sprite):
    """Nämä kehykset korvaavat liput pelin loputtua, jotta numeron tai miinankin näkee sen takaata

    Attributes:
        image: kuva joka spritelle ladataan
        rect: spriten sijainti ja koko
    """
    def __init__(self, _x=0, _y=0):
        super().__init__()
        self.image = pygame.image.load(os.path.join(
            dirname, "..", "assets", HIGHLIGHT_IMAGE))
        self.rect = self.image.get_rect()
        self.rect.x = _x
        self.rect.y = _y
