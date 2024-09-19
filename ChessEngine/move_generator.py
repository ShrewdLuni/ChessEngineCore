from ChessEngine.move import Move
from ChessEngine import move_flags
from ChessEngine import piece


class MoveGenerator:
    def __init__(self, board, precomputed_data):
        self.moves = []
        self.board = board

        self.friendly_color = piece.WHITE if board.color_to_move == "w" else piece.BLACK
        self.opponent_color = piece.BLACK if board.color_to_move == "w" else piece.WHITE

        self.precomputed_data = precomputed_data

    def generate_legal_moves(self):
        self.friendly_color = piece.WHITE if self.board.color_to_move == "w" else piece.BLACK
        self.opponent_color = piece.BLACK if self.board.color_to_move == "w" else piece.WHITE
        self.moves = []
        self.generate_moves()

    def generate_moves(self):
        for index in range(64):
            current_piece = self.board.square[index]
            if current_piece == 0:
                continue
            if piece.is_color(current_piece, self.friendly_color):
                piece_type = piece.get_piece_type(current_piece)
                if piece_type == piece.PAWN:
                    self.generate_pawn_moves(index)
                elif piece_type == piece.KING:
                    self.generate_king_moves(index)
                elif piece_type == piece.KNIGHT:
                    self. generate_knight_moves(index)
                else:
                    self.generate_sliding_moves(index, piece_type)

    def generate_pawn_moves(self, starting_square):
        is_white = piece.is_color(self.board.square[starting_square], piece.WHITE)

        edges = self.precomputed_data.edges[starting_square]
        edges = [edges[0], edges[4], edges[6]] if is_white else [edges[1], edges[5], edges[7]]

        pawn_move_offset = -8 if is_white else 8
        pawn_capture_offsets = [-9, -7] if is_white else [7, 9]

        target_square = starting_square + pawn_move_offset
        if self.board.square[target_square] == 0:
            if edges[0] == 1:
                self.generate_promotion_moves(starting_square, target_square)
            else:
                self.moves.append(Move(starting_square, target_square))
            target_square += pawn_move_offset
            if edges[0] == 6 and self.board.square[target_square] == 0:
                self.moves.append(Move(starting_square, target_square, move_flags.pawn_two_forward))

        for i in range(len(pawn_capture_offsets)):
            target_square = starting_square + pawn_capture_offsets[i]
            if self.board.en_passant != -1 and target_square - pawn_move_offset == self.board.en_passant:
                self.moves.append(Move(starting_square, target_square, move_flags.en_passant_capture))
            elif piece.is_color(self.board.square[target_square], self.opponent_color) and edges[i + 1] > 0:
                if edges[0] == 1:
                    self.generate_promotion_moves(starting_square, target_square)
                else:
                    self.moves.append(Move(starting_square, target_square))

    def generate_promotion_moves(self, starting_square, target_square):
        self.moves.append(Move(starting_square, target_square, move_flags.promote_to_queen))
        self.moves.append(Move(starting_square, target_square, move_flags.promote_to_knight))
        self.moves.append(Move(starting_square, target_square, move_flags.promote_to_rook))
        self.moves.append(Move(starting_square, target_square, move_flags.promote_to_bishop))

    def generate_king_moves(self, starting_square):
        for direction_index in range(len(piece.KING_DIRECTIONS)):
            target_square = starting_square + piece.KING_DIRECTIONS[direction_index]
            if self.precomputed_data.edges[direction_index] == 0 or piece.is_color(self.board.square[target_square], self.friendly_color):
                continue
            self.moves.append(Move(starting_square, target_square))

    def generate_knight_moves(self, starting_square):
        for direction in self.precomputed_data.knight_moves[starting_square]:
            target_square = starting_square + direction
            if piece.is_color(self.board.square[target_square], self.friendly_color):
                continue
            self.moves.append(Move(starting_square, target_square))

    def generate_sliding_moves(self, starting_square, piece_type):
        starting_direction_index = 4 if piece_type == piece.BISHOP else 0
        end_direction_index = 4 if piece_type == piece.ROOK else 8
        for direction_index in range(starting_direction_index, end_direction_index):
            for n in range(self.precomputed_data.edges[starting_square][direction_index]):
                target_square = starting_square + piece.KING_DIRECTIONS[direction_index] * (n + 1)

                piece_on_target_square = self.board.square[target_square]

                if piece.is_color(piece_on_target_square, self.friendly_color):
                    break

                self.moves.append(Move(starting_square, target_square))

                if piece.is_color(piece_on_target_square, self.opponent_color):
                    break
