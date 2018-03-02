import interface
import random

#painting = 278.238216667 out of 400 or 0.6955955417
#language = 18.1 out of 400 or 0.04525
#photobashing = 291.273528387 out of 400 or 0.728183821
#stories = 11.560197624 out of 400 or 0.02890049406
#dessert = 95.3720238095 out of 400 or 0.238
#Total = 680.7623105835 out of 2000 or 0.3403811553

myInterface = interface.TestInterface()
currentProblem = myInterface.GetNextProblem()

scores = []
while not currentProblem is None:
	#Solve problems
	for i in range(0, 10):#10 random activations
		submission = []
		for i in range(0, currentProblem.numArguments):
			if i==currentProblem.keyArgument:
				submission.append(random.choice(currentProblem.knowledgeBase))
			else:
				submission.append(random.random())
		currentProblem.ActivateFunction(submission)
	scores.append(currentProblem.Score())
	currentProblem = myInterface.GetNextProblem()

print (sum(scores))
