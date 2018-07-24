# TrickyTriangle

Find the optimum solution to Tricky Triangle of any size (but be prepared to wait if you specify a size > 8)

## Synopsis
Tricky Triangle is a physical game consisting of an equilateral triangle having 15 holes and 14 pegs.
The board is set up by placing the pegs in any of the available holes, leaving one hole open.
A peg can jump over another peg to an empty spot, removing the jumped peg in the process.
The game ends when there are no more possible moves.
To win the game, you need to have only one peg left on the board!

## TODO
* Extend to create a ledger of all possible ways to win a particular board configuration
* Add threads to handle solving large triangles
* Come up with different ways to choose the best move (currently random walk)
* Come up with a way to abort a game if it resembles a previously failed game (checksum for all moves at each position?)
* I create a 2D list to construct the board, then use a flattened version for moves. Consider doing everything in 1D
(though this doesn't add any value or even save any time)