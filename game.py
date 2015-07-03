import numpy as np
import logging

logger = logging.getLogger(__name__)

class Hand(object):
    def __init__(self, val):
        self.hand = [("black", val)]
        self.hand_sum = val

    def add_card(self, card):
        self.hand.append(card)
        if card[0] == "black":
            self.hand_sum += card[1]
        else:
            self.hand_sum -= card[1] 

class Game(object):
    def __init__(self, rng = None):
        if rng == None:
            self.rng = np.random.RandomState(12345)
        else:
            self.rng = rng
        self.player = Hand(self.rng.randint(1, 11))
        self.dealer = Hand(self.rng.randint(1, 11))

    def draw_a_card(self):
        val = self.rng.randint(1, 11)
        rnd = self.rng.randint(3)

        col = "red" if rnd < 1 else "black"

        return (col, val)
    
    #takes action
    #state: player's sum and dealer's first card
    #returns state & reward
    def step(self, action):
        terminal = False
        reward = 0
        if action == "hit":
            card = self.draw_a_card()
            logger.info("Card: " + str(card))
            
            self.player.add_card(card)
            if self.player.hand_sum < 1 or self.player.hand_sum > 21:
                reward = -1
                terminal = True
        else:#stick
            logger.info("Dealer Turn: ")

            while not terminal:
                card = self.draw_a_card()
                logger.info("Card: " + str(card))
                
                self.dealer.add_card(card)
                if self.dealer.hand_sum < 1 or self.dealer.hand_sum > 21:
                    reward = 1
                    terminal = True
                elif self.dealer.hand_sum >= 17:
                    terminal = True
                    logger.info("Action: stick")
                else:
                    logger.info("Action: hit")
            if reward == 0:
                reward = self.result()
        return (terminal, self.player.hand_sum, self.dealer.hand_sum, reward)

    def result(self):
        r = 0
        if self.player.hand_sum > self.dealer.hand_sum:
            r = 1
        elif self.player.hand_sum < self.dealer.hand_sum:
            r = -1
        return r
