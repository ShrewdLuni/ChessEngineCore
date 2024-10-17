from ChessEngine.engine import Engine


class EngineUCI:
    def __init__(self):
        self.engine = Engine()

    def ReceiveCommand(self, message):
        match message:
            case "uci":
                print("uciok")
            case "isready":
                print("readyok")
            case "ucinewgame":
                pass
            case "position":
                pass
            case "go":
                pass
            case "stop":
                pass
            case "quit":
                pass
