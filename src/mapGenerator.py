import random


class mapGen():
    def __init__(self, x=16, y=16, mines=40) -> None:
        # Generato appropriate amount of empty fields (0) and mines(9)
        cells = [0]*((x*y)-mines) + [9]*mines
        random.shuffle(cells)

        # divide into equal lists to get a minefield
        self.field = []
        for i in range(y):
            self.field.append(cells[i*x:(i+1)*x])

        # numbering the minefield
        for y in range(len(self.field)):
            for x in range(len(self.field[0])):
                if self.field[y][x] != 9:
                    self.field[y][x] = self.countMines(y, x)

    def countMines(self, y, x):
        count = 0
        # check all cells in < 2 distance
        for i in range(3):
            for j in range(3):
                x_proper = j+x-1
                y_proper = i+y-1
                # if in bounds and a mine, increase count
                if 0 <= y_proper and y_proper < len(self.field) and 0 <= x_proper and x_proper < len(self.field[0]) and self.field[y_proper][x_proper] == 9:
                    count += 1
        return count


print(mapGen(6, 7, 20))
