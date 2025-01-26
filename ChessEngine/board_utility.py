from ChessEngine import piece


class BoardUtility:
    def __init__(self, board, move_generator):
        self.board = board
        self.move_generator = move_generator

    def is_check(self, color):
        king_position = next((i for i in range(64) if self.board.square[i] == piece.KING | color), [])
        if king_position == -1:
            return False
        self.board.color_to_move = "w" if self.board.color_to_move == "b" else "b"
        opponent_responses = self.move_generator.generate_moves()
        self.board.color_to_move = "w" if self.board.color_to_move == "b" else "b"
        if any(opponent_move.get_target_square() == king_position for opponent_move in opponent_responses):
            return True
        return False
