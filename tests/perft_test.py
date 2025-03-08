import pytest

from ChessEngine import Engine

STARTPOS = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
KIWIPETE = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"


@pytest.fixture
def engine():
    return Engine()

@pytest.mark.parametrize("position,depth,expected", [
    (STARTPOS, 1, 20),
    (STARTPOS, 2, 400),
    (STARTPOS, 3, 8902),
    (STARTPOS, 4, 197281),
    (STARTPOS, 5, 4865609),

    (KIWIPETE, 1, 48),
    (KIWIPETE, 2, 2039),
    (KIWIPETE, 3, 97862),
    (KIWIPETE, 4, 4085603),
])
def test_perfit(engine: Engine, position: str, depth: int, expected: int):
    engine = Engine()
    engine.set_position(position)
    result = engine.move_generation_test(depth, True)
    assert result["count"] == expected 
