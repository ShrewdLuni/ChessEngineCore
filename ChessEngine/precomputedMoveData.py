class PrecomputedMoveData:
    def __init__(self):
        self.edges = {}
        self.PrecomputeMoveData()

    def PrecomputeMoveData(self):
        for y in range(8):
            for x in range(8):
                squareIndex = y * 8 + x

                up = y
                down = 7 - y
                left = x
                right = 7 - x

                upLeft = min(up, left)
                upRight = min(up, right)
                downLeft = min(down, left)
                downRight = min(down, right)

                self.edges[squareIndex] = [
                    up,
                    down,
                    left,
                    right,

                    upLeft,
                    downLeft,
                    upRight,
                    downRight,
                ]