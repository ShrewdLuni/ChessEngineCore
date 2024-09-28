from ChessEngine import piece
from ChessEngine import piece_square_table


class Evaluation:
    def __init__(self, board):
        self.pieces_value_map = {
            piece.PAWN: 100,
            piece.KNIGHT: 300,
            piece.BISHOP: 300,
            piece.ROOK: 500,
            piece.QUEEN: 900,
            piece.KING: 2000
        }
        self.pawn_position = [0] * 64

        self.board = board

    ### alpha version used for proto, will be changed later to something more advanced
    def evaluate(self):
        evaluation = self.calculate_material_difference()
        return evaluation

    def calculate_material_difference(self):
        material_difference = 0
        for index in range(64):
            current_piece = self.board.square[index]
            if current_piece == 0:
                continue
            value = self.pieces_value_map[piece.get_piece_type(current_piece)]
            value += piece_square_table.piece_position_map[current_piece][index]
            material_difference += value if piece.is_color(current_piece, piece.WHITE) else -value

        return material_difference if self.board.color_to_move == "w" else -material_difference
