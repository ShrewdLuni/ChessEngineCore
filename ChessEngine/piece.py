NOTHING = 0
KING = 1
PAWN = 2
KNIGHT = 3
BISHOP = 4
ROOK = 5
QUEEN = 6

WHITE = 8
BLACK = 16

KNIGHT_DIRECTIONS = [-17, -15, -10, -6, 6, 10, 15, 17]

# -17, 2, -1
# -15, 2,  1
# -10, 1, -2
# -6,  1,  2

# 6,  -1  -2
# 10, -1   2
# 15, -2  -1
# 17  -2   1
KING_DIRECTIONS = [-8, 8, -1, 1, -9, 7, -7, 9]
# up down left right upLeft downLeft upRight downRight


def get_piece_type(piece):
    return piece & 7


def is_color(piece, color):
    return piece & color == color
