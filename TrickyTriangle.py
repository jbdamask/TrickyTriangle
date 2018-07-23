import random
import logging
from operator import le, ge, lt
import enum

logging.basicConfig(level=logging.INFO)


class Directions(enum.Enum):
    LEFT = 1
    RIGHT = 2
    UP_LEFT = 3
    UP_RIGHT = 4
    DOWN_LEFT = 5
    DOWN_RIGHT = 6


class Board:
    def __init__(self, side_length):
        self.side_length = side_length
        self.size = int((side_length * (side_length + 1)) / 2)
        self.map = []
        self.empty_positions = []
        self.create_board_map()

    def create_board_map(self, fixed_position=None):
        # Set a random board position as empty
        # Note coder is expected to use off-the-shelf components for solved problems like random numbers
        if fixed_position is None:
            self.empty_positions.append(random.randint(0, self.size - 1))
        else:
            if fixed_position > self.size:
                raise Exception('fixed_position variable greater than board size. Try again')
            self.empty_positions.append(fixed_position)
        log_it(self.empty_positions[0])
        counter = 0
        for r in range(0, self.side_length):
            row = []
            if counter == 0:
                hole = [counter, 0, 0]
                directions = self.check_direction(hole)
                hole.append(directions)
                row.append(hole)
                counter += 1
            else:
                for c in range(0, r + 1):
                    hole = [counter, r, c]
                    directions = self.check_direction(hole)
                    hole.append(directions)
                    row.append(hole)
                    counter += 1
            self.map.append(row)

    def dump_map(self):
        for i in self.map:
            print(*i)  # Pythonic syntax to unpack lists

    def check_empty(self, position):
        return 1 if position in self.empty_positions else 0

    def check_spot(self, operand_left, operator, operand_right):
        return operator(operand_left, operand_right)

    # For a given triangle hole, determine possible moves
    def check_direction(self, item):
        index, row, column = item
        directions = []
        if self.check_spot((column - 2), ge, 0):
            directions.append(Directions.LEFT)
        if self.check_spot((column + 2), le, row):
            directions.append(Directions.RIGHT)
        if row >= 2 and self.check_spot((column - 2), ge, 0):
            directions.append(Directions.UP_LEFT)
        if row >= 2 and self.check_spot((column + 2), le, row):
            directions.append(Directions.UP_RIGHT)
        if self.check_spot((row + 2), lt, self.side_length):
            directions.append(Directions.DOWN_LEFT)
            directions.append(Directions.DOWN_RIGHT)
        return directions


# Returns a row / column string for printing
def RC(r, c):
    return "R" + str(r) + "C" + str(c)


def log_it(message):
    logging.debug(message)


b = Board(3)
#b.dump_map()
# Stores individual moves. Originating positions are stored in the odd elements and destinations are in even
# A full game will in in a list of size (b.size - 1)*2
moves = []
win_ledger = []  # Stores a list of games (i.e. as many moves lists that end with one peg left as are computed)
