import random
import logging
import enum

logging.basicConfig(level=logging.INFO)

def log_it(message):
    logging.debug(message)

# All possible ways a peg can move on the board
class Directions(enum.Enum):
    LEFT = 1
    RIGHT = 2
    UP_LEFT = 3
    UP_RIGHT = 4
    DOWN_LEFT = 5
    DOWN_RIGHT = 6


# The TrickyTriangle, its bad self
class Board:
    def __init__(self, side_length):
        self.side_length = side_length
        self.size = int((side_length * (side_length + 1)) / 2)
        self.map = []
        self.empty_positions = []
        self.create_board_map()

    def create_board_map(self):
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

    # Add pegs to all but one spot in the board
    # TODO This tightly couples holes and pegs. Not sure that's the best approach
    # Maybe it's ok...get rid of the peg concept and see moves as positional requests
    def add_pegs(self, empty_position=None):
        # Set a random board position as empty
        empty = -1
        if empty_position is None:
            empty = random.randint(0, self.size - 1)
        else:
            if empty_position > self.size:
                raise Exception('fixed_position variable greater than board size. Try again')
            empty = empty_position
        log_it("Empty positions: " + str(empty))
        for row in self.map:
            for hole in row:
                position = hole[0]
                hole.append(0) if position == empty else hole.append(1) # PEG = 1; EMPTY = 0

    # For a given triangle hole, determine possible moves
    def check_direction(self, item):
        index, row, column = item
        directions = []
        if (column-2) >= 0:
            directions.append(Directions.LEFT)
        if (column + 2) <= row:
            directions.append(Directions.RIGHT)
        if row >= 2 and (column -2) >= 0:
            directions.append(Directions.UP_LEFT)
        if row >= 2 and (column + 2) <= row:
            directions.append(Directions.UP_RIGHT)
        if (row + 2) < self.side_length:
            directions.append(Directions.DOWN_LEFT)
            directions.append(Directions.DOWN_RIGHT)
        return directions

    def dump_map(self):
        for i in self.map:
            print(*i)  # Pythonic syntax to unpack lists


# Returns a row / column string for printing
def RC(r, c):
    return "R" + str(r) + "C" + str(c)


b = Board(3)
b.add_pegs()
#b.dump_map()
# Stores individual moves. Originating positions are stored in the odd elements and destinations are in even
# A full game will in in a list of size (b.size - 1)*2
moves = []
win_ledger = []  # Stores a list of games (i.e. as many moves lists that end with one peg left as are computed)
