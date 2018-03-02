import questions

def AddWord(args, questionData):
	if len(args)==1:
		questionData.append(args[0])
	return questionData

def Score(questionData,target):
	differences = 0
	maxLength = max(len(target), len(questionData))
	for i in range(0, maxLength):
		if i>=len(questionData) or i>=len(target) or not target[i]==questionData[i]:
			differences+=1
	return float((float(maxLength)-differences)/float(maxLength))

def Clear(questionData):
	return []



#Full formulation of problems as list of problemType, questionData, initialKnowledgeBase, function, numArguments, keyArgument, scoreFunction, target, clear
def GetProblems():
	print ("loading language problems")
	questionData = questions.GetQuestions()
	problems = []
	for i in range(0, len(questionData)):
		problem = ["alien_language", [], questionData[i][0], AddWord, 1, 0, Score, questionData[i][1], Clear]
		problems.append(problem)
	print ("problems loaded")
	return problems