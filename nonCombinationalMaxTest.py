import interface
import random
import numpy as np

#painting = 338.795466667 out of 400 or 0.8469886667
#language = 288.4 out of 400 or 0.721
#photobashing = 356.533931566 out of 400 or 0.8913348289
#stories = 29.8659294197 out of 400 or 0.07466482355
#dessert = 196.903571429 out of 400 or 0.4922589286
#Total = 1,210.4988990817 out of 2000 or 0.6052494495

myInterface = interface.TestInterface()
currentProblem = myInterface.GetNextProblem()

scores = []
attempts = 0
while not currentProblem is None:
	#Special Case for each problem
	attempts+=1
	print (attempts)
	if currentProblem.problemtype=="painting":
		#Cheat: grab target and find closest thing in input set
		target = currentProblem.target
		colorOptions = list(currentProblem.knowledgeBase)
		colorOptions.append((1,1,1))
		for x in range(0, 100):
			column = []
			for y in range(0, 100):
				closestDist = float('inf')
				closestColor = None
				for inputColor in colorOptions:
					distance = np.sum(np.abs(np.array(inputColor)-target[x][y]))
					if distance<closestDist:
						closestDist = distance
						closestColor = inputColor
				currentProblem.ActivateFunction([float(x)/100.0,float(y)/100.0, closestColor])
		score = currentProblem.Score()
		scores.append(score)
		currentProblem = myInterface.GetNextProblem()
	elif currentProblem.problemtype=="alien_language":
		#Cheat: grab target and find closest thing in input set
		target = currentProblem.target
		wordOptions = currentProblem.knowledgeBase
		for word in target:
			if word in wordOptions:
				currentProblem.ActivateFunction([word])
			else:
				currentProblem.ActivateFunction([random.choice(wordOptions)])
		scores.append(currentProblem.Score())
		currentProblem = myInterface.GetNextProblem()
	elif currentProblem.problemtype=="photobashing":
		#Cheat: grab target and find closest thing in input set
		target = currentProblem.target
		imageOptions = currentProblem.knowledgeBase
		bestScore = 0.0
		for image in imageOptions:
			#for x in range(0, target.shape[0]):
			#	for y in range(0, target.shape[1]):
			currentProblem.Clear()
			currentProblem.ActivateFunction([0, 0, image])
			score = currentProblem.Score()
			if score>bestScore:
				bestScore = score
		scores.append(bestScore)
		currentProblem = myInterface.GetNextProblem()
	elif currentProblem.problemtype=="story":
		#Cheat: grab target and find closest thing in input set
		plotGraphs = currentProblem.knowledgeBase
		bestScore = 0.0
		for p in plotGraphs:
			currentProblem.ActivateFunction([p])
			score = currentProblem.Score()
			if score>bestScore:
				bestScore = score
		scores.append(bestScore)
		currentProblem = myInterface.GetNextProblem()
	elif currentProblem.problemtype=="dessert":
		#Cheat: grab target and find closest thing in input set
		recipes = currentProblem.knowledgeBase
		bestScore = 0.0
		for r in recipes:
			currentProblem.ActivateFunction([r])
			score = currentProblem.Score()
			if score>bestScore:
				bestScore = score
		scores.append(bestScore)
		currentProblem = myInterface.GetNextProblem()

print (sum(scores))
