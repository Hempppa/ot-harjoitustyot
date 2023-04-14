import random


class MapGen():
    def __init__(self, width=16, height=16, mines=40) -> None:
        # Generat appropriate amount of fields (0) and mines(9)
        cells = [0]*((width*height)-mines) + [9]*mines
        random.shuffle(cells)

        # divide into equal lists to get a minefield
        self.field = []
        for i in range(height):
            self.field.append(cells[i*width:(i+1)*width])

        # numbering the minefield
        for i in range(height):
            for j in range(width):
                if self.field[i][j] != 9:
                    self.field[i][j] = self.count_mines(i, j)

    def count_mines(self, height, width):
        count = 0
        # check all cells in < 2 distance
        for i in range(3):
            for j in range(3):
                width_proper = j+width-1
                height_proper = i+height-1
                # if in bounds and a mine, increase count
                if not (0 <= height_proper < len(self.field)
                        and 0 <= width_proper < len(self.field[0])):
                    continue
                if self.field[height_proper][width_proper] == 9:
                    count += 1
        return count
