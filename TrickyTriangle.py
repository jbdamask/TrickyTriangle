import random
import logging
import enum
import copy
import sys

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
        self.empty_hole = -1
        self.create_board_map()

    def create_board_map(self):
        """Generate the playing board"""
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

    def check_direction(self, hole):
        """Determine the directions each board position can move (these are fixed to the board, not peg)

        :param hole: Virtual hole on playing board
        :return:
        """
        index, row, column = hole
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

    def add_pegs(self, empty_position=None):
        """Place virtual pegs onto the board

        :param empty_position:
        """
        if empty_position is None:
            self.empty_hole = random.randint(0, self.size - 1)  # Set a random board position as empty
        else:
            if empty_position > self.size:
                raise Exception('fixed_position variable greater than board size. Try again')
            self.empty_hole = empty_position
        log_it("Empty positions: " + str(self.empty_hole))
        for row in self.map:
            for hole in row:
                position = hole[0]
                hole.append(False) if position == self.empty_hole else hole.append(True)  # PEG = True; EMPTY = False
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
        moves = [] # List of move_dict
        for d in directions:
            move_dict = {}  # Dict of position indexes: Current, Adjacent, Destination
            adjacent_hole = self.get_board_position(d, True, hole)
            destination_hole = self.get_board_position(d, False, hole)
            if self.flat_map[adjacent_hole][4] and not self.flat_map[destination_hole][4]:
                move_dict.update({"Current": index, "Adjacent": adjacent_hole, "Destination": destination_hole})
                moves.append(move_dict)
        return moves

    def choose_move(self, move_options):
        """Contains logic for selecting a game move

        :param move_options: Dictionary of possible moves for a given game state
        :return selection: Dictionary of selected move to make
        """
        selection = random.choice(list(move_options))
        return selection

    def move_peg(self, move):
        """Flips occupied bits for three holes: current, adjacent, destination

        :param move: Dict of the move to make
        """
        self.flat_map[move["Current"]][4] = False
        self.flat_map[move["Adjacent"]][4] = False
        self.flat_map[move["Destination"]][4] = True

    def dump_map(self):
        for i in self.map:
            print(*i)  # Pythonic syntax to unpack lists


def print_winner(game_moves):
    """Show the winning moves

    :param game_moves: Dict of recorded moves that won the game
    """
    for g in game_moves:
        print(str(g['Current'] + 1) + " -> " + str(g['Destination'] + 1))


#======================#
# LET THE GAMES BEGIN! #
#======================#
def main(args):
    # Side length should be >= 5
    arg1 = int(args[1]) if len(args) > 1 else 5
    arg2 = int(args[2])-1 if len(args) == 3 else None
    b = Board(arg1)
    if arg2+1 > b.size:
        print("You entered " + str(arg2+1) + " for the empty spot but the highest possible value is " + str(b.size))
        print("Try again!")
        sys.exit(1)
    b.add_pegs(arg2)
    games = 1
    print("Board size " + str(b.size))
    print("Starting with empty hole: " + str(b.empty_hole + 1))
    while True:
        # One iteration equals one game
        game_moves = []
        b2 = copy.deepcopy(b)  # Copy our board for non-destructive game play
        for i in range(0, b2.size):
            moves = {} # For each board state, there's a list of moves to consider
            for hole in b2.flat_map: # Determine all possible board moves
                if hole[4]: # If hole has peg, let's see where it can move
                    m = b2.determine_game_moves(hole)
                    for mv in m:
                        moves[hole[0]] = mv
            if len(moves) > 0:
                the_chosen = b2.choose_move(moves)
                c = moves[the_chosen]
                game_moves.append(c)
                b2.move_peg(c)
                i += 1
            else:
                break
        games += 1
        if len(game_moves) == b2.max_moves:
            print("Game " + str(games) + " is a winner!")
            print_winner(game_moves)
            break

if __name__ == "__main__":
    main(sys.argv)