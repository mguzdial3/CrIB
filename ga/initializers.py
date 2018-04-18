import numpy as np
import random
import copy

#TODO: change representation to a set of actions.
#       currently taking advantage of known "hidden representaiton" of each problem type
#TODO: can bring pixel level to components at rgb
#TODO: Lang at char level, No credit for partial words
#TODO: narrative, swap out contents of the nodes

#actionspace of painting and photobash are very large.
#num generations needs to be very large to even have enough actions
#story's intermediate state can not be graded in the same manner as the rest of the classes.
#In other words, can't really get intermediate without applying a function onto the state
'''
Typo in interface.problem. self.problemtype
In the paper, limitations and future work, "desert"
In narrative, "this was down to"
'''

#parent class for category specific work. doesn't do anything, just nice to know
class Environment:

    def initialize(self, problem, population_size):
        return None

    def mutate(self, problem, entity):
        return entity

    def crossover(self, problem, candidates):
        return candidates[0]

    def score(self, problem, candidate):
        return problem.scoreFunction(candidate, problem.target)

class Painter(Environment):
    def initialize(self, problem, population_size):
        population = []
        for i in range(population_size):
            e = np.ones([100, 100, 3])
            population.append(e)
        return population

    def mutate(self, problem, entity):
        #TODO: maybe open the action space to full area?
        new = np.copy(entity)
        kb = problem.knowledgeBase
        action = kb[random.randint(0, len(kb) - 1)]
        action[1] = kb[random.randint(0, len(kb) - 1)][1]
        action[2] = kb[random.randint(0, len(kb) - 1)][2]
        return problem.function([random.random(), random.random(), action], new)

    def crossover(self, problem, candidates):
        e1, e2 = candidates

        return None

class Language(Environment):
    def initialize(self, problem, population_size):
        population = [[random.choice(problem.knowledgeBase)] for i in range(population_size)]
        return population

    def mutate(self, problem, entity):
        #suffers from not being able to combine words
        new = [x for x in entity]
        if random.randint(0, 1) is 1 and len(new) > 0:
            alter = random.randint(0, len(new) - 1)
            new[alter] = new[alter] + random.choice(''.join(problem.knowledgeBase))
            return new
        else:
            new_word = random.choice(''.join(problem.knowledgeBase))
            return problem.function(new_word, new)

    def crossover(self, problem, candidates):
        e1, e2 = candidates
        e1 = ' '.join(e1)
        e2 = ' '.join(e2)

        w1 = e1[:random.randint(0, len(e1))]
        w2 = e2[:random.randint(0, len(e2))]

        return (w1 + w2).split(' ')

class PhotoBash(Environment):
    def initialize(self, problem, population_size):
        return [[] for i in range(population_size)]

    #action is 3 arg, x,y bottom left coordinate as [0,1] and z numpy array "image"
    def mutate(self, problem, entity):
        # new = np.copy(entity)
        new = copy.deepcopy(entity)
        action = [random.randint(0,1), random.randint(0,1), random.choice(problem.knowledgeBase)]
        choice = random.randint(0, len(new))
        if choice < len(entity):
            new[choice] = action
        else:
            new.append(action)
        return new

    def crossover(self, problem, candidates):
        e1, e2 = candidates
        return None

    def score(self, problem, candidate):
        problem.Clear()
        for i in range(len(candidate)):
            problem.ActivateFunction(candidate[i])
        return problem.Score()

class Story(Environment):
    def initialize(self, problem, population_size):
        population = []
        kb = problem.knowledgeBase
        for i in range(population_size):
            population.append(random.choice(kb))
        return population

    def mutate(self, problem, entity):
        new = entity.Clone()
        kb_story = random.choice(problem.knowledgeBase)
        newevent = random.choice(kb_story.nodes).eventName
        print(random.choice(new.nodes))
        # (random.choice(new.nodes)).eventName = newevent
        return new
        # return entity

    def crossover(self, problem, candidates):
        e1, e2 = candidates
        return None

    def score(self, problem, candidate):
        return problem.scoreFunction(problem.function([x], ["", problem.target]), problem.target)

class Dessert(Environment):
    ingredients = None
    names = None

    def initialize(self, problem, population_size):
        ingredients = [x[1][i] for x in problem.knowledgeBase for i in range(len(x[1]))]
        self.ingredients = list(set(ingredients))
        self.names = (' '.join([x[0] for x in problem.knowledgeBase])).split(' ')

        population = []
        for i in range(population_size):
            name = random.choice(self.names)
            num_ingredients = random.randint(0, len(self.ingredients) - 1)
            ingreds = random.sample(self.ingredients, num_ingredients)
            population.append([name, ingreds])

        return population

    def mutate(self, problem, entity):
        #the function literally takes in full answers, no building up to
        name = entity[0].split(' ')
        ingredients = [x for x in entity[1]]
        action = random.randint(0, 3)
        '''
        0 - remove from name
        1 - add to name
        2 - remove from ingredients
        3 - add to ingredients
        '''
        if action is 0:
            choice = random.choice(name)
            name = [x for x in name if x is not choice]
        elif action is 1 and len(name) < len(self.names):
            choice = random.choice([x for x in self.names if x not in name])
            name.append(choice)
        elif action is 2 and len(ingredients) > 0:
            choice = random.choice(ingredients)
            ingredients = [x for x in ingredients if x is not choice]
        elif len(ingredients) < len(self.ingredients):
            choice = random.choice([x for x in self.ingredients if x not in ingredients])
            ingredients.append(choice)
        name = ' '.join(name)
        return [name, ingredients]

    def crossover(self, problem, candidates):
        e1, e2 = candidates
        return None
