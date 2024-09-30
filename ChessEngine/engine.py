import random

from ChessEngine.board import Board
from ChessEngine.move_generator import MoveGenerator
from ChessEngine.precomputed_move_data import PrecomputedMoveData
from ChessEngine.evaluation import Evaluation
from ChessEngine.search_function import SearchFunction
from ChessEngine.board_utility import BoardUtility

class Engine:
    def __init__(self):
        self.board = Board()
        self.precomputed_move_data = PrecomputedMoveData()
        self.move_generator = MoveGenerator(self.board, self.precomputed_move_data)
        self.evaluation = Evaluation(self.board)
        self.board_utility = BoardUtility(self.board, self.move_generator)
        self.search_function = SearchFunction(self.board, self.move_generator, self.evaluation, self.board_utility)
        self.move_results = {}

    def get_random_move(self):
        moves = self.move_generator.generate_legal_moves()
        random_move = moves[random.randint(0, len(moves) - 1)]
        self.board.make_move(random_move.get_starting_square(), random_move.get_target_square(), random_move.get_move_flag())
        return random_move

    def get_best_move(self):
        alpha = self.search_function.iterative_deepening(15, 2)
        best_move = self.search_function.best_move
        self.board.make_move(best_move.get_starting_square(), best_move.get_target_square(), best_move.get_move_flag())
        return best_move

    def get_legal_moves(self):
        return self.move_generator.generate_legal_moves()

    def make_move(self, starting_square, target_square, flag=0):
        self.board.make_move(starting_square, target_square, flag)

    def unmake_move(self):
        self.board.unmake_move()

    def move_generation_test(self, depth, is_root=False):
        if depth == 0:
            return 1
        moves = self.move_generator.generate_legal_moves()
        positions = 0
        for move in moves:
            move = [move.get_starting_square(), move.get_target_square(), move.get_move_flag()]
            self.board.make_move(move[0], move[1], move[2])
            count = self.move_generation_test(depth - 1)
            if is_root:
                file_map = ["a", "b", "c", "d", "e", "f", "g", "h"]
                one = file_map[move[0] % 8] + str(8 - (move[0] // 8))
                two = file_map[move[1] % 8] + str(8 - (move[1] // 8))
                move_notation = f"{one}{two}"
                self.move_results[move_notation] = count

            positions += count
            self.board.unmake_move()

        return positions
