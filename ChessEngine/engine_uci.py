import time
import os

from ChessEngine.engine import Engine


class EngineUCI:
    def __init__(self):
        self.engine = Engine()

    def receive_command(self, message):
        if message == "uci":
            print("uciok")
        elif message == "isready":
            print("readyok")
        elif message == "ucinewgame":
            self.engine.new_game()
        elif "position" in message:
            self.process_position_command(message)
        elif "go" in message:
            self.process_go_command(message)
        elif "perft" in message:
            self.process_perft_command(message)
        elif "d" in message:
            self.process_draw_command(message)
        elif "stop" in message:
            print("stop")  # todo
        elif "quit" in message:
            quit()
        elif message in ["cls", "clear"]:
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            print("Unknown command.")

    def process_position_command(self, message):
        if "startpos" in message:
            fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        elif "fen" in message:
            fen = message.split("fen", 1)[1].strip().split("moves", 1)[0].strip()
        else:
            print("Invalid position")
            return
        self.engine.board.fen_to_board(fen)
        if "moves" in message:
            moves = message.split("moves", 1)[1].strip().split(" ")
            for move in moves:
                start = (ord(move[:2][0]) - 97) + (8 * (8 - int(move[:2][1])))
                target = (ord(move[2:][0]) - 97) + (8 * (8 - int(move[2:][1])))
                self.engine.make_move(start, target)

    def process_go_command(self, message):
        elements = message.split(" ")
        time = 2.0 
        if len(elements) > 1:
            time = float(elements[1])
        move = self.engine.get_best_move(search_time=time)["move"]

        start = "abcdefgh"[move.get_starting_square() % 8] + str(8 - (move.get_starting_square() // 8))
        target = "abcdefgh"[move.get_target_square() % 8] + str(8 - (move.get_target_square() // 8))
        print(f"bestmove {start + target}")

    def process_perft_command(self, message):
        depth = 3 if len(message.strip().split(" ")) < 2 else int(message.split(" ")[1])
        start_time = time.time()
        result = self.engine.move_generation_test(depth, True)
        end_time = time.time()
        total_positions = result["count"]
        moves = result["moves"]
        for move in moves:
            print(f"{move}: {moves[move]}")
        print(f"\nNodes searched: {total_positions}\n")
        elapsed_time = end_time - start_time
        positions_per_second = total_positions / elapsed_time
        kps = positions_per_second / 1_000
        print(f"Depth: {depth}")
        print(f"Elapsed time: {elapsed_time:.2f} seconds")
        print(f"Speed: {kps:.2f} thousand positions per second (KPS)")

    def process_draw_command(self, message):
        wide = "wide" in message
        print(self.engine.board.fen_from_board())
        bar = "+-----+-----+-----+-----+-----+-----+-----+-----+" if wide else "+---+---+---+---+---+---+---+---+"
        print(bar)
        pieces_map = {0: " ", 9: "K", 10: "P", 11: "N", 12: "B", 13: "R", 14: "Q", 17: "k", 18: "p", 19: "n", 20: "b",
                      21: "r", 22: "q"}
        for y in range(8):
            line = "|"
            for x in range(8):
                index = 8 * y + x
                piece = pieces_map[self.engine.board.square[index]]
                line += f"  {piece}  |" if wide else f" {piece} |"
            print(line)
            print(bar)
