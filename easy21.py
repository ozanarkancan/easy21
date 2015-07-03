import numpy as np
from montecarlo_player import *
from random_player import *
import logging
import argparse

def get_arg_parser():
    parser = argparse.ArgumentParser(prog="easy21")

    parser.add_argument("-agent", default="mc",
        help="Agent Type: random, mc (monte carlo), sarsa")
    parser.add_argument("-episode", default=100, type=int,
        help="Number of episodes")

    return parser

def get_agent(agent_type):
    if agent_type == "mc":
        return MonteCarloPlayer()
    elif agent_type == "sarsa":
        raise NotImplementedError("Sarsa is not implemented")
    else:
        return RandomPlayer()

if __name__ == "__main__":
    parser = get_arg_parser()
    args = vars(parser.parse_args())
    
    f_name = args["agent"] + "_" + str(args["episode"]) + ".log"
    logging.basicConfig(filename=f_name, level=logging.INFO)
    
    player = get_agent(args["agent"])
    player.simulate(args["episode"])
    
