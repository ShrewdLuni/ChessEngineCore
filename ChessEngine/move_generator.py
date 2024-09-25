from ChessEngine.move import Move
from ChessEngine import move_flags
from ChessEngine import piece


class MoveGenerator:
    def __init__(self, board, precomputed_data):
        self.board = board

        self.friendly_color = piece.WHITE if board.color_to_move == "w" else piece.BLACK
        self.opponent_color = piece.BLACK if board.color_to_move == "w" else piece.WHITE

        self.precomputed_data = precomputed_data

    def generate_legal_moves(self):
        self.friendly_color = piece.WHITE if self.board.color_to_move == "w" else piece.BLACK
        self.opponent_color = piece.BLACK if self.board.color_to_move == "w" else piece.WHITE

        moves = self.generate_moves()
        legal_moves = []
        color = self.friendly_color
        for move in moves:
            self.board.make_move(move.get_starting_square(), move.get_target_square(), move.get_move_flag())
            king_position = next(i for i in range(64) if self.board.square[i] == piece.KING | color)
            opponent_responses = self.generate_moves()
            if move.get_move_flag() == 2:
                castle_index = self.precomputed_data.castling_data[0].index(move.get_target_square())
                to_check = self.precomputed_data.castling_data[3][castle_index]
                if any(opponent_move.get_target_square() in to_check for opponent_move in self.generate_moves()):
                    self.board.unmake_move()
                    continue
            if not any(opponent_move.get_target_square() == king_position for opponent_move in opponent_responses):
                legal_moves.append(move)
            self.board.unmake_move()
        return legal_moves

    def generate_moves(self):
        self.friendly_color = piece.WHITE if self.board.color_to_move == "w" else piece.BLACK
        self.opponent_color = piece.BLACK if self.board.color_to_move == "w" else piece.WHITE
        moves = []
        for index in range(64):
            current_piece = self.board.square[index]
            if current_piece == 0:
                continue
            if piece.is_color(current_piece, self.friendly_color):
                piece_type = piece.get_piece_type(current_piece)
                if piece_type == piece.PAWN:
                    moves.extend(self.generate_pawn_moves(index))
                elif piece_type == piece.KING:
                    pass
                    moves.extend(self.generate_king_moves(index))
                elif piece_type == piece.KNIGHT:
                    moves.extend(self.generate_knight_moves(index))
                else:
                    moves.extend(self.generate_sliding_moves(index, piece_type))
        return moves

    def generate_pawn_moves(self, starting_square):
        moves = []
        is_white = piece.is_color(self.board.square[starting_square], piece.WHITE)

        edges = self.precomputed_data.edges[starting_square]
        edges = [edges[0], edges[4], edges[6]] if is_white else [edges[1], edges[5], edges[7]]

        pawn_move_offset = -8 if is_white else 8
        pawn_capture_offsets = [-9, -7] if is_white else [7, 9]

        target_square = starting_square + pawn_move_offset
        if self.board.square[target_square] == 0:
            if edges[0] == 1:
                moves.extend(self.generate_promotion_moves(starting_square, target_square))
            else:
                moves.append(Move(starting_square, target_square))
            target_square += pawn_move_offset
            if edges[0] == 6 and self.board.square[target_square] == 0:
                moves.append(Move(starting_square, target_square, move_flags.pawn_two_forward))

        for i in range(len(pawn_capture_offsets)):
            target_square = starting_square + pawn_capture_offsets[i]
            if self.board.en_passant != -1 and target_square - pawn_move_offset == self.board.en_passant and edges[i + 1] > 0:
                moves.append(Move(starting_square, target_square, move_flags.en_passant_capture))
            elif piece.is_color(self.board.square[target_square], self.opponent_color) and edges[i + 1] > 0:
                if edges[0] == 1:
                    moves.extend(self.generate_promotion_moves(starting_square, target_square))
                else:
                    moves.append(Move(starting_square, target_square))
        return moves

    def generate_promotion_moves(self, starting_square, target_square):
        return [Move(starting_square, target_square, move_flags.promote_to_queen),
                Move(starting_square, target_square, move_flags.promote_to_knight),
                Move(starting_square, target_square, move_flags.promote_to_rook),
                Move(starting_square, target_square, move_flags.promote_to_bishop)]

    def generate_king_moves(self, starting_square):
        moves = []
        for direction_index in range(len(piece.KING_DIRECTIONS)):
            target_square = starting_square + piece.KING_DIRECTIONS[direction_index]
            if self.precomputed_data.edges[starting_square][direction_index] == 0:
                continue
            if piece.is_color(self.board.square[target_square], self.friendly_color):
                continue
            moves.append(Move(starting_square, target_square))

        starting_index = 0 if piece.is_color(self.board.square[starting_square], piece.WHITE) else 2
        for i in range(starting_index, starting_index + 2):
            if self.board.castling[i] == 1:
                castling_squares, rook_squares, free_squares = self.precomputed_data.castling_data[:3]
                if piece.get_piece_type(self.board.square[rook_squares[i]]) != piece.ROOK:
                    continue
                if not piece.is_color(self.board.square[rook_squares[i]], self.friendly_color):
                    continue
                if any(self.board.square[index] != piece.NOTHING for index in free_squares[i]):
                    continue
                moves.append(Move(starting_square, castling_squares[i], 2))
        return moves

    def generate_knight_moves(self, starting_square):
        moves = []
        for direction in self.precomputed_data.knight_moves[starting_square]:
            target_square = starting_square + direction
            if piece.is_color(self.board.square[target_square], self.friendly_color):
                continue
            moves.append(Move(starting_square, target_square))
        return moves

    def generate_sliding_moves(self, starting_square, piece_type):
        moves = []
        starting_direction_index = 4 if piece_type == piece.BISHOP else 0
        end_direction_index = 4 if piece_type == piece.ROOK else 8
        for direction_index in range(starting_direction_index, end_direction_index):
            for n in range(self.precomputed_data.edges[starting_square][direction_index]):
                target_square = starting_square + piece.KING_DIRECTIONS[direction_index] * (n + 1)

                piece_on_target_square = self.board.square[target_square]

                if piece.is_color(piece_on_target_square, self.friendly_color):
                    break

                moves.append(Move(starting_square, target_square))

                if piece.is_color(piece_on_target_square, self.opponent_color):
                    break
        return moves
