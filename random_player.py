import numpy as np
from player import *

class RandomPlayer(Player):
    def action(self):
        r = self.rng.randint(2)
        a = "hit" if r == 0 else "stick"
        return a
