import random

from ChessEngine.board import Board
from ChessEngine.move_generator import MoveGenerator
from ChessEngine.precomputed_move_data import PrecomputedMoveData


class Engine:
    def __init__(self):
        self.board = Board()
        self.precomputed_move_data = PrecomputedMoveData()
        self.move_generator = MoveGenerator(self.board, self.precomputed_move_data)

    def get_random_move(self):
        self.move_generator.generate_legal_moves()
        random_move = self.move_generator.moves[random.randint(0, len(self.move_generator.moves) - 1)]
        self.board.make_move(random_move.starting_square, random_move.target_square)
        return random_move

    def get_legal_moves(self):
        self.move_generator.generate_legal_moves()
        return self.move_generator.moves

    def make_move(self, starting_square, target_square):
        self.board.make_move(starting_square, target_square)