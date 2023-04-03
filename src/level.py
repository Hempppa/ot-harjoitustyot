import pygame
from sprites.cell import CellCover, CellZero, CellOne, CellTwo, CellThree, CellFour, CellFive, CellSix, CellSeven, CellEight, CellNine

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

        self.all_other_cells = pygame.sprite.Group()
        self.pairings = {}

        self._initialize_sprites(mineField)

    def _initialize_sprites(self, mineField):
        for y in range(len(mineField.field)):
            for x in range(len(mineField.field[0])):
                cell = mineField.field[y][x]
                x_position = x*self.cell_size
                y_position = y*self.cell_size

                #These are covers for the cells
                cover = CellCover(x_position,y_position)
                self.cellCovers.add(cover)

                if cell == 0:
                    temp = CellZero(x_position,y_position)
                    self.pairings[(x,y)] = (temp, cover)
                    self.cellZero.add(CellZero(x_position,y_position))
                elif cell == 1:
                    temp = CellOne(x_position,y_position)
                    self.pairings[(x,y)] = (temp, cover)
                    self.cellOne.add(temp)
                elif cell == 2:
                    temp = CellTwo(x_position,y_position)
                    self.pairings[(x,y)] = (temp, cover)
                    self.cellTwo.add(temp)
                elif cell == 3:
                    temp = CellThree(x_position,y_position)
                    self.pairings[(x,y)] = (temp, cover)
                    self.cellThree.add(temp)
                elif cell == 4:
                    temp = CellFour(x_position,y_position)
                    self.pairings[(x,y)] = (temp, cover)
                    self.cellFour.add(temp)
                elif cell == 5:
                    temp = CellFive(x_position,y_position)
                    self.pairings[(x,y)] = (temp, cover)
                    self.cellFive.add(temp)
                elif cell == 6:
                    temp = CellSix(x_position,y_position)
                    self.pairings[(x,y)] = (temp, cover)
                    self.cellSix.add(temp)
                elif cell == 7:
                    temp = CellSeven(x_position,y_position)
                    self.pairings[(x,y)] = (temp, cover)
                    self.cellSeven.add(temp)
                elif cell == 8:
                    temp = CellEight(x_position,y_position)
                    sself.pairings[(x,y)] = (temp, cover)
                    self.cellEight.add(temp)
                elif cell == 9:
                    temp = CellNine(x_position,y_position)
                    self.pairings[(x,y)] = (temp, cover)
                    self.cellNine.add(temp)
        self.all_other_cells.add(self.cellZero, self.cellOne, self.cellTwo, self.cellThree, self.cellFour, self.cellFive, self.cellSix, self.cellSeven, self.cellEight, self.cellNine)

    def cellClicked(self, buttons, pos):
        if buttons[0]:
            for cell in self.all_other_cells:
                if cell.rect.collidepoint(pos):
                    if type(cell) == CellNine:
                        return self.gameOver()
                    else:
                        self.reveal(cell)
                        return True

    def gameOver(self):
        self.cellCovers.empty()
        return False

    def reveal(self, cell):
        if cell.covered:
            cell.covered = False
            y = cell.rect.y//self.cell_size
            x = cell.rect.x//self.cell_size
            if type(cell) == CellZero:
                for i in range(3):
                    for j in range(3):
                        if (x+j-1,y+i-1) in self.pairings:
                            self.reveal(self.pairings[(x+j-1,y+i-1)][0])
            self.cellCovers.remove(self.pairings[(x,y)][1])            
        