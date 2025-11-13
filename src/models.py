from enum import Enum

class Cell(Enum):
    EMPTY = 0
    CROSS = 1
    TICK = 2
    MAYBE = 3
    CROSS_INHERITED = 4
    DEAD = 5


    def next_member(self):
        if self.value < 3:
            return Cell((self.value + 1) % 3)
        elif self == Cell.MAYBE:
            return Cell.EMPTY
        else:
            return self
        