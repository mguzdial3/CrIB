# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import numpy as np
from scipy.stats import rv_discrete, entropy
from copy import deepcopy
from collections import defaultdict




class PaintingWorldAction(object):
    def __init__(self, x, y, r, g, b):
        self.action = (x, y, r, g, b)
        self.move = x,y
        self.color = r,g,b
        self._hash = 100*(x+2) + 10*(y+2) + r**2+g**2+b**2

    def __hash__(self):
        return int(self._hash)

    def __eq__(self, other):
        # (x, y, r, g, b) = self.action
        # a = np.array([x,y,r,g,b])
        # (x, y, r, g, b) = other.action
        # b = np.array([x,y,r,g,b])
        return (np.array(self.action) == np.array(other.action)).all()

    def __str__(self):
        return str(self.action)

    def __repr__(self):
        return str(self.action)


class PaintingWorld(object):
    def __init__(self, size, information_gain, goal, problem):
        self.size = np.asarray(size)
        self.colors = [[(1.,1.,1.) for _ in xrange(100)] for n in xrange(100)]
        self.information_gain = information_gain
        self.goal = np.asarray(goal)
        self.problem = problem


class PaintingWorldState(object):
    def __init__(self, pos, color, world, belief=None):
        self.pos = pos
        self.color = color
        self.world = world
        self.actions = [PaintingWorldAction(x,y,r/float(4),g/float(4),b/float(4)) for x in range(-1, 2) for y in range(-1, 2) for r in range(5) for g in range(5) for b in range(5)]

        # self.actions = [PaintingWorldAction( 0, 0, 1., 1., 1.),
        #                 PaintingWorldAction( 0, 1, 1., 1., 1.),
        #                 PaintingWorldAction( 1, 0, 1., 1., 1.),
        #                 PaintingWorldAction(-1, 0, 1., 1., 1.),
        #                 PaintingWorldAction( 0,-1, 1., 1., 1.),
        #                 PaintingWorldAction( 0, 0, 0., 0., 0.),
        #                 PaintingWorldAction( 0, 1, 0., 0., 0.),
        #                 PaintingWorldAction( 1, 0, 0., 0., 0.),
        #                 PaintingWorldAction(-1, 0, 0., 0., 0.),
        #                 PaintingWorldAction( 0,-1, 0., 0., 0.),
        #                 PaintingWorldAction( 0, 0, 1., 0., 0.),
        #                 PaintingWorldAction( 0, 1, 1., 0., 0.),
        #                 PaintingWorldAction( 1, 0, 1., 0., 0.),
        #                 PaintingWorldAction(-1, 0, 1., 0., 0.),
        #                 PaintingWorldAction( 0,-1, 1., 0., 0.),
        #                 PaintingWorldAction( 0, 0, 0., 1., 0.),
        #                 PaintingWorldAction( 0, 1, 0., 1., 0.),
        #                 PaintingWorldAction( 1, 0, 0., 1., 0.),
        #                 PaintingWorldAction(-1, 0, 0., 1., 0.),
        #                 PaintingWorldAction( 0,-1, 0., 1., 0.),
        #                 PaintingWorldAction( 0, 0, 0., 0., 1.),
        #                 PaintingWorldAction( 0, 1, 0., 0., 1.),
        #                 PaintingWorldAction( 1, 0, 0., 0., 1.),
        #                 PaintingWorldAction(-1, 0, 0., 0., 1.),
        #                 PaintingWorldAction( 0,-1, 0., 0., 1.),
        #                 PaintingWorldAction( 0, 0, 1., 1., 0.),
        #                 PaintingWorldAction( 0, 1, 1., 1., 0.),
        #                 PaintingWorldAction( 1, 0, 1., 1., 0.),
        #                 PaintingWorldAction(-1, 0, 1., 1., 0.),
        #                 PaintingWorldAction( 0,-1, 1., 1., 0.),
        #                 PaintingWorldAction( 0, 0, 0., 1., 1.),
        #                 PaintingWorldAction( 0, 1, 0., 1., 1.),
        #                 PaintingWorldAction( 1, 0, 0., 1., 1.),
        #                 PaintingWorldAction(-1, 0, 0., 1., 1.),
        #                 PaintingWorldAction( 0,-1, 0., 1., 1.),
        #                 PaintingWorldAction( 0, 0, 1., 0., 1.),
        #                 PaintingWorldAction( 0, 1, 1., 0., 1.),
        #                 PaintingWorldAction( 1, 0, 1., 0., 1.),
        #                 PaintingWorldAction(-1, 0, 1., 0., 1.),
        #                 PaintingWorldAction( 0,-1, 1., 0., 1.),]

        if belief:
            self.belief = belief
        else:
            self.belief = dict((a, np.array([1] * len(self.actions))) for a in self.actions)

    def _correct_position(self, pos):
        upper = np.min(np.vstack((pos, self.world.size)), 0)
        return np.max(np.vstack((upper, np.array([0, 0]))), 0)

    def perform(self, action):
        # get distribution about outcomes
        probabilities = self.belief[action] / np.sum(self.belief[action])
        distrib = rv_discrete(values=(range(len(probabilities)),
                                      probabilities))

        # draw sample
        sample = distrib.rvs()

        # update belief accordingly
        belief = deepcopy(self.belief)
        belief[action][sample] += 1

        # build next state
        pos = self._correct_position(tuple(map(sum, zip(self.pos, self.actions[sample].move))))
        self.world.colors[self.pos[0]][self.pos[1]] = self.actions[sample].color
        return PaintingWorldState(pos, self.actions[sample].color, self.world, belief)

    def real_world_perform(self, action):
        # update belief accordingly
        belief = deepcopy(self.belief)
        for i, a in enumerate(self.actions):
            if action.action == a.action:
                real_action = i
                break
        belief[action][real_action] += 1

        pos = self._correct_position(tuple(map(sum, zip(self.pos, action.move))))
        return PaintingWorldState(pos, action.color, self.world, belief)


    def is_terminal(self):
        return False

    def __eq__(self, other):
        return (self.pos == other.pos).all()

    def __hash__(self):
        return int(self.pos[0]*100 + self.pos[1])

    def __str__(self):
        return str(self.pos) + str(self.color)

    def __repr__(self):
        return str(self.pos) + str(self.color)

    def reward(self, parent, action):
        problem = self.world.problem
        # print ("reward!!", problem.scoreFunction(self.world.colors, problem.target))

        return problem.scoreFunction(self.world.colors, problem.target)


        # if (self.pos == self.world.goal).all():
        #     print("g", end="")
        #     return 100
        # else:
        #     reward = -1
        #     if self.world.information_gain:
        #         for a in self.actions:
        #             reward += entropy(parent.belief[a], self.belief[a])
        #     return reward