from __future__ import division
from __future__ import print_function

import random
import argparse

import numpy as np

from mcts.mcts import *
# import mymcts.painting_world_state as state
from mcts.graph import StateNode
from mcts.tree_policies import *
from mcts.default_policies import *
from mcts.backups import *
import time

try:
    import cPickle as pickle
except ImportError:
    import pickle
import datetime

from mymcts.painting_world_state import *
import interface
import random



__author__ = 'johannes'


def run_experiment(intrinsic_motivation, gamma, c, mc_n, runs, steps, problem):
    st1 = time.time()
    # trajectories = []
    start = np.array([50, 50])
    true_belief = True

    mcts_search = MCTS(tree_policy=UCB1(c=1.41),
                default_policy=immediate_reward,
                backup=monte_carlo)

    rewards = []
    for r in range(runs):
        sta = time.time()
        print ("RUN number", r)
        goal = draw_goal(start, 6)
        # manual = draw_goal(start, 3)
        # print("Goal: {}".format(goal))
        # # print("Manual: {}".format(manual))

        world = PaintingWorld((100, 100), False, (100, 100), problem)
        belief = None
        root_state = PaintingWorldState((0,0), (1,1,1),world)
        if true_belief:
            belief = {}
            for action in root_state.actions:
              belief[action] = [1]*len(root_state.actions)
            root_state.belief = belief
        # print(root_state.pos)
        next_state = StateNode(None, root_state)
        # trajectory =[]
        rew = 0
        for step in range(steps):
            # try:
            # if step % 3 == 0:
            #     print("step", step)
            st = time.time()
            ba = mcts_search(next_state, n=mc_n)
            # if step % 3 == 0:
            #     print("step", step)
                # print("=" * 80)
                # print("State: {}".format(next_state.state))
                # # print("Belief: {}".format(next_state.state.belief))
                # print("Reward: {}".format(next_state.reward))
                # print("N: {}".format(next_state.n))
                # print("Q: {}".format(next_state.q))
                # print("Action: {}".format(ba.action))
            # trajectory.append(next_state.state.pos)
            rew = next_state.reward
            if (next_state.state.pos == np.array(goal)).all():
                break
            next_s = next_state.children[ba].sample_state(real_world=True)
            next_state = next_s
            next_state.parent = None

            en = time.time()
            print ("step", step, "time elapsed", en - st)

            if step >= 5 and rew > 0.5:
                break

            # except KeyboardInterrupt:
            #     break
        # trajectories.append(trajectory)
        # print (next_state.reward)
        rewards.append(rew)

        # with open(gen_name("trajectories", "pkl"), "w") as f:
        #     pickle.dump(trajectories, f)
        # print("=" * 80)
        end = time.time()
        print ("run", r, "time elapsed", end-sta)
        if rewards[-1] > 0:
            break
    w = max(rewards)
    print ("REWARD", w)
    end1 = time.time()
    print ("problem time elapsed", end1 - st1)
    return w

def draw_goal(start, dist):
    delta_x = random.randint(0, dist)
    delta_y = dist - delta_x
    return start - np.array([delta_x, delta_y])


def gen_name(name, suffix):
    datestr = datetime.datetime.strftime(datetime.datetime.now(),
        '%Y-%m-%d-%H:%M:%S')
    return name + datestr + suffix


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run experiment for UCT with '
                                                 'intrinsic motivation.')
    parser.add_argument('--intrinsic', '-i', action='store_true',
                        help='Should intrinsic motivation be used?')
    parser.add_argument('--mcsamples', '-m', type=int, default=5,
                        help='How many monte carlo runs should be made.')
    parser.add_argument('--runs', '-r', type=int, default=2,
                        help='How many runs should be made.')
    parser.add_argument('--steps', '-s', type=int, default=10,
                        help="Maximum number of steps performed.")
    parser.add_argument('--gamma', '-g', type=float, default=0.6,
                        help='The learning rate.')
    parser.add_argument('--uct_c', '-c', type=float, default=10,
                        help='The UCT parameter Cp.')

    args = parser.parse_args()


    myInterface = interface.TestInterface()
    currentProblem = myInterface.GetNextProblem()


    scores = []
    counter = 1
    while counter <= 400:
        if counter >= 0:
            print ("PROBLEM COUNTER", counter)
            scores.append(run_experiment(intrinsic_motivation=args.intrinsic, gamma=args.gamma,
                       mc_n=args.mcsamples, runs=args.runs, steps=args.steps,
                       c=args.uct_c, problem=currentProblem))
        currentProblem = myInterface.GetNextProblem()
        counter += 1

    print (sum(scores))
    print ("1 to 400")
    print (counter)
