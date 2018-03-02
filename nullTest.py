import interface

#painting = 278.319666667 out of 400 or 0.6957991667
#language = 0.0 out of 400 or 0.0
#photobashing = 302.416826922 out of 400 or 0.7560420673
#stories = 0.0 out of 400 or 0.0
#dessert = 0.0 out of 400 or 0.0
#Total = 580.736493589 out of 2000 or 0.2903682468

myInterface = interface.TestInterface()
currentProblem = myInterface.GetNextProblem()

scores = []
while not currentProblem is None:
	#Solve problems
	scores.append(currentProblem.Score())
	currentProblem = myInterface.GetNextProblem()

print (sum(scores))
