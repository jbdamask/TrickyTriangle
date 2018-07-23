import unittest
import random
from operator import eq, le, ge
from TrickyTriangle import Board, Directions

class TestBoard(unittest.TestCase):


    def test_create_board_map(self):
        b = Board(5)
        self.assertEqual(sum(len(x) for x in b.map), 15, "Triangle size not correct")

    def test_initial_empty_position_ok(self):
        counter = 0
        number_tests = 100
        number_pass = 0
        i = 0
        while i < number_tests:
            side = random.randint(3, 8) # Create boards of different sizes (computed from side length)
            board = Board(side)
            empty_position = random.randint(0, board.size-1)
            board.add_pegs(empty_position)
            true_vals = 0
            for x in board.map:
                for item in x:
                    if item[4] == 0:
                        true_vals += 1
            if true_vals == 1:
                number_pass += 1
            else:
                break
            i += 1
        self.assertEqual(number_pass, number_tests, "More than one board position is empty on init")


class TestChecksSetupC(unittest.TestCase):

    def setUp(self):
        self.b = Board(7)
        self.b.create_board_map()

    def test_wtf(self):
        directions = self.b.map[0][0][3]  # Top of triangle
        x = [self.assertFalse(Directions.LEFT in directions),
             self.assertFalse(Directions.RIGHT in directions),
             self.assertFalse(Directions.UP_LEFT in directions),
             self.assertFalse(Directions.UP_RIGHT in directions),
             self.assertTrue(Directions.DOWN_LEFT in directions),
             self.assertTrue(Directions.DOWN_RIGHT in directions)]

        self.assertEqual(str(x).count("None"), 6, "Expected 6 correct directions")

        directions = self.b.map[4][2][3] # Position 12 is the only one in a 7-triangle that can move in all 6 positions
        x = [self.assertTrue(Directions.LEFT in directions),
             self.assertTrue(Directions.RIGHT in directions),
             self.assertTrue(Directions.UP_LEFT in directions),
             self.assertTrue(Directions.UP_RIGHT in directions),
             self.assertTrue(Directions.DOWN_LEFT in directions),
             self.assertTrue(Directions.DOWN_RIGHT in directions)]

        self.assertEqual(str(x).count("None"), 6, "Expected 6 correct directions")


# if __name__ == '__main__':
#     unittest.main()