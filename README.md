# TrickyTriangle

Find the optimum solution to Tricky Triangle of (theoretically) any size

## Requirements
Python 3.7

## Synopsis
* Default - Five holes per side, random empty starting position
** python TrickyTriangle.py
* Set board size to six holes per side
** python TrickyTriangle.py 6
* Set board size to eight holes per side and specific hole 1 as empty starting position
** python TrickyTriangle.py 8 1


## Description
Tricky Triangle is a physical game consisting of an equilateral triangle having 15 holes and 14 pegs.
The board is set up by placing the pegs in any of the available holes, leaving one hole open.
A peg can jump over another peg to an empty spot, removing the jumped peg in the process.
The game ends when there are no more possible moves.
To win the game, you need to have only one peg left on the board!

## TODO
* Come up with different ways to choose the best move (currently random walk)
* Extend to create a ledger of all possible ways to win a particular board configuration
* I create a 2D list to construct the board, then use a flattened version for moves. Consider doing everything in 1D
(though this doesn't add any value or even save any time)