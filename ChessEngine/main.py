import json

from ChessEngine.board import Board
from ChessEngine.moveGenerator import MoveGenerator
from ChessEngine.precomputedMoveData import PrecomputedMoveData

def main():
    brd = Board()
    pmd = PrecomputedMoveData()
    mg = MoveGenerator(brd, pmd)
    brd.FENtoBoard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    mg.GenerateLegalMoves()
    c = 0
    for move in mg.moves:
        c += 1
        renderBoard(brd, move.startingSquare, move.targetSquare)

def renderBoard(board, startingSquare, targetSquare):
    print("Start:", startingSquare, "Target:", targetSquare)
    line = "| "
    print("---------------------------")
    for y in range(8):
        for x in range(8):
            index = 8 * y + x
            square = ""
            if index == startingSquare:
                square = "S "
            elif index == targetSquare:
                square = "E "
            else:
                square = str(board.square[8 * y + x]) + " "
            line += square if len(square) > 2 else square + " "
        print(line + "|")
        line = "| "
    print("---------------------------")


if __name__ == "__main__":
    main()