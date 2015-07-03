import numpy as np
from collections import OrderedDict

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
            print "Card: ",
            print card
            self.player.add_card(card)
            if self.player.hand_sum < 1 or self.player.hand_sum > 21:
                reward = -1
                terminal = True
        else:#stick
            print "Dealer Turns: "
            while not terminal:
                card = self.draw_a_card()
                print "Card: ",
                print card
                self.dealer.add_card(card)
                if self.dealer.hand_sum < 1 or self.dealer.hand_sum > 21:
                    reward = 1
                    terminal = True
                elif self.dealer.hand_sum >= 17:
                    terminal = True
                    print "Action: stick"
                else:
                    print "Action: hit"
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

class Player(object):
    def __init__(self):
        self.played_game = 0
        self.win = 0

    def play(self):
        self.rng = np.random.RandomState()
        game = Game(self.rng)
        state = (False, game.player.hand_sum, game.dealer.hand_sum, 0)
        print "Initial: ",
        print state

        while not state[0]:
            a = self.action()
            print "Action: ",
            print a
            state = game.step(a)
            print "State: ",
            print state

        return state[-1]


    def action(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def simulate(self, episode = 20):
        for i in xrange(1, episode + 1):
            result = self.play()
            self.played_game += 1
            print "Episode: {0} Result: {1}\n".format(i, result)
            if result == 1:
                self.win += 1

        print "Win Ratio: %{0}".format(100 * float(self.win) / self.played_game)

class RandomPlayer(Player):
    def action(self):
        r = self.rng.randint(2)
        a = "hit" if r == 0 else "stick"
        return a

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
        print "Initial: ",
        print state
        
        path = OrderedDict()

        while not state[0]:
            a = self.action(state)
            print "Action: ",
            print a
            s = state[1:3]
            state = game.step(a)
            r = state[-1]
            if not s in path.keys():
                path[(s[0], s[1], a)] = r
            print "State: ",
            print state

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
        print "eps: ",
        print eps
        if rnd < eps:
            rnd = self.rng.randint(2)
            a = "hit" if rnd == 0 else "stick"
        else:
            if self.Q[(state[1], state[2], "hit")] > self.Q[(state[1], state[2], "stick")]:
                a = "hit"
            else:
                a = "stick"
        return a

if __name__ == "__main__":
    #player = RandomPlayer()
    player = MonteCarloPlayer()

    player.simulate(1000000)
    
