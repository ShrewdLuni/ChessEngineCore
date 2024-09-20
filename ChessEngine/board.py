from ChessEngine import piece

class Board:
    def __init__(self):
        self.square = [0] * 64
        self.color_to_move = "w"
        self.castling = [1, 1, 1, 1]
        self.en_passant = -1
        self.half_move_clock = 0
        self.full_move_number = 1

    def fen_to_board(self, fen_string):
        fields = fen_string.split(" ")
        position = fields[0]
        self.color_to_move = fields[1]
        self.half_move_clock = fields[4]
        self.full_move_number = fields[5]
        castling = [0, 0, 0, 0]
        if "K" in fields[2]:
            castling[0] = 1
        if "Q" in fields[2]:
            castling[1] = 1
        if "k" in fields[2]:
            castling[2] = 1
        if "q" in fields[2]:
            castling[3] = 1

        if fields[3] != "-":
            self.en_passant = (ord(position[0]) - 97) + (8 * (8 - int(position[1])))

        fen_to_piece = {
            'k': piece.KING,
            'q': piece.QUEEN,
            'r': piece.ROOK,
            'b': piece.BISHOP,
            'n': piece.KNIGHT,
            'p': piece.PAWN,
        }

        index = 0
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
        if empty > 0:
            pieces_position += str(empty)

        castling = ''.join([char for char, flag in zip("KQkq", self.castling) if flag == 1])
        en_passant = "-"
        if self.en_passant != -1:
            en_passant = ["h", "g", "f", "e", "d", "c", "b", "a"][(self.en_passant // 8) - 1] + str(self.en_passant % 8)

        return f'{pieces_position} {self.color_to_move} {castling} {en_passant} {self.half_move_clock} {self.full_move_number}'

    def make_move(self, starting_square, target_square, flag = 0):
        self.en_passant = -1

        match flag:
            case 0:
                self.square[target_square] = self.square[starting_square]
            case 1:
                self.square[target_square] = self.square[starting_square]
            case 2:
                pass
            case 3 | 4 | 5 | 6:
                piece_color = piece.WHITE if piece.is_color(self.square[starting_square], piece.WHITE) else piece.BLACK
                if flag == 3:
                    self.square[target_square] = piece.QUEEN | piece_color
                elif flag == 4:
                    self.square[target_square] = piece.KNIGHT | piece_color
                elif flag == 5:
                    self.square[target_square] = piece.ROOK | piece_color
                elif flag == 6:
                    self.square[target_square] = piece.BISHOP | piece_color
            case 7:
                self.en_passant = target_square
                self.square[target_square] = self.square[starting_square]

        self.square[starting_square] = piece.NOTHING
        self.color_to_move = "w" if self.color_to_move == "b" else "b"

    def unmake_move(self):
        pass
