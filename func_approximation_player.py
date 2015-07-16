import numpy as np
import logging
from collections import OrderedDict
from player import *

logger = logging.getLogger(__name__)

class FuncApproximationPlayer(Player):
    def __init__(self, _lambda=0.5, gamma = 1):
        Player.__init__(self)
        self.rng = np.random.RandomState()
        self.Q = {}
        self.E = {}
        self.N = {}
        self.theta = self.rng.normal(size=(36, 1))
        self._lambda = _lambda
        self.gamma = gamma
        self.alpha = 0.01
        self.eps = 0.05

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
        
        rnd = self.rng.randint(2)
        a = "hit" if rnd == 0 else "stick"
        e = np.zeros((36, 1))

        while not state[0]:
            logger.debug('Action: ' + a)
            fa = self.feature_vector(state[1], state[2], a)
            e[np.where(fa == 1), 0] += 1
            state_prime = game.step(a)
            r = state_prime[-1]
            delta = r - np.sum(self.theta[np.where(fa == 1), 0])
            
            qa = []
            for act in ["hit", "stick"]:
                fact = self.feature_vector(state[1], state[2], act)
                qa.append(np.sum(self.theta[np.where(fact == 1), 0]))
            
            delta += self.gamma * max(qa)
            self.theta += self.alpha * delta * e

            rnd = self.rng.rand()
            if rnd < self.eps:
                e = np.zeros((36, 1))
                rnd = self.rng.randint(2)
                a = "hit" if rnd == 0 else "stick"
            else:
                qa = []
                actions = ["hit", "stick"]
                for act in actions:
                    fact = self.feature_vector(state[1], state[2], act)
                    qa.append(np.sum(self.theta[np.where(fact == 1), 0]))
                indx = np.argmax(qa)
                a = actions[indx]
                e *= self.gamma * self._lambda
            state = state_prime
            
        return state[-1]

    def feature_vector(self, p_sum, dealer, a):
        vec = np.zeros((36, 1))
        ds = [(1, 5), (5, 8), (8, 11)]
        ps = [(1, 7), (4, 10), (7, 13), (10, 16), (13, 19), (16, 22)]
        a_s = ["hit", "stick"]

        indx = 0
        for d_intrvl in ds:
            for p_intrvl in ps:
                for act in a_s:
                    if dealer in range(d_intrvl[0], d_intrvl[1]) and \
                        p_sum in range(p_intrvl[0], p_intrvl[1]) and \
                        act == a:
                        vec[indx, 0] = 1
                    indx += 1

        return vec
