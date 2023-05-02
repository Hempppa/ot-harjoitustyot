import random


class MapGen():
    """Generoi "kartan" annetuilla arvoilla, kartta on lista, listoista joista jokainen on rivi ja sisältää ruutuja edustavia numeroita

    Attributes:
        field: pelin kartta (sitä vastaava numeroita sisältävä listojen lista)
    """
    def __init__(self, width=16, height=16, mines=40):
        """Luo kentän annetuista arvoista. Luodaan oikea määrä miinoja, sekoitetaan ne, jaetaan kartta riveihin ja lasketaan muut numerot

        Args:
            width (int, optional): kentän leveys. Defaults to 16.
            height (int, optional): kentän korkeus. Defaults to 16.
            mines (int, optional): miinojen lkm. Defaults to 40.
        """
        cells = [0]*((width*height)-mines) + [9]*mines
        random.shuffle(cells)

        self.field = []
        for i in range(height):
            self.field.append(cells[i*width:(i+1)*width])

        for i in range(height):
            for j in range(width):
                if self.field[i][j] != 9:
                    self.field[i][j] = self.count_mines(i, j)

    def count_mines(self, height, width):
        """Laskee ruutuun oikean arvon

        Args:
            height int: korkeus sijainti
            width int: leveys sijainti

        Returns:
            int: 1-8, palauttaa viereisten miinojen lkm
        """
        count = 0
        for i in range(3):
            for j in range(3):
                width_proper = j+width-1
                height_proper = i+height-1
                if not (0 <= height_proper < len(self.field)
                        and 0 <= width_proper < len(self.field[0])):
                    continue
                if self.field[height_proper][width_proper] == 9:
                    count += 1
        return count
