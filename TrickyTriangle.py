import random
import logging
from operator import eq, le, ge, lt

logging.basicConfig(level=logging.INFO)

class Board:
    def __init__(self, side_length):
        self.side_length = side_length
        self.size = int((side_length * (side_length + 1)) / 2)
        self.map = []
        self.empty_positions = []
        self.create_board_map()
        self.move_directions = ['LEFT', 'RIGHT', 'UP-LEFT', 'UP-RIGHT', 'DOWN-LEFT', 'DOWN-RIGHT']

    def create_board_map(self, fixed_position=None):
        # Set a random board position as empty
        # Note coder is expected to use off-the-shelf components for solved problems like random numbers
        if fixed_position is None:
            self.empty_positions.append(random.randint(0, self.size-1))
        else:
            if fixed_position > self.size:
                raise Exception('fixed_position variable greater than board size. Try again')
            self.empty_positions.append(fixed_position)
        log_it(self.empty_positions[0])
        counter = 0
        for r in range(0, self.side_length ):
            row = []
            if counter == 0:
                row.append([ counter, 0, 0, self.check_empty(counter) ])
                counter += 1
            else:
                for c in range(0, r + 1):
                    row.append( [ counter, r, c, self.check_empty(counter) ] )
                    counter += 1
            self.map.append(row)

    def dump_map(self):
        for i in self.map:
            print(*i)  # Pythonic syntax to unpack lists

    def check_empty(self, position):
        return 1 if position in self.empty_positions else 0

    def check_spot(self, operand_left, operator, operand_right):
        return operator(operand_left, operand_right)

    def check_move(self, item):
        index, row, column, occupied_status = item
        if occupied_status:
            for i in self.move_directions:
                if i == 'LEFT':
                    if self.check_spot((column - 2), ge, 0):
                        log_it(RC(row, column) + " left ok")
                if i == 'RIGHT':
                    if self.check_spot((column + 2), le, row):
                        log_it(RC(row, column) + " right ok")
                if i == 'UP-LEFT':
                    if self.check_spot((column - 2), ge, 0):
                        if self.check_spot((row - 2), ge, 0):
                            log_it(RC(row, column) + " up-left ok")
                if i == 'UP-RIGHT':
                    if row >= 2:
                        if self.check_spot((column + 2), le, row):
                            log_it(RC(row, column) + " up-right ok")
                # Downward moves are only concerned with rows as column numbers increase
                if i == 'DOWN-LEFT' or i == 'DOWN-RIGHT':
                    if self.check_spot((row + 2), lt, self.side_length):
                        log_it(RC(row, column) + " down-left ok")



# Returns a row / column string for printing
def RC(r,c):
    return "R" + str(r) + "C" + str(c)


def log_it(message):
    logging.debug(message)


# def check_horizontal(operand_left, operator, operand_right):
#     return operator(operand_left, operand_right)
#
#
# def check_vertical(operand_left, operator, operand_right):
#     return operator(operand_left, operand_right)




b = Board(7)
#b.dump_map()
# Stores individual moves. Originating positions are stored in the odd elements and destinations are in even
# A full game will in in a list of size (b.size - 1)*2
moves = []
win_ledger = []  # Stores a list of games (i.e. as many moves lists that end with one peg left as are computed)


for x in b.map:
    for item in x:
        b.check_move(item)
#
#    position, row, occupied = x
    # for y in range(0, len(x)+1):
    #     print (y)

#    check_move (b.map[5])


