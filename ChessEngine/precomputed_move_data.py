from ChessEngine import piece


class PrecomputedMoveData:
    def __init__(self):
        self.edges = {}
        self.knight_moves = {}
        self.castling_data = ()
        self.precompute_move_data()

    def precompute_move_data(self):
        self.castling_data = (
            (62, 58, 6, 2),  # king target squares
            (63, 56, 0, 7),  # rook starting squares
            ((61, 62), (59, 58, 57), (5, 6), (3, 2, 1)),  # squares that need to be free for castle to be possible
            ((60, 61, 62), (60, 59, 58), (4, 5, 6), (4, 3, 2)) # squares that need to be safe for castle
        )
        for y in range(8):
            for x in range(8):
                square_index = y * 8 + x

                up = y
                down = 7 - y
                left = x
                right = 7 - x

                up_left = min(up, left)
                up_right = min(up, right)
                down_left = min(down, left)
                down_right = min(down, right)

                self.edges[square_index] = [
                    up,
                    down,
                    left,
                    right,

                    up_left,
                    down_left,
                    up_right,
                    down_right,
                ]
                self.knight_moves[square_index] = []
                knight_offsets = {
                    0: (2, -1),
                    1: (2, 1),
                    2: (1, -2),
                    3: (1, 2),

                    4: (-1, -2),
                    5: (-1, 2),
                    6: (-2, -1),
                    7: (-2, 1)
                }
                for offset_index in knight_offsets:
                    offset = knight_offsets[offset_index]
                    if 0 <= y - offset[0] < 8 and 0 <= x + offset[1] < 8:
                        self.knight_moves[square_index].append(piece.KNIGHT_DIRECTIONS[offset_index])
