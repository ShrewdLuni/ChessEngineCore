import json

from ChessEngine.board import Board
from ChessEngine.move_generator import MoveGenerator
from ChessEngine.precomputed_move_data import PrecomputedMoveData

def main():
    brd = Board()
    pmd = PrecomputedMoveData()
    mg = MoveGenerator(brd, pmd)
    brd.fen_to_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    mg.generate_legal_moves()

    move_count = 0
    for move in mg.moves:
        move_count += 1
        render_board(brd, move.starting_square, move.target_square)

    print(f"Total moves generated: {move_count}")

def render_board(board, starting_square, target_square):
    print(f"Start: {starting_square}, Target: {target_square}")
    print("---------------------------")
    for y in range(8):
        line = "| "
        for x in range(8):
            index = 8 * y + x
            square = ""
            if index == starting_square:
                square = "S "
            elif index == target_square:
                square = "E "
            else:
                square = str(board.square[index]) + " "
            line += square if len(square) > 2 else square + " "
        print(line + "|")
    print("---------------------------")


if __name__ == "__main__":
    main()