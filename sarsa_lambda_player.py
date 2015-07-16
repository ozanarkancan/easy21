import numpy as np
import logging
from collections import OrderedDict
from player import *

logger = logging.getLogger(__name__)

class SarsaLambdaPlayer(Player):
    def __init__(self, _lambda=0.5, gamma = 1):
        Player.__init__(self)
        self.rng = np.random.RandomState()
        self.Q = {}
        self.E = {}
        self.N = {}
        self._lambda = _lambda
        self.gamma = gamma
        for p_sum in range(1,22):
            for dealer in range(1,11):
                self.Q[(p_sum, dealer, "hit")] = self.rng.uniform(-1, 1)
                self.Q[(p_sum, dealer, "stick")] = self.rng.uniform(-1, 1)
                self.E[(p_sum, dealer, "hit")] = 0
                self.E[(p_sum, dealer, "stick")] = 0
                self.N[(p_sum, dealer)] = 0
        
    def play(self):
        self.rng = np.random.RandomState()
        game = Game(self.rng)
        state = (False, game.player.hand_sum, game.dealer.hand_sum, 0)
        logger.debug("Initial: " + str(state))
        
        path = OrderedDict()

        a = self.action(state)

        while not state[0]:
            logger.debug('Action: ' + a)

            state_prime = game.step(a)
            r = state_prime[-1]
            a_prime = self.action(state_prime)
            
            self.update(state, a, r, state_prime, a_prime)

            state = state_prime
            a = a_prime

            logger.debug('State: ' + str(state_prime))
        
        return state[-1]

    def update(self, s, a, r, s_prime, a_prime):
        self.N[(s[1], s[2])] += 1

        if not (s_prime[1], s_prime[2], a_prime) in self.Q.keys():
            qnext = 0
        else:
            qnext = self.Q[(s_prime[1], s_prime[2], a_prime)]
        
        delta = r + self.gamma * qnext - self.Q[(s[1], s[2], a)]
        self.E[(s[1], s[2], a)] += 1
        for p_sum in range(1,22):
            for dealer in range(1,11):
                try:
                    alpha = 1.0 / self.N[(p_sum, dealer)]
                except:
                    alpha = 0
                for a in ["hit", "stick"]:
                    s_a = (p_sum, dealer, a)
                    self.Q[s_a] += alpha * delta * self.E[s_a]
                    self.E[s_a] *= self.gamma * self._lambda
 
    def action(self, state):
        rnd = self.rng.rand()
        N = 0 if not (state[1], state[2]) in self.N.keys() else self.N[(state[1], state[2])]
        eps = 100.0 / (100.0 + N)
        logger.debug("Epsilon: " + str(eps))
        
        if rnd < eps:
            rnd = self.rng.randint(2)
            a = "hit" if rnd == 0 else "stick"
        else:
            if self.Q[(state[1], state[2], "hit")] > self.Q[(state[1], state[2], "stick")]:
                a = "hit"
            else:
                a = "stick"
        return a

