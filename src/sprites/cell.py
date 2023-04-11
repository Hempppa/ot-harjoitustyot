import pygame
import os

dirname = os.path.dirname(__file__)

class CellCover(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.image = pygame.image.load(os.path.join(dirname, "..", "assets", "tile.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.flagged = None

class CellZero(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.image = pygame.image.load(os.path.join(dirname, "..", "assets", "tile0.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.covered = True

class CellOne(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.image = pygame.image.load(os.path.join(dirname, "..", "assets", "tile1.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.covered = True

class CellTwo(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.image = pygame.image.load(os.path.join(dirname, "..", "assets", "tile2.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.covered = True

class CellThree(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.image = pygame.image.load(os.path.join(dirname, "..", "assets", "tile3.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.covered = True

class CellFour(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.image = pygame.image.load(os.path.join(dirname, "..", "assets", "tile4.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.covered = True

class CellFive(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()

        self.image = pygame.image.load(os.path.join(dirname, "..", "assets", "tile5.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.covered = True

class CellSix(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()

        self.image = pygame.image.load(os.path.join(dirname, "..", "assets", "tile6.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.covered = True

class CellSeven(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()

        self.image = pygame.image.load(os.path.join(dirname, "..", "assets", "tile7.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.covered = True

class CellEight(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()

        self.image = pygame.image.load(os.path.join(dirname, "..", "assets", "tile8.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.covered = True

class CellNine(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()

        self.image = pygame.image.load(os.path.join(dirname, "..", "assets", "tile9.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.covered = True