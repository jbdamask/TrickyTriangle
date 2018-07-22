import random
import logging
from operator import eq, le, ge

logging.basicConfig(level=logging.DEBUG)

class Board:
    def __init__(self, side_length):
        self.side_length = side_length
        self.size = int((side_length * (side_length + 1)) / 2)
        self.map = []
        self.empty_positions = []
        self.create_board_map()

    def create_board_map(self):
        # Set a random board position as empty
        # Note coder is expected to use off-the-shelf components for solved problems like random numbers
        self.empty_positions.append(random.randint(0, self.size-1))
        print(self.empty_positions[0])
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


def check_spot(operand_left, operator, operand_right):
    return operator(operand_left, operand_right)


def check_move(item):
   # print(item)
    index, row, column, occupied_status = item
    if occupied_status:
        for i in move_directions:
            if i == 'LEFT':
                if check_spot((column-2), ge, 0):
                    log_it(RC(row, column) + " left ok")
            if i == 'RIGHT':
                if check_spot((column + 2), le, row):
                    log_it(RC(row, column) + " right ok")
            if i == 'UP-LEFT':
                if check_spot((column - 2), ge, 0):
                    if check_spot((row - 2), ge, 0):
                        log_it(RC(row, column) + " up-left ok")
            if i == 'UP-RIGHT':
                if check_spot((column + 2), le, row):
                    if check_spot((row - 2), le, row):
                        log_it(RC(row, column) + " up-right ok")
            if i == 'DOWN-LEFT':
               pass
            if i == 'DOWN-RIGHT':
                pass

b = Board(5)
#b.dump_map()
# Stores individual moves. Originating positions are stored in the odd elements and destinations are in even
# A full game will in in a list of size (b.size - 1)*2
moves = []
win_ledger = []  # Stores a list of games (i.e. as many moves lists that end with one peg left as are computed)

move_directions = ['LEFT', 'RIGHT', 'UP-LEFT', 'UP-RIGHT', 'DOWN-LEFT', 'DOWN-RIGHT']

for x in b.map:
    for item in x:
        check_move(item)
#
#    position, row, occupied = x
    # for y in range(0, len(x)+1):
    #     print (y)

#    check_move (b.map[5])


