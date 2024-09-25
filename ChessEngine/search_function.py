class SearchFunction:
    def __init__(self, board, move_generator, evaluation):
        self.board = board
        self.move_generator = move_generator
        self.evaluation = evaluation
        self.best_move = None

    def search(self, depth, alpha, beta, is_root=False):
        if depth == 0:
            return self.evaluation.evaluate()

        moves = self.move_generator.generate_legal_moves()

        if len(moves) == 0:
            return float('-inf')

        for move in moves:
            self.board.make_move(move.get_starting_square(), move.get_target_square(), move.get_move_flag())
            evaluation = -self.search(depth - 1, -beta, -alpha)
            self.board.unmake_move()

            if evaluation >= beta:
                return beta

            if evaluation > alpha:
                alpha = evaluation
                if is_root:
                    self.best_move = move

        return alpha
