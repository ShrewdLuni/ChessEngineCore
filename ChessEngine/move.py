class Move:
    def __init__(self, starting_square, target_square, flag=0):
        self.move = (flag << 12) | (target_square << 6) | starting_square

    def get_starting_square(self):
        return self.move & 0x3F

    def get_target_square(self):
        return (self.move >> 6) & 0x3F

    def get_move_flag(self):
        return (self.move >> 12) & 0xF
