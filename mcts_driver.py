from mymcts.test import *

import interface
import argparse
import random

from mymcts.paintingtest import *


myInterface = interface.TestInterface()
currentProblem = myInterface.GetNextProblem()


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

scores = []
counter = 1
while not currentProblem is None:
  # ptest_perform(currentProblem)

  #Solve problems

  print ("PROBLEM COUNTER", counter)
  scores.append(run_experiment(intrinsic_motivation=args.intrinsic, gamma=args.gamma,
                               mc_n=args.mcsamples, runs=args.runs, steps=args.steps,
                               c=args.uct_c, problem=currentProblem))
  currentProblem = myInterface.GetNextProblem()
  counter += 1

print (sum(scores))
print (sum(scores)/float(counter))