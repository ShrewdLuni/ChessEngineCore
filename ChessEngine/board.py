from ChessEngine import piece


class Board:
    def __init__(self):
        self.square = [0] * 64
        self.color_to_move = "w"
        self.castling = "KQkq"
        self.en_passant = "-"
        self.half_move_clock = 0
        self.full_move_number = 1
        self.fen_to_board("rnbqkbnr/8/8/8/8/8/8/RNBQKBNR w KQkq - 0 1")

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

    def fen_from_board(self):
        pieces_position = ""
        empty = 0

        piece_to_fen = {
            piece.KING: 'k',
            piece.QUEEN: 'q',
            piece.ROOK: 'r',
            piece.BISHOP: 'b',
            piece.KNIGHT: 'n',
            piece.PAWN: 'p',
        }

        for i in range(len(self.square)):
            current_square = self.square[i]
            if i % 8 == 0 and i != 0:
                if empty > 0:
                    pieces_position += str(empty)
                    empty = 0
                pieces_position += "/"

            if current_square == 0:
                empty += 1
                if empty == 8:
                    pieces_position += "8"
                    empty = 0
            else:
                if empty > 0:
                    pieces_position += str(empty)
                    empty = 0
                current_piece = str(piece_to_fen[piece.get_piece_type(current_square)])
                if piece.is_color(current_square, piece.WHITE):
                    current_piece = current_piece.upper()
                pieces_position += current_piece

        return f'{pieces_position} {self.color_to_move} {self.castling} {self.en_passant} {self.half_move_clock} {self.full_move_number}'

    def make_move(self, starting_square, target_square):
        self.square[target_square] = self.square[starting_square]
        self.square[starting_square] = piece.NOTHING
        self.color_to_move = "w" if self.color_to_move == "b" else "b"

    def unmake_move(self):
        pass
