import time

from termcolor import colored
from ChessEngine.engine import Engine
from ChessEngine.evaluation import Evaluation

def main():
    engine = Engine()
    engine.board.fen_to_board("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1")
    # engine.board.make_move(28, 11, 0)
    print(engine.board.fen_from_board())

    depth = 5
    start_time = time.time()
    total_positions = engine.move_generation_test(depth, True)
    show_kps(depth, total_positions, start_time, time.time())
    # data = """
    # """
    # lines = data.strip().splitlines()
    # chess_dict = {line.split(":")[0].strip(): int(line.split(":")[1].strip()) for line in lines}
    # stockfish_result = {k: chess_dict[k] for k in sorted(chess_dict)}
    # engine_result = {k: engine.move_results[k] for k in sorted(engine.move_results)}
    # print(stockfish_result)
    # print(engine_result)
    # check_moves(stockfish_result, engine_result)

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

def show_kps(depth, total_positions, start_time, end_time):
    elapsed_time = end_time - start_time
    positions_per_second = total_positions / elapsed_time
    kps = positions_per_second / 1_000
    print(f"Depth: {depth}")
    print(f"Total positions: {total_positions}")
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    print(f"Speed: {kps:.2f} thousand positions per second (KPS)")

def check_moves(dict1, dict2):
    print("---------------------------")
    bad_keys = []
    for key in dict1.keys():
        if not key in dict2:
            bad_keys.append(key)
            continue
        count1 = dict1[key]
        count2 = dict2[key]

        print(f"{key}: ", end="")
        print(colored(f"{count1}", "green"), end=" ")
        if count1 == count2:
            print(colored(f"{count2}", "green"))
        else:
            print(colored(f"{count2}", "red"))
    print(bad_keys)

if __name__ == "__main__":
    main()