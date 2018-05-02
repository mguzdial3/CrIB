from __future__ import division

from painting_world_state import *

def ptest_perform(problem):
    n = 1000

    world = PaintingWorld((100, 100), False, (100, 100), problem)
    # belief = dict(zip([PaintingWorldAction(),
    #                    PaintingWorldAction(),
    #                    PaintingWorldAction(),
    #                    PaintingWorldAction(np.array([-1, 0]))],
    #                   [[10, 1, 1, 1], [1, 10, 1, 1], [1, 1, 10, 1],
    #                    [1, 1, 1, 10]]))

    state = PaintingWorldState((0,0), (0,0,0),world)
    belief = {}
    for action in state.actions:
      belief[action] = [1]*len(state.actions)
    state.belief = belief


    outcomes = np.array([0.] * len(state.actions))
    for i in range(n):
        new_state = state.perform(state.actions[0])
        # print(new_state.belief[state.actions[0]])

        # if new_state.belief[state.actions[0]][0] == 2:
        #     outcomes[0] += 1
        # elif new_state.belief[state.actions[0]][1] == 2:
        #     outcomes[1] += 1
        # elif new_state.belief[state.actions[0]][2] == 2:
        #     outcomes[2] += 1
        # elif new_state.belief[state.actions[0]][3] == 2:
        #     outcomes[3] += 1

        for x in xrange(len(new_state.belief[state.actions[0]])):
          if new_state.belief[state.actions[0]][x] == 2:
            outcomes[x] += 1

    print(outcomes)

    deviation = 3./np.sqrt(n)
    outcomes /= float(n)
    print(outcomes)
    expectation = np.array(belief[state.actions[0]])/\
                  sum(belief[state.actions[0]])

    # print expectation
    # print deviation
    assert (expectation - deviation < outcomes).all()
    assert (outcomes < expectation + deviation).all()


# ptest_perform()

# mcts = MCTS(tree_policy=UCB1(c=1.41),
#                 default_policy=immediate_reward,
#                 backup=monte_carlo)

# root = StateNode(MazeState([0, 0]))
# best_action = mcts(root)