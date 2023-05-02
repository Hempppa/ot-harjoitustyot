import os
import pygame
from config import TILE_0, TILE_1, TILE_2, TILE_3, TILE_4, TILE_5, TILE_6, TILE_7, TILE_8
from config import COVER_IMAGE, MINE_IMAGE

dirname = os.path.dirname(__file__)

class CellCover(pygame.sprite.Sprite):
    """pygame.sprite.Sprite olio ruutujen peitteille

    Attributes:
        image: kuvatiedosto, jolla sprite piirretään
        rect: Spriten sijainti ja koko
        flagged: pitää kirjaa onko peite liputettu
    """
    def __init__(self, _x=0, _y=0):
        """Konstruktori luo Spriten kohtaan (x,y) ja asettaa liputtoman tilan ruudulle. Kuva ladataan "assets" kansiosta config.py määritellyllä COVER_IMAGE nimellä

        Args:
            _x (int, optional): peitteen leveys sijainti. Defaults to 0.
            _y (int, optional): peitteen korkeus sijainti. Defaults to 0.
        """
        self.image = pygame.image.load(os.path.join(dirname, "..", "assets", COVER_IMAGE))
        super().__init__()
        self.rect = self.image.get_rect()
        self.rect.x = _x
        self.rect.y = _y
        self.flagged = None

class CellNumbered(pygame.sprite.Sprite):
    """Sama kuin peite, mutta numerot sinne peitteen alle, erona ainoastaan lippujen sijaan pidetään kirjaa onko peitettynä ja kuva on eri

    Attributes:
        covered: pitää kirjaa onko ruutu peitetty
    """
    def __init__(self, _x=0, _y=0):
        super().__init__()
        self.rect = self.image.get_rect()
        self.rect.x = _x
        self.rect.y = _y
        self.covered = True

class CellZero(CellNumbered):
    """Kaikki seuraavat perii CellNumbered luokan ja ainoana erona on kuva joka ladataan

    Attributes:
        image: kuvatiedosto, joka spritelle ladataan
    """
    def __init__(self,_x=0, _y=0):
        self.image = pygame.image.load(os.path.join(dirname, "..", "assets", TILE_0))
        super().__init__(_x, _y)

class CellOne(CellNumbered):
    def __init__(self,_x=0, _y=0):
        self.image = pygame.image.load(os.path.join(dirname, "..", "assets", TILE_1))
        super().__init__(_x, _y)

class CellTwo(CellNumbered):
    def __init__(self,_x=0, _y=0):
        self.image = pygame.image.load(os.path.join(dirname, "..", "assets", TILE_2))
        super().__init__(_x, _y)

class CellThree(CellNumbered):
    def __init__(self,_x=0, _y=0):
        self.image = pygame.image.load(os.path.join(dirname, "..", "assets", TILE_3))
        super().__init__(_x, _y)

class CellFour(CellNumbered):
    def __init__(self,_x=0, _y=0):
        self.image = pygame.image.load(os.path.join(dirname, "..", "assets", TILE_4))
        super().__init__(_x, _y)

class CellFive(CellNumbered):
    def __init__(self,_x=0, _y=0):
        self.image = pygame.image.load(os.path.join(dirname, "..", "assets", TILE_5))
        super().__init__(_x, _y)

class CellSix(CellNumbered):
    def __init__(self,_x=0, _y=0):
        self.image = pygame.image.load(os.path.join(dirname, "..", "assets", TILE_6))
        super().__init__(_x, _y)

class CellSeven(CellNumbered):
    def __init__(self,_x=0, _y=0):
        self.image = pygame.image.load(os.path.join(dirname, "..", "assets", TILE_7))
        super().__init__(_x, _y)

class CellEight(CellNumbered):
    def __init__(self,_x=0, _y=0):
        self.image = pygame.image.load(os.path.join(dirname, "..", "assets", TILE_8))
        super().__init__(_x, _y)

class CellNine(CellNumbered):
    def __init__(self,_x=0, _y=0):
        self.image = pygame.image.load(os.path.join(dirname, "..", "assets", MINE_IMAGE))
        super().__init__(_x, _y)
