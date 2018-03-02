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

def Stamp(args, questionData):
	if len(args)==3 and isFloat(args[0]) and isFloat(args[1]):
		minX = int(args[0]*questionData.shape[0])
		minY = int(args[1]*questionData.shape[1])
		maxX = min((int(args[0]*questionData.shape[0]+args[2].shape[0])), questionData.shape[0])
		maxY = min(int(args[1]*questionData.shape[1]+args[2].shape[1]), questionData.shape[1])
		for x in range(minX, maxX):
			for y in range(minY, maxY):
				questionData[x][y] = args[2][x-minX][y-minY]
	return questionData

def Score(questionData,target):
	return np.divide( (questionData.shape[0]*questionData.shape[1]*questionData.shape[2]*255) -np.sum(np.absolute(questionData-target)),(questionData.shape[0]*questionData.shape[1]*questionData.shape[2]*255))

def Clear(questionData):
	return np.multiply(np.ones(questionData.shape),255.0)

def ConstructCanvas(target):
	return np.multiply(np.ones(target.shape),255.0)

#Full formulation of problems as list of problemType, questionData, initialKnowledgeBase, function, numArguments, keyArgument, scoreFunction, target, clear
def GetProblems():
	print ("loading photobashing problems")
	questionData = questions.GetQuestionFilenames()
	problems = []
	for i in range(0, len(questionData)):
		#Open image
		target = np.array(ndimage.imread("./photobashing/questions/"+str(questionData[i])))
		inputNames = questionData[i][:-5]#remove .jpeg
		inputNames = inputNames.split("-")
		inputs = []
		for questionName in inputNames:
			inputs.append(np.array(ndimage.imread("./photobashing/palette/input-"+str(questionName)+".jpeg", mode='RGB')))
		problem = ["photobashing", ConstructCanvas(target), inputs, Stamp, 3, 2, Score, target, Clear]
		problems.append(problem)
	print ("problems loaded")
	return problems



