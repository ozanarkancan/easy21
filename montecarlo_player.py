import numpy as np
import logging
from collections import OrderedDict
from player import *

logger = logging.getLogger(__name__)

class MonteCarloPlayer(Player):
    def __init__(self):
        Player.__init__(self)
        self.rng = np.random.RandomState()
        self.Q = {}
        self.N = {}
        for p_sum in range(1,22):
            for dealer in range(1,11):
                self.Q[(p_sum, dealer, "hit")] = self.rng.randint(-3, 3)
                self.Q[(p_sum, dealer, "stick")] = self.rng.randint(-3, 3)
                self.N[(p_sum, dealer)] = 0
    
    def play(self):
        self.rng = np.random.RandomState()
        game = Game(self.rng)
        state = (False, game.player.hand_sum, game.dealer.hand_sum, 0)
        logger.info("Initial: " + str(state))
        
        path = OrderedDict()

        while not state[0]:
            a = self.action(state)
            logger.info('Action: ' + a)

            s = state[1:3]
            state = game.step(a)
            r = state[-1]
            if not s in path.keys():
                path[(s[0], s[1], a)] = r
            
            logger.info('State: ' + str(state))

        self.update(path)

        return state[-1]

    def update(self, path):

        s_a_list = path.keys()
        for i in range(len(s_a_list)):
            s_a = s_a_list[i]
            
            a = "hit" if s_a[-1] == "stick" else "stick"

            if not (s_a[0], s_a[1], a)  in s_a_list[:i]: #first visit
                self.N[(s_a[0], s_a[1])] += 1

            alpha = 1.0 / self.N[(s_a[0], s_a[1])]
            self.Q[s_a] = self.Q[s_a] + alpha * (path[s_a_list[-1]] - self.Q[s_a])

    def action(self, state):
        rnd = self.rng.rand()
        eps = 100.0 / (100.0 + self.N[(state[1], state[2])])
        logger.info("Epsilon: " + str(eps))
        
        if rnd < eps:
            rnd = self.rng.randint(2)
            a = "hit" if rnd == 0 else "stick"
        else:
            if self.Q[(state[1], state[2], "hit")] > self.Q[(state[1], state[2], "stick")]:
                a = "hit"
            else:
                a = "stick"
        return a

