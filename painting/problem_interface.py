from PIL import Image
import questions
import numpy as np
from scipy import ndimage

def isFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def Paint(args, questionData):
	if len(args)==3 and isFloat(args[0]) and isFloat(args[1]) and len(args[2])==3:
		questionData[int(args[0]*100)][int(args[1]*100)] = args[2]
	return questionData

def Score(questionData,target):
	return np.divide(30000.0-np.sum(np.absolute(questionData-target)),30000.0)

def Clear(questionData):
	return ConstructCanvas()

def ConstructCanvas():
	return np.ones((100,100,3))

#Full formulation of problems as list of problemType, questionData, initialKnowledgeBase, function, numArguments, keyArgument, scoreFunction, target, clear
def GetProblems():
	print ("loading painting problems")
	questionData = questions.GetQuestionInputs()
	problems = []
	for i in range(0, len(questionData)):
		#Open image
		target = np.array(ndimage.imread("./painting/questions/"+str(i)+".png"))
		target = np.divide(target, 254.0)

		problem = ["painting", ConstructCanvas(), questionData[i][0], Paint, 3, 2, Score, target, Clear]
		problems.append(problem)
	print ("problems loaded")
	return problems



