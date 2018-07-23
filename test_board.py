import unittest
import random
from operator import eq, le, ge
from TrickyTriangle import Board


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
            size = random.randint(3, 8)
            b = Board(size)
            true_vals = 0
            for x in b.map:
                for item in x:
                    if item[3] == 1:
                        true_vals += 1
            if true_vals == 1:
                number_pass += 1
            else:
                break
            i += 1
        self.assertEqual(number_pass, number_tests, "More than one board position is empty on init")


    def test_check_moves(self):

        b = Board(7)
        b.create_board_map(1)  # Passing in fixed_position
        index, row, column, occupied_status = 0, 0, 0, 1
        # Test left
        self.assertFalse(b.check_spot((column - 2), ge, 0))
        # Test right
        self.assertFalse(b.check_spot((column + 2), le, row))
        # Test up-left
        self.assertFalse(b.check_spot((column - 2), ge, 0) and b.check_spot((row - 2), ge, 0))
        # Test up-right
        self.assertFalse(b.check_spot((column - 2), ge, 0) and b.check_spot((row - 2), ge, 0))
        # Test down-left
        self.assertTrue(row + 2 < b.side_length)

if __name__ == '__main__':
    unittest.main()