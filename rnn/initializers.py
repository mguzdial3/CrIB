import numpy as np
import random
import copy

#parent class for category specific work. doesn't do anything, just nice to know
class Environment:

    def initialize(self, problem):
        return None

    def score(self, problem, candidate):
        return problem.scoreFunction(candidate, problem.target)

class Dessert(Environment):
    ingredients = None
    names = None
    allIngredients = None

    def initialize(self, interface):
        myInterface = interface.TestInterface()
        currentProblem = myInterface.GetNextProblem()
        p = 1
        allIngredients = []
        while not currentProblem is None:
            # print("problem: " + str(p))
            p += 1
            if currentProblem.problemType is "dessert":
                allIngredients += [y for x in currentProblem.knowledgeBase for y in x[1]]
            currentProblem = myInterface.GetNextProblem()
        allIngredients = list(set(allIngredients))
        # print len(allIngredients) # 128 ingredients
        self.allIngredients = allIngredients

    def initXY(self, problem):
        ingredients = [y for x in problem.knowledgeBase for y in x[1]]
        # print ingredients
        target = problem.target[1]
        # print target
        
        matrixIng = np.zeros((len(self.allIngredients)))
        matrixTarget = np.zeros((len(self.allIngredients)))
        for i, x in enumerate(self.allIngredients):
            if x in ingredients:
                matrixIng[i] = 1
            if x in target:
                matrixTarget[i] = 1

        # print matrixIng
        # print
        # print matrixTarget
        return matrixIng, matrixTarget

    def initTarget(self, problem):
        ingredients = [problem.target[1]]
        ## TODO: THIS IS WRONG
        names = [problem.target[0].split(' ')]
        # print ingredients
        # print self.ingredients
        # print names
        # print self.names
        matrix = np.zeros((1, len(self.ingredients) + len(self.names), 1))
 
        for i, x in enumerate(names):
            for e, y in enumerate(self.names):
                if y in x:
                    matrix[i][e] = 1
        # print self.names
        # print names
        # print allNames

        for i, x in enumerate(ingredients):
            for e, y in enumerate(self.ingredients):
                if y in x:
                    matrix[i][e + len(self.names)] = 1
        # print self.ingredients
        # print ingredients
        # print allIngredients

        # print matrix
        return matrix

    def convert(self, mat):
        nameMat = mat[0][:len(self.names)]
        ingMat = mat[0][len(self.names):]
        strName = ' '.join([self.names[i] for i, x in enumerate(nameMat) if x == 1])
        strIng = [self.ingredients[i] for i, x in enumerate(ingMat) if x == 1 ]
        return [strName, strIng]
