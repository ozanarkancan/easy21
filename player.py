import numpy as np
import logging
from game import *

logger = logging.getLogger(__name__)

class Player(object):
    def __init__(self):
        self.played_game = 0
        self.win = 0

    def play(self):
        self.rng = np.random.RandomState()
        game = Game(self.rng)
        state = (False, game.player.hand_sum, game.dealer.hand_sum, 0)
        logger.info('Initial: ' + str(state))

        while not state[0]:
            a = self.action()
            logger.info('Action: ' + a)
            state = game.step(a)
            logger.info('State: ' + str(state))

        return state[-1]

    def action(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def simulate(self, episode = 20):
        for i in xrange(1, episode + 1):
            result = self.play()
            self.played_game += 1
            
            logger.info("Episode: {0} Result: {1}\n".format(i, result))
            
            if result == 1:
                self.win += 1

        logger.info("Win Ratio: %{0}".format(100 * float(self.win) / self.played_game))
