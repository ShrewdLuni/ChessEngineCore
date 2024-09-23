from ChessEngine.engine import Engine

def main():
    engine = Engine()
    print(render_board(engine.board, -1, -1))


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