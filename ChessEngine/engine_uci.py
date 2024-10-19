from ChessEngine.engine import Engine


class EngineUCI:
    def __init__(self):
        self.engine = Engine()

    def receive_command(self, message):
        match message:
            case "uci":
                print("uciok")
            case "isready":
                print("readyok")
            case "ucinewgame":
                self.engine.new_game()
            case "position":
                self.process_position_command(message)
            case "go":
                self.process_go_command(message)
            case "stop":
                print("stop")  # todo
            case "quit":
                print("quit")  # todo

    def process_position_command(self, message):
        message = message.lower()
        if "startpos" in message:
            self.engine.set_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        elif "fen" in message:
            fen = message.split("fen")[1].strip()
            self.engine.set_position(fen)

    def process_go_command(self, message):
        move = self.engine.get_best_move()
        start = "abcdefgh"[move.get_starting_square() % 8] + str(8 - (move.get_starting_square() // 8))
        target = "abcdefgh"[move.get_target_square() % 8] + str(8 - (move.get_target_square() // 8))
        print(f"bestmove {start + target}")
