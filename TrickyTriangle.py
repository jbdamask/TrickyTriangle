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
        # To have one peg left on a board starting with one empty position,
        # the number of possible moves is 1 - number of pegs
        self.max_moves = self.size - 2
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

    # Determine the directions each board position can move (these are fixed to the board, not peg)
    def check_direction(self, item):
        index, row, column = item
        directions = []
        if (column - 2) >= 0:
            directions.append(Directions.LEFT)
        if (column + 2) <= row:
            directions.append(Directions.RIGHT)
        if row >= 2 and (column - 2) >= 0:
            directions.append(Directions.UP_LEFT)
        if row >= 2 and (column + 2) <= row:
            directions.append(Directions.UP_RIGHT)
        if (row + 2) < self.side_length:
            directions.append(Directions.DOWN_LEFT)
            directions.append(Directions.DOWN_RIGHT)
        return directions


    # Add pegs to all but one spot in the board
    # TODO This tightly couples holes and pegs. Not sure that's the best approach
    # Maybe it's ok...get rid of the peg concept and see moves as positional requests
    def add_pegs(self, empty_position=None):
        if empty_position is None:
            empty = random.randint(0, self.size - 1)  # Set a random board position as empty
        else:
            if empty_position > self.size:
                raise Exception('fixed_position variable greater than board size. Try again')
            empty = empty_position
        log_it("Empty positions: " + str(empty))
        for row in self.map:
            for hole in row:
                position = hole[0]
                hole.append(False) if position == empty else hole.append(True)  # PEG = True; EMPTY = False
        # Flattening the list to make re-positioning easier
        self.flat_map = [item for sublist in self.map for item in sublist]

    def get_board_position(self, direction, adjacent, hole):
        """Returns index of desired position

        :param direction: Direction considered
        :param adjacent: Boolean indicating if we're to look at position in between current and desired
        :param hole: Hole object
        :return: Board.flat_map index of requested position
        """
        index, row, column, directions, occupied = hole
        if direction == Directions.LEFT:
            return index - 1 if adjacent else index - 2
        if direction == Directions.RIGHT:
            return index + 1 if adjacent else index + 2
        if direction == Directions.UP_LEFT:
            return index - (row + 1) if adjacent else index - row - (row + 1)
        if direction == Directions.UP_RIGHT:
            return index - row if adjacent else index - row - (row - 1)
        if direction == Directions.DOWN_LEFT:
            return index + (row + 1) if adjacent else index + row + (row + 3)
        if direction == Directions.DOWN_RIGHT:
            return index + (row + 2) if adjacent else index + (row + 2) + (row + 3)

    # During a game, we figure out the list of actual moves a peg can make
    def determine_game_moves(self, hole):
        """Constructs the list of moves a peg can make during a game

        :param position: Object at a given spot on the board
        :return: List of possible moves
        """
        index, row, column, directions, occupied = hole

        moves = []  # List of position indexes we can move to
        for d in directions:
            adjacent_hole = self.get_board_position(d, True, hole)
            destination_hole = self.get_board_position(d, False, hole)
            if self.flat_map[adjacent_hole][4] and not self.flat_map[destination_hole][4]:
                moves.append(destination_hole)
        return moves

    def choose_move(self, move_options):
        """Contains logic for selecting a game move

        :param move_options: Dictionary of possible moves for a given game state
        :return selection: Dictionary of selected move to make
        """
        selection = random.choice(list(move_options))
        return selection

    def dump_map(self):
        for i in self.map:
            print(*i)  # Pythonic syntax to unpack lists


b = Board(5)
b.add_pegs()
#b.dump_map()
# Stores individual moves. Originating positions are stored in the odd elements and destinations are in even
# A full game will in in a list of size (b.size - 1)*2
game_moves = []
win_ledger = []  # Stores a list of games (i.e. as many moves lists that end with one peg left as are computed)

# Gameplay
#for i in range(0, b.max_moves):
for i in range(0, 1):
    moves = {}
    for hole in b.flat_map: # Determine all possible board moves
        if hole[4]: # If hole has peg, let's see where it can move
            m = b.determine_game_moves(hole)
            for mv in m:
                moves[hole[0]] = mv

                # for m in moves:
        #     print("Peg in position " + str(hole[0]) + " can move to position " + str(m))

    print(moves)
    the_chosen = b.choose_move(moves)
    c = {the_chosen: moves[the_chosen]}
    print(c)
    i += 1