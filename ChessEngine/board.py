from ChessEngine import piece


class Board:
    def __init__(self):
        self.square = [0] * 64
        self.color_to_move = "w"
        self.castling = [1, 1, 1, 1]
        self.en_passant = -1
        self.half_move_clock = 0
        self.full_move_number = 1

        self.state_stack = []

        self.__castling_mappings = {
            62: ([63, 61], (0, 1)),  # White Kingside
            58: ([56, 59], (0, 1)),  # White Queenside
            6: ([0, 5], (2, 3)),  # Black Kingside
            2: ([7, 3], (2, 3)),  # Black Queenside
        }
        self.__rook_castling_map = {63: 0, 56: 1, 0: 2, 7: 3}

        self.fen_to_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

        self.is_checkmate = False

    def fen_to_board(self, fen_string):
        self.is_checkmate = False
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
        self.castling = castling
        if fields[3] != "-":

            self.en_passant = (ord(fields[3][0]) - 97) + (8 * (8 - int(fields[3][1])))

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
                for i in range(int(char)):
                    self.square[index] = 0
                    index += 1
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
        castling = "-" if castling == "" else castling
        en_passant = "-"
        if self.en_passant != -1:
            en_passant = ["a", "b", "c", "d", "e", "f", "g", "h"][self.en_passant % 8] + str(8 - (self.en_passant // 8))

        return f'{pieces_position} {self.color_to_move} {castling} {en_passant} {self.half_move_clock} {self.full_move_number}'

    def make_move(self, starting_square, target_square, flag=0):
        self.state_stack.append([
            (starting_square, self.square[starting_square]),  # Index 0: (starting square, piece)
            (target_square, self.square[target_square]),  # Index 1: (target square, piece)
            flag,  # Index 2: flag
            (self.en_passant, self.square[self.en_passant]),  # Index 3: en passant
            self.castling[:],  # Index 4: castling rights
            self.color_to_move  # Index 5: color to move
        ])

        match flag:
            case 0:
                self.square[target_square] = self.square[starting_square]
                if any(self.castling):
                    piece_type = piece.get_piece_type(self.square[starting_square])
                    if piece_type == piece.KING:
                        color_index = 0 if piece.is_color(self.square[starting_square], piece.WHITE) else 2
                        self.castling[color_index] = self.castling[color_index + 1] = 0
                    elif piece_type == piece.ROOK:
                        castling_index = self.__rook_castling_map.get(starting_square)
                        if castling_index is not None:
                            self.castling[castling_index] = 0
            case 1:
                self.square[target_square] = self.square[starting_square]
                self.square[self.en_passant] = piece.NOTHING
            case 2:
                self.square[target_square] = self.square[starting_square]
                if target_square in self.__castling_mappings:
                    rook_from_to, castling_indices = self.__castling_mappings[target_square]
                    self.castling[castling_indices[0]] = 0
                    self.castling[castling_indices[1]] = 0
                self.square[rook_from_to[1]] = self.square[rook_from_to[0]]
                self.square[rook_from_to[0]] = piece.NOTHING
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

        if flag != 7:
            self.en_passant = -1

        self.square[starting_square] = piece.NOTHING
        self.color_to_move = "w" if self.color_to_move == "b" else "b"

    def unmake_move(self):
        if len(self.state_stack) == 0:
            return

        last_state = self.state_stack.pop()

        starting_square, starting_piece = last_state[0]
        target_square, target_piece = last_state[1]
        self.en_passant = last_state[3][0]
        self.castling = last_state[4]
        self.color_to_move = last_state[5]

        self.square[starting_square] = starting_piece
        self.square[target_square] = target_piece

        flag = last_state[2]
        if flag == 1:
            self.square[self.en_passant] = last_state[3][1]
        elif flag == 2:
            if target_square in self.__castling_mappings:
                rook_from_to, castling_indices = self.__castling_mappings[target_square]
                self.castling[castling_indices[0]] = 1
                self.castling[castling_indices[1]] = 1

            self.square[rook_from_to[0]] = self.square[rook_from_to[1]]
            self.square[rook_from_to[1]] = piece.NOTHING
