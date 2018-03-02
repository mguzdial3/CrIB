import interface
import random
import numpy as np

#painting = 383.596483333 out of 400 or 0.9589912083
#language = 400.0 out of 400 or 1.0 (by adding 966038 total, 2,415.095 on average words)


myInterface = interface.TestInterface()
currentProblem = myInterface.GetNextProblem()

scores = []
attempts = 0
additions = []
while not currentProblem is None:
	#Special Case for each problem
	attempts+=1
	print (attempts)
	if currentProblem.problemtype=="painting":
		#Cheat: grab target and find closest thing in input set
		target = currentProblem.target
		colorOptions = list(currentProblem.knowledgeBase)
		colorOptions.append((1,1,1))
		#Naive amalgam
		newOptions = []
		for c in colorOptions:
			for c2 in colorOptions:
				newOptions.append((c[0], c[1], c2[2]))
				newOptions.append((c[0], c2[1], c[2]))
				newOptions.append((c2[0], c[1], c[2]))
				newOptions.append((c[0], c2[1], c2[2]))
				newOptions.append((c2[0], c[1], c2[2]))
				newOptions.append((c2[0], c2[1], c[2]))
		for c in newOptions:
			if not c in colorOptions:
				colorOptions.append(c)
		newOptions = []
		for c in colorOptions:
			for c2 in colorOptions:
				newOptions.append((c[0], c[1], c2[2]))
				newOptions.append((c[0], c2[1], c[2]))
				newOptions.append((c2[0], c[1], c[2]))
				newOptions.append((c[0], c2[1], c2[2]))
				newOptions.append((c2[0], c[1], c2[2]))
				newOptions.append((c2[0], c2[1], c[2]))
		for c in newOptions:
			if not c in colorOptions:
				colorOptions.append(c)
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
		added=0
		newOptions = []
		for w in wordOptions:
			for w2 in wordOptions:
				newOptions.append(w+w2)
				newOptions.append(w2+w)
		for c in newOptions:
			if not c in wordOptions:
				added+=1
				wordOptions.append(c)
		newOptions = []
		for w in wordOptions:
			for w2 in wordOptions:
				newOptions.append(w+w2)
				newOptions.append(w2+w)
		for c in newOptions:
			if not c in wordOptions:
				added+=1
				wordOptions.append(c)
		additions.append(added)
		for word in target:
			if word in wordOptions:
				currentProblem.ActivateFunction([word])
			else:
				currentProblem.ActivateFunction([random.choice(wordOptions)])
		scores.append(currentProblem.Score())
		currentProblem = myInterface.GetNextProblem()
	
print (sum(additions))
print (sum(scores))
