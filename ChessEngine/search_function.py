import time


class SearchFunction:
    def __init__(self, board, move_generator, evaluation):
        self.board = board
        self.move_generator = move_generator
        self.evaluation = evaluation
        self.best_move_this_iteration = None
        self.best_move = None

        self.start_time = None
        self.time_limit = 1


    def iterative_deepening(self, max_depth, time_limit):
        self.time_limit = time_limit
        self.start_time = time.time()
        self.best_move_this_iteration = None
        print("---------")
        for depth in range(1, max_depth + 1):
            if time.time() - self.start_time >= self.time_limit:
                break
            alpha = self.search(depth, -float('inf'), float('inf'), is_root=True)
            if self.best_move_this_iteration:
                self.best_move = self.best_move_this_iteration
            start = ["a", "b", "c", "d", "e", "f", "g", "h"][self.best_move.get_starting_square() % 8] + str(8 - (self.best_move.get_starting_square() // 8))
            target = ["a", "b", "c", "d", "e", "f", "g", "h"][self.best_move.get_target_square() % 8] + str(8 - (self.best_move.get_target_square() // 8))
            print(depth, alpha, start + target)

        return self.best_move

    def search(self, depth, alpha, beta, is_root=False):
        if time.time() - self.start_time >= self.time_limit:
            return 0

        if depth == 0:
            return self.evaluation.evaluate()

        moves = self.move_generator.generate_legal_moves()
        if is_root and self.best_move_this_iteration:
            moves.insert(0, self.best_move_this_iteration)

        if len(moves) == 0:
            if True: #check
                return float('-inf')
            return 0 #stalemate

        for move in moves:
            self.board.make_move(move.get_starting_square(), move.get_target_square(), move.get_move_flag())
            evaluation = -self.search(depth - 1, -beta, -alpha)
            self.board.unmake_move()
            if time.time() - self.start_time >= self.time_limit:
                return 0

            if evaluation >= beta:
                return beta
            if evaluation > alpha:
                alpha = evaluation
                if is_root:
                    self.best_move_this_iteration = move

        return alpha
