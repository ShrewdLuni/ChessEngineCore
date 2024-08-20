import ChessEngine.piece as Piece

class Board:
    def __init__(self):
        self.square = [0] * 64
        self.colorToMove = "w"


    def FENtoBoard(self, FENString):
        fen_to_piece = {
            'k': Piece.King,
            'q': Piece.Queen,
            'r': Piece.Rook,
            'b': Piece.Bishop,
            'n': Piece.Knight,
            'p': Piece.Pawn,
        }

        index = 0
        fields = FENString.split(" ")
        position = fields[0]
        self.colorToMove = fields[1]

        for char in position:
            if char.isdigit():
                index += int(char)
            elif char != "/":
                piece_color = Piece.White if char.isupper() else Piece.Black
                piece_type = fen_to_piece[char.lower()]

                self.square[index] = piece_type | piece_color
                index += 1
