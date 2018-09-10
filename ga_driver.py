import interface
import random
import numpy as np
import ga.initializers as initi

num_iterations = 5
prob_mutation = 0.7
population_size = 10
#choose first x candidates
num_parent = 20
num_children = 20

#driver method. Abstract evolution from class-dependent mutations
def evolve(problem, init):
    population = init.initialize(problem, population_size)

    for i in range(num_iterations):
        #do crossover
        first_x = population[:num_parent]
        co = [init.crossover(problem, (random.choice(first_x) , random.choice(first_x))) for _ in range(num_children)]
        if co[0] is not None:
            population = population + co

        # do mutation
        for j in range(population_size):
            entity = population[j]
            if random.random() <= prob_mutation * 100:
                mutation = init.mutate(problem, entity)
                population.append(mutation)
        population = sorted(population, key = lambda x: init.score(problem, x), reverse=True)
        population = population[:population_size]
        # print(population[:population_size])
        # print(map(lambda x: init.score(problem, x), population)[:10])
        # print(problem.scoreFunction(population[0], problem.target))
    return population[0]


myInterface = interface.TestInterface()
currentProblem = myInterface.GetNextProblem()
initializers = [initi.Painter(), initi.Language(), initi.PhotoBash(), initi.Story(), initi.Dessert()]

scores = []
p = 1
while not currentProblem is None:
    print("problem: " + str(p))
    # raw_input()
    p += 1

    answer = ''
    if currentProblem.problemType is "painting":
        #278.4
        currentProblem.questionData = evolve(currentProblem, initializers[0])
        pass
    elif currentProblem.problemType is "alien_language":
        #131.27
        currentProblem.questionData = evolve(currentProblem, initializers[1])
        pass
    elif currentProblem.problemType is "photobashing":
        #357.37
        candidate = evolve(currentProblem, initializers[2])
        currentProblem.Clear()
        for i in range(len(candidate)):
            currentProblem.ActivateFunction(candidate[i])
        pass
    elif currentProblem.problemType is "story":
        #178.578222594
        #Currently stuck on problem 45, infinite recursion error
        qd = currentProblem.function([evolve(currentProblem, initializers[3])], [None, currentProblem.target])
        currentProblem.questionData = qd
        pass
    elif currentProblem.problemType is "dessert":
        #267.75
        print currentProblem.knowledgeBase
        print 
        currentProblem.questionData = evolve(currentProblem, initializers[4])
        print currentProblem.questionData
        print
        print
        print
        pass
    scores.append(currentProblem.Score())
    currentProblem = myInterface.GetNextProblem() if p < 4 else None

print (sum(scores))
