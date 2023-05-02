from levelgeneration.map_generator import MapGen
from levelgeneration.level import Level
import unittest

MINEFIELD_1 = MapGen(9, 9, 9)
MINEFIELD_2 = [[1, 1, 1],
               [1, 9, 1],
               [1, 1, 1]]
MINEFIELD_3 = [[0, 0, 0],
               [0, 0, 0],
               [0, 0, 0]]
MINEFIELD_4 = [[9, 9, 9, 9, 9, 9, 2, 1, 1],
               [9, 8, 9, 7, 6, 5, 4, 9, 2],
               [9, 9, 9, 9, 9, 9, 9, 3, 9]]

class TestLevel(unittest.TestCase):
    def setUp(self):
        self.sprite_handler1 = Level(MINEFIELD_1.field, 50)
        self.sprite_handler2 = Level(MINEFIELD_2, 50)
        self.sprite_handler3 = Level(MINEFIELD_3, 50)
        self.sprite_handler4 = Level(MINEFIELD_4, 50)

    def test_correct_amount_of_cell_sprites(self):
        self.assertEqual(len(self.sprite_handler1.all_cells), 9*9)

    def test_correct_sprite_types(self):
        self.assertEqual(len(self.sprite_handler2.cells_numbers), 8)
        self.assertEqual(len(self.sprite_handler2.cells_nine), 1)

    def test_correct_amount_of_cell_covers(self):
        self.assertEqual(len(self.sprite_handler1.cell_covers), len(self.sprite_handler1.all_cells))

    def test_pairing_works(self):
        for pair in self.sprite_handler1.pairings:
            location = self.sprite_handler1.pairings[pair]
            cell = location[0]
            cover = location[1]
            self.assertEqual(cell.rect.x, cover.rect.x)
            self.assertEqual(cell.rect.y, cover.rect.y)

    def test_clearing_numbered_cell_works(self):
        self.assertEqual(self.sprite_handler2.cell_clicked(1, (25, 25)), 10)
        self.assertEqual(len(self.sprite_handler2.cell_covers), 8)

    def test_clearing_empty_cell_clears_more(self):
        self.assertEqual(self.sprite_handler3.cell_clicked(1, (25, 25)), 1)
        self.assertEqual(len(self.sprite_handler3.cell_covers), 0)

    def test_clearing_a_mine_ends_game(self):
        self.assertEqual(self.sprite_handler2.cell_clicked(1, (75, 75)), 0)
        self.assertEqual(len(self.sprite_handler2.cell_covers), 0)

    def test_zero_flags_at_start(self):
        self.assertEqual(len(self.sprite_handler1.flags), 0)

    def test_gameover_modifies_board(self):
        self.sprite_handler2.cell_clicked(3, (25, 25))
        self.assertEqual(self.sprite_handler2.game_over(), 0)
        self.assertEqual(len(self.sprite_handler2.cell_covers), 0)

    def test_flagging_cells_works(self):
        self.assertEqual(self.sprite_handler1.cell_clicked(3, (25, 25)), 10)
        self.assertEqual(len(self.sprite_handler1.flags), 1)
        self.assertEqual(self.sprite_handler1.flag(self.sprite_handler1.pairings[(0, 1)][1]), None)
        self.assertEqual(len(self.sprite_handler1.flags), 2)

    def test_cant_have_more_flags_than_mines(self):
        self.assertEqual(self.sprite_handler2.flag(self.sprite_handler2.pairings[(0, 1)][1]), None)
        self.assertEqual(len(self.sprite_handler2.flags), 1)
        self.assertEqual(self.sprite_handler2.flag(self.sprite_handler2.pairings[(1, 1)][1]), None)
        self.assertEqual(len(self.sprite_handler2.flags), 1)

    def test_cant_clear_flagged_cell(self):
        self.sprite_handler1.cell_clicked(3, (25, 25))
        self.sprite_handler1.cell_clicked(1, (25, 25))
        self.assertEqual(len(self.sprite_handler1.cell_covers), len(self.sprite_handler1.all_cells))
        self.assertEqual(len(self.sprite_handler1.flags), 1)

    def test_can_remove_flag(self):
        self.sprite_handler1.cell_clicked(3, (25, 25))
        self.sprite_handler1.cell_clicked(3, (25, 25))
        self.assertEqual(len(self.sprite_handler1.flags), 0)
