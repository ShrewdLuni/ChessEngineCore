import time

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
        elif "stop" in message:
            print("stop")  # todo
        elif "quit" in message:
            print("quit")  # todo
        else:
            print("Unrecognized command")

    def process_position_command(self, message):
        if "startpos" in message:
            fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        elif "fen" in message:
            fen = message.split("fen", 1)[1].strip().split("moves", 1)[0].strip()
        self.engine.board.fen_to_board(fen)
        if "moves" in message:
            moves = message.split("moves", 1)[1].strip().split(" ")
            for move in moves:
                start = (ord(move[:2][0]) - 97) + (8 * (8 - int(move[:2][1])))
                target = (ord(move[2:][0]) - 97) + (8 * (8 - int(move[2:][1])))
                self.engine.make_move(start, target)

    def process_go_command(self, message):
        move = self.engine.get_best_move()
        start = "abcdefgh"[move.get_starting_square() % 8] + str(8 - (move.get_starting_square() // 8))
        target = "abcdefgh"[move.get_target_square() % 8] + str(8 - (move.get_target_square() // 8))
        print(f"bestmove {start + target}")

    def process_perft_command(self, message):
        depth = 3
        start_time = time.time()
        result = self.engine.move_generation_test(depth, True)
        end_time = time.time()
        total_positions = result["count"]
        print(result["count"])
        elapsed_time = end_time - start_time
        positions_per_second = total_positions / elapsed_time
        kps = positions_per_second / 1_000
        print(f"Depth: {depth}")
        print(f"Total positions: {total_positions}")
        print(f"Elapsed time: {elapsed_time:.2f} seconds")
        print(f"Speed: {kps:.2f} thousand positions per second (KPS)")

