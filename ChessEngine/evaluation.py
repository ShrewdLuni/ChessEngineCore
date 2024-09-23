from ChessEngine import piece


class Evaluation:
    def __init__(self):
        self.pawn_value = 1
        self.knight_value = 3
        self.bishop_value = 3
        self.rook_value = 5
        self.queen_value = 9

        self.pieces_value_map = {
            piece.PAWN: self.pawn_value,
            piece.KNIGHT: self.knight_value,
            piece.BISHOP: self.bishop_value,
            piece.ROOK: self.rook_value,
            piece.QUEEN: self.queen_value
        }

    ### alpha version used for proto, will be changed later to something more advanced
    def evaluate(self):
        evaluation = self.calculate_material_difference()
        return evaluation

    def calculate_material_difference(self):
        material_difference = 0
        for index in range(64):
            value = self.pieces_value_map[piece.get_piece_type(self.board.square[index])]
            material_difference += value if piece.is_color(self.board.square[index],piece.WHITE) else -value
        return material_difference
