import random

from ChessEngine import piece
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

    def new_game(self):
        self.set_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def set_position(self, fen):
        self.board.fen_to_board(fen)

    def make_move(self, starting_square, target_square, flag=0):
        self.board.make_move(starting_square, target_square, flag)

    def unmake_move(self):
        self.board.unmake_move()

    def get_random_move(self):
        moves = self.move_generator.generate_legal_moves()
        random_move = moves[random.randint(0, len(moves) - 1)]
        self.board.make_move(random_move.get_starting_square(), random_move.get_target_square(), random_move.get_move_flag())
        return random_move

    def get_best_move(self, search_time = 2.0):
        alpha = self.search_function.iterative_deepening(15, search_time)
        best_move = self.search_function.best_move
        if best_move:
            self.board.make_move(best_move.get_starting_square(), best_move.get_target_square(), best_move.get_move_flag())
        return {"move": best_move, "evaluation": self.search_function.best_move_evaluation}

    def get_legal_moves(self):
        moves = self.move_generator.generate_legal_moves()
        if len(moves) == 0:
            self.board.is_checkmate = self.board_utility.is_check(piece.WHITE if self.board.color_to_move == "w" else piece.BLACK)
        return moves

    def get_current_evaluation(self):
        return self.evaluation.evaluate()

    def move_generation_test(self, depth, is_root=False):
        if is_root:
            self.move_results = {}
        if depth == 0:
            return {"count": 1, "moves": {}}
        moves = self.move_generator.generate_legal_moves()
        positions = 0
        for move in moves:
            move = [move.get_starting_square(), move.get_target_square(), move.get_move_flag()]
            self.board.make_move(move[0], move[1], move[2])
            count = self.move_generation_test(depth - 1)["count"]
            if is_root:
                file_map = ["a", "b", "c", "d", "e", "f", "g", "h"]
                one = file_map[move[0] % 8] + str(8 - (move[0] // 8))
                two = file_map[move[1] % 8] + str(8 - (move[1] // 8))
                move_notation = f"{one}{two}"
                self.move_results[move_notation] = count

            positions += count
            self.board.unmake_move()

        return {"count": positions, "moves": {k: self.move_results[k] for k in sorted(self.move_results)}}
