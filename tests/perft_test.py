import pytest

from ChessEngine import Engine

POSITIONS = [
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1",
    "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1",
    "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1",
    "r2q1rk1/pP1p2pp/Q4n2/bbp1p3/Np6/1B3NBn/pPPP1PPP/R3K2R b KQ - 0 1 ",
    "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8",
    "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10"
]

@pytest.fixture
def engine():
    return Engine()

@pytest.mark.parametrize("position,depth,expected", [
    (POSITIONS[0], 1, 20),
    (POSITIONS[0], 2, 400),
    (POSITIONS[0], 3, 8902),
    (POSITIONS[0], 4, 197281),
    (POSITIONS[0], 5, 4865609),

    (POSITIONS[1], 1, 48),
    (POSITIONS[1], 2, 2039),
    (POSITIONS[1], 3, 97862),
    (POSITIONS[1], 4, 4085603),
    (POSITIONS[1], 5, 193690690),

    (POSITIONS[2], 1, 14),
    (POSITIONS[2], 2, 191),
    (POSITIONS[2], 3, 2812),
    (POSITIONS[2], 4, 43238),
    (POSITIONS[2], 5, 674624),

    (POSITIONS[3], 1, 6),
    (POSITIONS[3], 2, 264),
    (POSITIONS[3], 3, 9467),
    (POSITIONS[3], 4, 422333),
    (POSITIONS[3], 5, 15833292),

    (POSITIONS[4], 1, 6),
    (POSITIONS[4], 2, 264),
    (POSITIONS[4], 3, 9467),
    (POSITIONS[4], 4, 422333),
    (POSITIONS[4], 5, 15833292),

    (POSITIONS[5], 1, 44),
    (POSITIONS[5], 2, 1486),
    (POSITIONS[5], 3, 62379),
    (POSITIONS[5], 4, 2103487),
    (POSITIONS[5], 5, 89941194),

    (POSITIONS[6], 1, 46),
    (POSITIONS[6], 2, 2079),
    (POSITIONS[6], 3, 89890),
    (POSITIONS[6], 4, 3894594),
    (POSITIONS[6], 5, 164075551),
])
def test_perfit(engine: Engine, position: str, depth: int, expected: int):
    engine = Engine()
    engine.set_position(position)
    result = engine.move_generation_test(depth, True)
    assert result["count"] == expected 
