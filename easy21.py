import numpy as np
from montecarlo_player import *
from random_player import *
import logging
import argparse
import pylab as p
import mpl_toolkits.mplot3d.axes3d as p3

def get_arg_parser():
    parser = argparse.ArgumentParser(prog="easy21")

    parser.add_argument("-agent", default="mc",
        help="Agent Type: random, mc (monte carlo), sarsa")
    parser.add_argument("-episode", default=100, type=int,
        help="Number of episodes")
    parser.add_argument("-plot_v", default=False, type=bool,
        help="Plot value function")

    return parser

def get_agent(agent_type):
    if agent_type == "mc":
        return MonteCarloPlayer()
    elif agent_type == "sarsa":
        raise NotImplementedError("Sarsa is not implemented")
    else:
        return RandomPlayer()

def plot_v(agent):
    v_val = np.zeros((10, 21))

    for p_sum in xrange(1, 22):
        for d in xrange(1, 11):
            v_val[d - 1][p_sum - 1] = \
                max([agent.Q[(p_sum, d, "hit")], agent.Q[(p_sum, d, "stick")]])

    x = np.arange(1, 22)
    y = np.arange(1, 11)

    X, Y = p.meshgrid(x, y)

    fig = p.figure()
    cont = p.contourf(X, Y, v_val)
    fig.colorbar(cont)
    p.xlabel('Player sum')
    p.ylabel('Dealer first card')
    p.title('Value Function')
    p.show()

if __name__ == "__main__":
    parser = get_arg_parser()
    args = vars(parser.parse_args())
    
    f_name = args["agent"] + "_" + str(args["episode"]) + ".log"
    logging.basicConfig(filename=f_name, filemode='w', level=logging.INFO)
    
    player = get_agent(args["agent"])
    player.simulate(args["episode"])

    if args["plot_v"] and args["agent"] == "mc":
        plot_v(player)
                
    
