import os
import pygame
from config import FLAG_IMAGE

dirname = os.path.dirname(__file__)

class Flag(pygame.sprite.Sprite):
    """Pelissä lippua vastaava sprite

    Attributes:
        image: kuva joka spritelle ladataan
        rect: spriten sijainti ja koko
    """
    def __init__(self, _x=0, _y=0):
        super().__init__()
        self.image = pygame.image.load(
            os.path.join(dirname, "..", "assets", FLAG_IMAGE))
        self.rect = self.image.get_rect()
        self.rect.x = _x
        self.rect.y = _y
