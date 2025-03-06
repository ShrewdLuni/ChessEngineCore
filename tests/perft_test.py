from ChessEngine import Engine

def test_perfit(depth: int = 5):
    engine = Engine()
    result = engine.move_generation_test(depth, True)
    assert result["count"] == 4865609
