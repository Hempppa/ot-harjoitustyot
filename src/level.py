import pygame
from sprites.cell import CellCover, CellZero, CellOne, CellTwo, CellThree
from sprites.cell import CellFour, CellFive, CellSix, CellSeven, CellEight, CellNine
from sprites.flag import Flag
from sprites.highlight import Highlight

class Level:
    def __init__(self, minefield, cell_size):
        self.cell_covers = pygame.sprite.Group()

        self.cells_zero = pygame.sprite.Group()
        #1-8
        self.cells_numbers = pygame.sprite.Group()
        self.cells_nine = pygame.sprite.Group()
        self.all_cells = pygame.sprite.Group()
        self.pairings = {}

        self.flags = pygame.sprite.Group()
        self.cell_size = cell_size

        self._initialize_sprites(minefield)

    def _initialize_sprites(self, minefield):
        width = len(minefield[0])
        heigth = len(minefield)
        for i in range(heigth):
            for j in range(width):
                cell = minefield[i][j]
                x_position = j*self.cell_size
                y_position = i*self.cell_size

                # These are covers for the cells
                cover = CellCover(x_position, y_position)
                self.cell_covers.add(cover)

                numbered_cell = self.determine_cell_number(cell, x_position, y_position)
                self.pairings[(j, i)] = (numbered_cell, cover)
        self.all_cells.add(self.cells_zero, self.cells_numbers, self.cells_nine)

    def determine_cell_number(self, cell, x_position, y_position):
        if cell == 0:
            temp = CellZero(x_position, y_position)
            self.cells_zero.add(CellZero(x_position, y_position))
        elif cell == 9:
            temp = CellNine(x_position, y_position)
            self.cells_nine.add(temp)
        else:
            temp = self.cell_numbers_one_through_eight(cell, x_position, y_position)
            self.cells_numbers.add(temp)
        return temp

    def cell_numbers_one_through_eight(self, cell, x_position, y_position):
        if cell == 1:
            temp = CellOne(x_position, y_position)
        elif cell == 2:
            temp = CellTwo(x_position, y_position)
        elif cell == 3:
            temp = CellThree(x_position, y_position)
        elif cell == 4:
            temp = CellFour(x_position, y_position)
        elif cell == 5:
            temp = CellFive(x_position, y_position)
        elif cell == 6:
            temp = CellSix(x_position, y_position)
        elif cell == 7:
            temp = CellSeven(x_position, y_position)
        elif cell == 8:
            temp = CellEight(x_position, y_position)
        return temp

    def cell_clicked(self, buttons, pos):
        if buttons[0]:
            for cell in self.all_cells:
                if cell.rect.collidepoint(pos):
                    return self.reveal(cell)
        else:
            for cover in self.cell_covers:
                if cover.rect.collidepoint(pos):
                    self.flag(cover)
        return 10

    def game_over(self):
        self.cell_covers.empty()
        temp = pygame.sprite.Group()
        for flag in self.flags:
            temp.add(Highlight(flag.rect.x, flag.rect.y))
        self.flags = temp
        return 0

    def flag(self, cover):
        if cover.flagged is None:
            if len(self.flags) < len(self.cells_nine):
                new_flag = Flag(cover.rect.x, cover.rect.y)
                self.flags.add(new_flag)
                cover.flagged = new_flag
            # mahdollinen ilmoitus lippujen loppumisesta
        else:
            current_flag = cover.flagged
            self.flags.remove(current_flag)
            cover.flagged = None

    def reveal(self, cell):
        if not cell.covered:
            return 10
        int_y = cell.rect.y//self.cell_size
        int_x = cell.rect.x//self.cell_size
        if self.pairings[(int_x, int_y)][1].flagged is not None:
            return 10
        if isinstance(cell, CellNine):
            return self.game_over()
        cell.covered = False
        if isinstance(cell,CellZero):
            for i in range(9):
                add_x = i//3
                add_y = i%3
                if (int_x+add_x-1, int_y+add_y-1) in self.pairings:
                    self.reveal(self.pairings[(int_x+add_x-1, int_y+add_y-1)][0])
        self.cell_covers.remove(self.pairings[(int_x, int_y)][1])

        if len(self.cell_covers.sprites()) == len(self.cells_nine.sprites()):
            return 1
        return 10
