from mapGenerator import mapGen
from level import Level
import unittest


class TestLevel(unittest.TestCase):
    def setUp(self):
        self.mineField1 = mapGen()
        self.mineField2 = [[1, 1, 1],
                           [1, 9, 1],
                           [1, 1, 1]]
        self.mineField3 = [[0, 0, 0],
                           [0, 0, 0],
                           [0, 0, 0]]
        self.sprite_handler1 = Level(self.mineField1.field, 50)
        self.sprite_handler2 = Level(self.mineField2, 50)
        self.sprite_handler3 = Level(self.mineField3, 50)

    def test_correct_amount_of_cell_sprites(self):
        # 1 handler
        self.assertEqual(
            len(self.sprite_handler1.all_other_cells.sprites()), 16*16)

    def test_correct_sprite_types(self):
        # 2
        self.assertEqual(len(self.sprite_handler2.cellOne.sprites()), 8)
        self.assertEqual(len(self.sprite_handler2.cellNine.sprites()), 1)

    def test_correct_amount_of_cell_covers(self):
        # 1
        self.assertEqual(len(self.sprite_handler1.cellCovers.sprites()), len(
            self.sprite_handler1.all_other_cells.sprites()))

    def test_pairing_works(self):
        # 1
        for pair in self.sprite_handler1.pairings:
            location = self.sprite_handler1.pairings[pair]
            cell = location[0]
            cover = location[1]
            self.assertEqual(cell.rect.x, cover.rect.x)
            self.assertEqual(cell.rect.y, cover.rect.y)

    def test_clearing_numbered_cell_works(self):
        # 2
        self.assertEqual(self.sprite_handler2.cellClicked((True, False, False), (25, 25)), True)
        self.assertEqual(len(self.sprite_handler2.cellCovers.sprites()), 8)

    def test_clearing_empty_cell_clears_more(self):
        # 3
        self.assertEqual(self.sprite_handler3.cellClicked((True, False, False), (25, 25)), False)
        self.assertEqual(len(self.sprite_handler3.cellCovers.sprites()), 0)

    def test_clearing_a_mine_ends_game(self):
        # 2
        self.assertEqual(self.sprite_handler2.cellClicked((True, False, False), (75, 75)), False)
        self.assertEqual(len(self.sprite_handler2.cellCovers.sprites()), 0)

    def test_gameover_clears_board(self):
        # 2
        self.assertEqual(self.sprite_handler2.gameOver(), False)
        self.assertEqual(len(self.sprite_handler2.cellCovers.sprites()), 0)
