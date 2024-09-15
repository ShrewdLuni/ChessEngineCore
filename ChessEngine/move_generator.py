from ChessEngine.move import Move
from ChessEngine import piece


class MoveGenerator:
    def __init__(self, board, precomputed_data):
        self.moves = []
        self.board = board

        self.friendly_color = piece.WHITE
        self.opponent_color = piece.BLACK

        self.precomputed_data = precomputed_data

    def generate_legal_moves(self):
        self.generate_moves()

    def generate_moves(self):
        for index in range(64):
            current_piece = self.board.square[index]
            if current_piece == 0:
                continue
            if piece.is_color(current_piece, piece.WHITE):
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
        pass

    def generate_king_moves(self, starting_square):
        pass

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
