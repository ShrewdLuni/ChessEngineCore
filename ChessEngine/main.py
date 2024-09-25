import time

from ChessEngine.engine import Engine
from ChessEngine.evaluation import Evaluation

def main():
    engine = Engine()
    depth = 5
    start_time = time.time()
    total_positions = engine.move_generation_test(depth)
    end_time = time.time()
    elapsed_time = end_time - start_time
    positions_per_second = total_positions / elapsed_time
    kps = positions_per_second / 1_000
    print(f"Depth: {depth}")
    print(f"Total positions: {total_positions}")
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    print(f"Speed: {kps:.2f} thousand positions per second (KPS)")

def render_board(board, starting_square, target_square):
    # print(f"Start: {starting_square}, Target: {target_square}")
    # print("---------------------------")
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