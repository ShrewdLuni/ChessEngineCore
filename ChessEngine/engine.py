import random

from board import Board
from moveGenerator import MoveGenerator

class Engine:
    def __init__(self):
        self.board = Board()
        self.moveGenerator = MoveGenerator(self.board)

    def GetRandomMove(self, FENString):
        self.board.FENtoBoard(FENString)
        self.moveGenerator.GenerateLegalMoves()

        randomMove = random.randint(0, len(self.moveGenerator.moves) - 1)
        return self.moveGenerator.moves[randomMove]