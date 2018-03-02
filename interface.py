from painting import problem_interface as painting_interface
from alien_language import problem_interface as language_interface
from photobashing import problem_interface as photobashing_interface
from stories import problem_interface as story_interface
from desserts import problem_interface as dessert_interface


class Problem:
	def __init__(self, _problemType, _questionData, _initialKnowledgeBase, _function, _numArguments, _keyArgument, _scoreFunction, _target, _clearFunction):
		self.problemtype =_problemType
		self.questionData = _questionData
		self.knowledgeBase = _initialKnowledgeBase
		self.function = _function
		self.numArguments = _numArguments
		self.keyArgument = _keyArgument
		self.scoreFunction = _scoreFunction
		self.target = _target
		self.clearFunction = _clearFunction

	#Accept arguments as a list of numArguments length
	def ActivateFunction(self, args):
		self.questionData = self.function(args,self.questionData)

	#Returns a score [0.0,1.0] that expresses the extent to which questionData matches target
	def Score(self):
		return self.scoreFunction(self.questionData, self.target)

	#Clears current questionData
	def Clear(self):
		self.questionData = self.clearFunction(self.questionData)

class TestInterface:
	def __init__(self):
		#ALTER THIS LINE TO TEST ON A SUBSET OF DOMAINS
		self.interfaces = [painting_interface, language_interface, photobashing_interface, story_interface, dessert_interface]
		self.GetProblems()

	def GetProblems(self):
		problemLists = self.interfaces[0].GetProblems()
		self.interfaces = self.interfaces[1:]
		self.problems = []
		for p in problemLists:
			self.problems.append(Problem(p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8]))

	def GetNextProblem(self):
		if len(self.problems)>0:
			#pop next problem off stack
			self.currentProblem = self.problems[0]
			self.problems = self.problems[1:]
			return self.currentProblem
		else:
			if len(self.interfaces)>0:
				self.GetProblems()
				return self.GetNextProblem()
			else:
				return None



