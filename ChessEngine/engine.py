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
        moves = self.move_generator.generate_legal_moves()
        random_move = moves[random.randint(0, len(moves) - 1)]
        self.board.make_move(random_move.get_starting_square(), random_move.get_target_square(), random_move.get_move_flag())
        return random_move

    def get_legal_moves(self):
        return self.move_generator.generate_legal_moves()

    def make_move(self, starting_square, target_square, flag=0):
        self.board.make_move(starting_square, target_square, flag)

    def unmake_move(self):
        self.board.unmake_move()
