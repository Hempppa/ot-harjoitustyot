import pygame
from sprites.cell import CellCover, CellZero, CellOne, CellTwo, CellThree, CellFour, CellFive, CellSix, CellSeven, CellEight, CellNine
from sprites.flag import Flag
from sprites.highlight import Highlight


class Level:
    def __init__(self, mineField, cell_size):
        self.cell_size = cell_size

        self.cellCovers = pygame.sprite.Group()

        self.cellZero = pygame.sprite.Group()
        self.cellOne = pygame.sprite.Group()
        self.cellTwo = pygame.sprite.Group()
        self.cellThree = pygame.sprite.Group()
        self.cellFour = pygame.sprite.Group()
        self.cellFive = pygame.sprite.Group()
        self.cellSix = pygame.sprite.Group()
        self.cellSeven = pygame.sprite.Group()
        self.cellEight = pygame.sprite.Group()
        self.cellNine = pygame.sprite.Group()

        self.flags = pygame.sprite.Group()
        self.highlights = pygame.sprite.Group()

        self.all_other_cells = pygame.sprite.Group()
        self.allCells = pygame.sprite.Group()
        self.pairings = {}

        self._initialize_sprites(mineField)

    def _initialize_sprites(self, mineField):
        for y in range(len(mineField)):
            for x in range(len(mineField[0])):
                cell = mineField[y][x]
                x_position = x*self.cell_size
                y_position = y*self.cell_size

                # These are covers for the cells
                cover = CellCover(x_position, y_position)
                self.cellCovers.add(cover)

                if cell == 0:
                    temp = CellZero(x_position, y_position)
                    self.pairings[(x, y)] = (temp, cover)
                    self.cellZero.add(CellZero(x_position, y_position))
                elif cell == 1:
                    temp = CellOne(x_position, y_position)
                    self.pairings[(x, y)] = (temp, cover)
                    self.cellOne.add(temp)
                elif cell == 2:
                    temp = CellTwo(x_position, y_position)
                    self.pairings[(x, y)] = (temp, cover)
                    self.cellTwo.add(temp)
                elif cell == 3:
                    temp = CellThree(x_position, y_position)
                    self.pairings[(x, y)] = (temp, cover)
                    self.cellThree.add(temp)
                elif cell == 4:
                    temp = CellFour(x_position, y_position)
                    self.pairings[(x, y)] = (temp, cover)
                    self.cellFour.add(temp)
                elif cell == 5:
                    temp = CellFive(x_position, y_position)
                    self.pairings[(x, y)] = (temp, cover)
                    self.cellFive.add(temp)
                elif cell == 6:
                    temp = CellSix(x_position, y_position)
                    self.pairings[(x, y)] = (temp, cover)
                    self.cellSix.add(temp)
                elif cell == 7:
                    temp = CellSeven(x_position, y_position)
                    self.pairings[(x, y)] = (temp, cover)
                    self.cellSeven.add(temp)
                elif cell == 8:
                    temp = CellEight(x_position, y_position)
                    self.pairings[(x, y)] = (temp, cover)
                    self.cellEight.add(temp)
                elif cell == 9:
                    temp = CellNine(x_position, y_position)
                    self.pairings[(x, y)] = (temp, cover)
                    self.cellNine.add(temp)
        self.all_other_cells.add(self.cellZero, self.cellOne, self.cellTwo, self.cellThree, self.cellFour, self.cellFive, self.cellSix, self.cellSeven, self.cellEight, self.cellNine)

    def cellClicked(self, buttons, pos):
        if buttons[0]:
            for cell in self.all_other_cells:
                if cell.rect.collidepoint(pos):
                    return self.reveal(cell)
        else:
            for cover in self.cellCovers:
                if cover.rect.collidepoint(pos):
                    return self.flag(cover)

    def gameOver(self):
        self.cellCovers.empty()
        for flag in self.flags:
            self.highlights.add(Highlight(flag.rect.x, flag.rect.y))
        self.flags.empty()
        return 0

    def flag(self, cover):
        if cover.flagged == None:
            if len(self.flags) < len(self.cellNine):
                newFlag = Flag(cover.rect.x, cover.rect.y)
                self.flags.add(newFlag)
                cover.flagged = newFlag
                # mahdollinen ilmoitus lippujen loppumisesta
        else:
            currentFlag = cover.flagged
            self.flags.remove(currentFlag)
            cover.flagged = None
        return

    def reveal(self, cell):
        if cell.covered:
            y = cell.rect.y//self.cell_size
            x = cell.rect.x//self.cell_size
            if self.pairings[(x, y)][1].flagged != None:
                return True
            if type(cell) == CellNine:
                return self.gameOver()
            cell.covered = False
            if type(cell) == CellZero:
                for i in range(3):
                    for j in range(3):
                        if (x+j-1, y+i-1) in self.pairings:
                            self.reveal(self.pairings[(x+j-1, y+i-1)][0])
            self.cellCovers.remove(self.pairings[(x, y)][1])

        if len(self.cellCovers.sprites()) == len(self.cellNine.sprites()):
            return 1
        return
