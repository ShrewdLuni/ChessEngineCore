import random

from board import Board
from move_generator import MoveGenerator
from ChessEngine.precomputed_move_data import PrecomputedMoveData


class Engine:
    def __init__(self):
        self.board = Board()
        self.precomputed_move_data = PrecomputedMoveData()
        self.move_generator = MoveGenerator(self.board, self.precomputed_move_data)

    def get_random_move(self, fen_string):
        self.board.fen_to_board(fen_string)
        self.move_generator.generate_legal_moves()

        random_move = random.randint(0, len(self.move_generator.moves) - 1)
        return self.move_generator.moves[random_move]
