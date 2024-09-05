class PrecomputedMoveData:
    def __init__(self):
        self.edges = {}
        self.precompute_move_data()

    def precompute_move_data(self):
        for y in range(8):
            for x in range(8):
                square_index = y * 8 + x

                up = y
                down = 7 - y
                left = x
                right = 7 - x

                up_left = min(up, left)
                up_right = min(up, right)
                down_left = min(down, left)
                down_right = min(down, right)

                self.edges[square_index] = [
                    up,
                    down,
                    left,
                    right,

                    up_left,
                    down_left,
                    up_right,
                    down_right,
                ]
