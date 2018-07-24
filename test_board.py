import unittest
import random
from operator import eq, le, ge
from TrickyTriangle import Board, Directions

class TestBoard(unittest.TestCase):
    def test_create_board_map(self):
        b = Board(5)
        self.assertEqual(sum(len(x) for x in b.map), 15, "Triangle size not correct")

    def test_add_pegs(self):
        counter = 0
        number_tests = 100
        number_pass = 0
        i = 0
        while i < number_tests:
            side = random.randint(3, 15) # Create boards of different sizes (computed from side length)
            b = Board(side)
            empty_position = random.randint(0, b.size-1)
            b.add_pegs(empty_position)
            true_vals = 0
            for x in b.map:
                for item in x:
                    if item[4] == 0:
                        true_vals += 1
            if true_vals == 1:
                number_pass += 1
            else:
                break
            i += 1
        self.assertEqual(number_pass, number_tests, "More than one board position is empty on init")

    def test_directions(self):
        b = Board(7)
        directions = b.map[0][0][3]  # Top of triangle
        x = [self.assertFalse(Directions.LEFT in directions),
             self.assertFalse(Directions.RIGHT in directions),
             self.assertFalse(Directions.UP_LEFT in directions),
             self.assertFalse(Directions.UP_RIGHT in directions),
             self.assertTrue(Directions.DOWN_LEFT in directions),
             self.assertTrue(Directions.DOWN_RIGHT in directions)]

        self.assertEqual(str(x).count("None"), 6, "Expected 6 correct directions")

        directions = b.map[4][2][3] # Position 12 is the only one in a 7-triangle that can move in all 6 positions
        x = [self.assertTrue(Directions.LEFT in directions),
             self.assertTrue(Directions.RIGHT in directions),
             self.assertTrue(Directions.UP_LEFT in directions),
             self.assertTrue(Directions.UP_RIGHT in directions),
             self.assertTrue(Directions.DOWN_LEFT in directions),
             self.assertTrue(Directions.DOWN_RIGHT in directions)]

        self.assertEqual(str(x).count("None"), 6, "Expected 6 correct directions")

    def test_get_board_position(self):
        b = Board(7)
        b.add_pegs()

        hole = b.flat_map[0] # Get first hole on the board and check down_left
        self.assertEqual(b.get_board_position(hole[3][0], True, hole), 1, "Expected index 1")
        self.assertEqual(b.get_board_position(hole[3][0], False, hole), 3, "Expected index 3")

        hole = b.flat_map[12] # Get twelfth hole on the board and check various
        # Left
        self.assertEqual(b.get_board_position(hole[3][0], True, hole), 11, "Expected index 11")
        self.assertEqual(b.get_board_position(hole[3][0], False, hole), 10, "Expected index 10")
        # Right
        self.assertEqual(b.get_board_position(hole[3][1], True, hole), 13, "Expected index 13")
        self.assertEqual(b.get_board_position(hole[3][1], False, hole), 14, "Expected index 14")
        # Up left
        self.assertEqual(b.get_board_position(hole[3][2], True, hole), 7, "Expected index 7")
        self.assertEqual(b.get_board_position(hole[3][2], False, hole), 3, "Expected index 3")
        # Up right
        self.assertEqual(b.get_board_position(hole[3][3], True, hole), 8, "Expected index 8")
        self.assertEqual(b.get_board_position(hole[3][3], False, hole), 5, "Expected index 5")
        # Down left
        self.assertEqual(b.get_board_position(hole[3][4], True, hole), 17, "Expected index 17")
        self.assertEqual(b.get_board_position(hole[3][4], False, hole), 23, "Expected index 23")
        # Down right
        self.assertEqual(b.get_board_position(hole[3][5], True, hole), 18, "Expected index 18")
        self.assertEqual(b.get_board_position(hole[3][5], False, hole), 25, "Expected index 25")

    def test_determine_game_moves(self):
        b = Board(5)
        b.add_pegs(0) # Keep first hole open
        all_moves = {}
        for hole in b.flat_map:
            if hole[4]: # If hole has peg, let's see if it can move
                moves = b.determine_game_moves(hole)
                if len(moves) > 0:
                    all_moves[hole[0]] = moves
        self.assertTrue(len(all_moves), 2)
        self.assertEqual(all_moves[3][0], 0)
        self.assertEqual(all_moves[5][0], 0)