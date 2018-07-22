import unittest
import random
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



if __name__ == '__main__':
    unittest.main()