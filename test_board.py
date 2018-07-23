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


class TestChecksSetupA(unittest.TestCase):

    def setUp(self):
        self.b = Board(7)
        self.b.create_board_map(1)  # Passing in fixed_position
        self.index, self.row, self.column, self.occupied_status = 0, 0, 0, 1
        print("7-triangle: Position 0 empty")

    def test_check_left(self):
        # Test left
        self.assertFalse(self.b.check_spot((self.column - 2), ge, 0))

    def test_check_right(self):
        # Test right
        self.assertFalse(self.b.check_spot((self.column + 2), le, self.row))

    def test_check_up_left(self):
        # Test up-left
        self.assertFalse(self.b.check_spot((self.column - 2), ge, 0) and self.b.check_spot((self.row - 2), ge, 0))

    def test_check_up_right(self):
        # Test up-right
        self.assertFalse(self.b.check_spot((self.column - 2), ge, 0) and self.b.check_spot((self.row - 2), ge, 0))

    def test_check_down_left_and_right(self):
        # Test down-left and down-right (same logic)
        self.assertTrue(self.row + 2 < self.b.side_length)


class TestChecksSetupB(unittest.TestCase):

    def setUp(self):
        self.b = Board(7)
        self.b.create_board_map(12)  # Passing in fixed_position
        self.index, self.row, self.column, self.occupied_status = 9, 4, 2, 1

    def test_check_left(self):
        # Test left
        self.assertTrue(self.b.check_spot((self.column - 2), ge, 0))

    def test_check_right(self):
        # Test right
        self.assertTrue(self.b.check_spot((self.column + 2), le, self.row))

    def test_check_up_left(self):
        # Test up-left
        self.assertTrue(self.b.check_spot((self.column - 2), ge, 0) and self.b.check_spot((self.row - 2), ge, 0))

    def test_check_up_right(self):
        # Test up-right
        self.assertTrue(self.b.check_spot((self.column - 2), ge, 0) and self.b.check_spot((self.row - 2), ge, 0))

    def test_check_down_left_and_right(self):
        # Test down-left and down-right (same logic)
        self.assertTrue(self.row + 2 < self.b.side_length)

if __name__ == '__main__':
    unittest.main()