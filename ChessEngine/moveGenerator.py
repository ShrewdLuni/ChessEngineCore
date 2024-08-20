import ChessEngine.piece as Piece
from ChessEngine.move import Move

class MoveGenerator:
    def __init__(self, board, precomputedData):
        self.moves = []
        self.board = board

        self.friendlyColor = Piece.White
        self.opponentColor = Piece.Black

        self.precomputedData = precomputedData


    def GenerateLegalMoves(self):
        self.GenerateMoves()

    def GenerateMoves(self):
        for index in range(64):
            piece = self.board.square[index]
            if piece == 0:
                continue
            if Piece.IsColor(piece, Piece.White):
                pieceType = Piece.GetPieceType(piece)
                if pieceType == Piece.Pawn:
                    self.GeneratePawnMoves(index)
                elif pieceType == Piece.King:
                    self.GenerateKingMoves(index)
                elif pieceType == Piece.Knight:
                    self. GenerateKnightMoves(index)
                else:
                    self.GenerateSlidingMoves(index, pieceType)

    def GeneratePawnMoves(self, startingSqure):
        pass

    def GenerateKingMoves(self, startingSquare):
        pass

    def GenerateKnightMoves(self, startingSquare):
        pass

    def GenerateSlidingMoves(self, startingSquare, pieceType):
        startingDirectionIndex = 4 if pieceType == Piece.Bishop else 0
        endDirectionIndex = 4 if pieceType == Piece.Rook else 8
        for directionIndex in range(startingDirectionIndex, endDirectionIndex):
            for n in range(self.precomputedData.edges[startingSquare][directionIndex]):
                targetSquare = startingSquare + Piece.KingDirections[directionIndex] * (n + 1)

                pieceOnTargetSquare = self.board.square[targetSquare]

                if Piece.IsColor(pieceOnTargetSquare, self.opponentColor):
                    break

                self.moves.append(Move(startingSquare, targetSquare))

                if Piece.IsColor(pieceOnTargetSquare, self.opponentColor):
                    break


    def IsExistingSquare(self, squareIndex):
        return True if -1 < squareIndex < 64 else False