import pytest

from ChessEngine import Engine


@pytest.mark.parametrize("depth,expected", [
    (1, 20),
    (2, 400),
    (3, 8902),
    (4, 197281),
    (5, 4865609),
    # (6, 119060324),
    # (7, 3195901860),
    # (8, 84998978956),
    # (9, 2439530234167),
])
def test_perfit(depth: int, expected: int):
    engine = Engine()
    result = engine.move_generation_test(depth, True)
    assert result["count"] == expected 
