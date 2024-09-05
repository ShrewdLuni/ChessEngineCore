from ChessEngine import piece


class Board:
    def __init__(self):
        self.square = [0] * 64
        self.color_to_move = "w"

    def fen_to_board(self, fen_string):
        fen_to_piece = {
            'k': piece.KING,
            'q': piece.QUEEN,
            'r': piece.ROOK,
            'b': piece.BISHOP,
            'n': piece.KNIGHT,
            'p': piece.PAWN,
        }

        index = 0
        fields = fen_string.split(" ")
        position = fields[0]
        self.color_to_move = fields[1]

        for char in position:
            if char.isdigit():
                index += int(char)
            elif char != "/":
                piece_color = piece.WHITE if char.isupper() else piece.BLACK
                piece_type = fen_to_piece[char.lower()]

                self.square[index] = piece_type | piece_color
                index += 1
