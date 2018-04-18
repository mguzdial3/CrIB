import interface
import random
import mimicry


myInterface = interface.TestInterface()
currentProblem = myInterface.GetNextProblem()



scores = []
while not currentProblem is None:
  qd = currentProblem.questionData

  # newQD = []

  # for x in range(len(qd)):
  #   for y in range(len(qd[x])):
  #     for z in range(len(qd[x][y])):
  #       newQD.append( int(100*(qd[x][y][z])) )

  # oldQD = [newQD[x:x+3] for x in range(len(newQD)) if x % 3 == 0]
  # oldQD = [oldQD[x:x+100] for x in range(len(oldQD)) if x % 100 == 0]

  newQD = [(0, 100) for x in range(30000)]

  print "MIMIC"
  m = mimicry.mimic.Mimic(newQD, currentProblem.ScoreQ, samples=1000, percentile=0.9)
  #Solve problems
  for i in range(10):
  	print i
  	submission = m.fit()
  	currentProblem.ActivateFunction(submission)

  scores.append(currentProblem.Score())
  currentProblem = myInterface.GetNextProblem()

print (sum(scores))
