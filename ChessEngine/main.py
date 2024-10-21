from ChessEngine.engine_uci import EngineUCI

def main():
    engine = EngineUCI()

    command = ""
    while command != "quit":
        command = input()
        engine.receive_command(command)


if __name__ == "__main__":
    main()