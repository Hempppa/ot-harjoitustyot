import unittest
from map_generator import MapGen


class TestmapGenerator(unittest.TestCase):
    def setUp(self):
        self.mineField = MapGen(6, 7, 20)

    def test_correct_heigth(self):
        self.assertEqual(len(self.mineField.field), 7)

    def test_correct_width(self):
        for line in self.mineField.field:
            self.assertEqual(len(line), 6)

    def test_correct_mines_amount(self):
        mines = 0
        for line in self.mineField.field:
            mines += line.count(9)
        self.assertEqual(mines, 20)
