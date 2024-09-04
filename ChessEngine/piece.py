Nothing = 0
King = 1
Pawn = 2
Knight = 3
Bishop = 4
Rook = 5
Queen = 6

White = 8
Black = 16

KnightDirections = [-17, -15, -10, -6, 6, 10, 15, 17]
KingDirections = [-8, 8, -1, 1, -9, 7, -7, 9]
#up down left right upLeft downLeft upRight downRight

def GetPieceType(piece):
    return piece & 7

def IsColor(piece, color):
    return piece & color == color