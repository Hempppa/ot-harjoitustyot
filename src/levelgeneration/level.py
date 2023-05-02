import pygame
from sprites.cell import CellCover, CellZero, CellOne, CellTwo, CellThree
from sprites.cell import CellFour, CellFive, CellSix, CellSeven, CellEight, CellNine
from sprites.flag import Flag
from sprites.highlight import Highlight

class Level:
    """Tämä luokka hallitsee pelin Spritejä joita rendereri tulee piirtämään

    Attributes:
        cell_covers: Ruutujen peitteen, yksi jokaista ruutua kohti alussa
        cells_zero: Ruudut joihin ei tule numeroa
        cells_numbers: Ruudut joissa on jokin numero
        cells_nine: ruudut joissa on 9 eli miinat
        all_cells: ruudut 0-9, eli kaikki ns pohjat
        pairings: taulukko, jossa pidetään kirjaa ruuduista ja niiden peitteistä
        flags: kaikki liput, joita on alussa nolla
        cell_size: ruutujen koko
    """
    def __init__(self, minefield, cell_size=50):
        """Luodaan ryhmät joihin spriten sijoitetaan

        Args:
            minefield list: MapGenin luoma numerokartta, joka on lista listoja joista 
                            jokainen on rivi kentällä 
            cell_size int: yhden ruudun koko, vakiona 50
        """
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
        """Luodaan karttaa vastaavat spritet, kartaa vastaaville paikoille

        Args:
            minefield: sama kuin konstruktorin kartta
        """
        width = len(minefield[0])
        heigth = len(minefield)
        for i in range(heigth):
            for j in range(width):
                cell = minefield[i][j]
                x_position = j*self.cell_size
                y_position = i*self.cell_size

                cover = CellCover(x_position, y_position)
                self.cell_covers.add(cover)

                numbered_cell = self.determine_cell_number(cell, x_position, y_position)
                self.pairings[(j, i)] = (numbered_cell, cover)
        self.all_cells.add(self.cells_zero, self.cells_numbers, self.cells_nine)

    def determine_cell_number(self, cell, x_position, y_position):
        """Jatkaa liian pitkää funktion toimintaa, päättelee onko tyhjä, miina vai numero.
        Luo Spriten ja lisää sen ryhmään

        Args:
            cell int: ruudun arvo
            x_position int: leveys sijainti
            y_position int: korkeus sijainti

        Returns:
            temp: Sprite olio
        """
        if cell == 0:
            temp = CellZero(x_position, y_position)
            self.cells_zero.add(temp)
        elif cell == 9:
            temp = CellNine(x_position, y_position)
            self.cells_nine.add(temp)
        else:
            temp = self.cell_numbers_one_through_eight(cell, x_position, y_position)
            self.cells_numbers.add(temp)
        return temp

    def cell_numbers_one_through_eight(self, cell, x_position, y_position):
        """Jatkoa jatkolle, muodostaa 1-8 Spritet

        Args:
            cell int: ruudun arvo
            x_position int: leveys sijainti
            y_position int: korkeus sijainti

        Returns:
            temp Sprite: palauttaa muodostetun Spriten
        """
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

    def cell_clicked(self, button, pos):
        """Pelissä painettu hiiren nappia "button" kohdassa "pos". Tarkistetaan millaiseen ruutuun
        osuttiin ja mitä sille tehdään

        Args:
            button tuple(Bool,Bool,Bool): tuple jossa on kolme booleania edustamassa 
                                          hiiren kolmea nappia
            pos tuple(x,y): napinpainalluksen sijainti

        Returns:
            int: 10, 0 tai 1, 10 peli jatkuu, 0 peli hävittiin, 1 peli voitettiin
        """
        if button == 1:
            for cell in self.all_cells:
                if cell.rect.collidepoint(pos):
                    return self.reveal(cell)
        elif button == 3:
            for cover in self.cell_covers:
                if cover.rect.collidepoint(pos):
                    self.flag(cover)
        return 10

    def game_over(self):
        """Muokkaa kenttää häviön takia

        Returns:
            int: 0 peli on hävitty
        """
        self.cell_covers.empty()
        temp = pygame.sprite.Group()
        for flag in self.flags:
            temp.add(Highlight(flag.rect.x, flag.rect.y))
        self.flags = temp
        return 0

    def flag(self, cover):
        """Muodostaa tai poistaa lipun haluttusta kohdasta

        Args:
            cover: Sprite jota painettiin
        """
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
        """Poistaa peitteitä ruuduista, myös cascade poisto huomioitu, kun ruutu = 0.
        Tarkistaa voiton ja häviön varalta.

        Args:
            cell: Ruutu jota painettiin

        Returns:
            int: 10, 1 tai 0; 10 peli jatkuu, 1 peli on voitettu, 0 peli hävittiin
        """
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
