import questions

class StoryPlotNode:
	def __init__(self, _eventName, _eventClass):
		self.eventName = _eventName
		self.eventClass = _eventClass
		self.activated = False
		self.parents = []
		self.negations = []
		self.fromStory = ""

	def AddParent(self, nodeA):
		if not nodeA in self.parents:
			self.parents.append(nodeA)

	def AddNegation(self, nodeA):
		if not nodeA in self.negations:
			self.negations.append(nodeA)

	#returns eventName if can activate, false otherwise
	def Activate(self):
		canRun = True
		for p in self.parents:
			if not p.activated:
				canRun = False
				break

		if canRun:
			for n in self.negations:
				if n.activated:
					canRun = False
					break

		if canRun:
			self.activated = True
			return self.eventName
		else:
			return ""

	def CanActivate(self):
		if self.activated:
			return False
		canRun = True
		for p in self.parents:
			if not p.activated:
				canRun = False
				break

		if canRun:
			for n in self.negations:
				if n.activated:
					canRun = False
					break

		if canRun:
			return True
		else:
			return False


class Story:
	def __init__(self, _storyName):
		self.storyName = _storyName
		self.nodes = []
		self.eventClasses = []

	def AddNode(self, node):
		if node.fromStory == "":
			node.fromStory = self.storyName
		self.nodes.append(node)
		self.eventClasses.append(node.eventClass)

	def Clone(self):
		newStory = Story(self.storyName)
		newNodes = []
		for node in self.nodes:
			cloneNode = StoryPlotNode(node.eventName, node.eventClass)
			cloneNode.activated=node.activated
			cloneNode.fromStory=node.fromStory
			newNodes.append(cloneNode)
		for n in range(0, len(self.nodes)):
			for parent in self.nodes[n].parents:
				newNodes[n].parents.append(newNodes[self.nodes.index(parent)])
			for negation in self.nodes[n].negations:
				newNodes[n].negations.append(newNodes[self.nodes.index(negation)])

		for n in newNodes:
			newStory.AddNode(n)
		return newStory


	def PossibleActivations(self):
		possibleNodes = []
		for node in self.nodes:
			if node.CanActivate():
				possibleNodes.append(node)
		return possibleNodes

#Graphs 

#1 PHARMACY

def BuildPharmacy():
	pharmacy = Story("pharmacy")
	node1 = StoryPlotNode("A orders drugs", "intro")
	node2 = StoryPlotNode("B asks for prescription", "")
	node2.AddParent(node1)
	node3 = StoryPlotNode("A produces prescription", "")
	node3.AddParent(node2)
	node4 = StoryPlotNode("A can't produce prescription", "")
	node4.AddParent(node2)
	node3.AddNegation(node4)
	node4.AddNegation(node3)
	node5 = StoryPlotNode("B checks prescription", "")
	node5.AddParent(node3)
	node6 = StoryPlotNode("B refuses to sell", "")
	node6.AddParent(node4)
	node7 = StoryPlotNode("A leaves", "end")
	node7.AddParent(node6)
	node8 = StoryPlotNode("B delivers drugs", "")
	node8.AddParent(node5)
	node9 = StoryPlotNode("A pays cash", "payment")
	node10 = StoryPlotNode("A swipes a card", "payment")
	node10.AddNegation(node9)
	node9.AddNegation(node10)
	node10.AddParent(node8)
	node9.AddParent(node8)
	node11 = StoryPlotNode("A takes change", "payment2")
	node11.AddParent(node9)
	node12 = StoryPlotNode("A takes receipt", "payment2")
	node12.AddParent(node9)
	node13 = StoryPlotNode("A takes receipt", "payment2")
	node13.AddParent(node10)
	node14 = StoryPlotNode("A leaves", "end")
	node14.AddParent(node12)
	node15 = StoryPlotNode("A leaves", "end")
	node15.AddParent(node15)

	nodes = [node1, node2, node3, node4, node5, node6, node7, node8, node9, node10, node11, node12, node13, node14, node15]
	for n in nodes:
		pharmacy.AddNode(n)
	return pharmacy

#2 Robbery
def BuildRobbery():
	robbery = Story("robbery")
	node1 = StoryPlotNode("A enters bank", "intro")
	node2 = StoryPlotNode("A sees B", "")
	node2.AddParent(node1)
	node3 = StoryPlotNode("A scans bank", "")
	node3.AddParent(node1)
	node4 = StoryPlotNode("A waits in line", "")
	node4.AddParent(node1)
	node5 = StoryPlotNode("A covers face", "mystery")
	node6 = StoryPlotNode("A approaches B", "meet")
	node7 = StoryPlotNode("B greets A", "meet")
	node7.AddNegation(node5)
	node8 = StoryPlotNode("B is scared", "fear")
	node8.AddParent(node6)
	node8.AddParent(node5)
	node8 = StoryPlotNode("B is scared", "fear")
	node8.AddParent(node6)
	node9 = StoryPlotNode("A pulls out gun", "threaten")
	node9.AddParent(node6)
	node10 = StoryPlotNode("A demands money", "threaten")
	node10.AddParent(node9)
	node11 = StoryPlotNode("B collects money", "")
	node11.AddParent(node10)
	node12 = StoryPlotNode("B presses alarm", "")
	node12.AddParent(node10)
	node13 = StoryPlotNode("Police arrive", "danger")
	node13.AddParent(node12)
	node14 = StoryPlotNode("Police arrest A", "end")
	node14.AddParent(node13)
	node15 = StoryPlotNode("B gives A money", "payment")
	node15.AddParent(node11)
	node16 = StoryPlotNode("A leaves bank", "")
	node16.AddParent(node15)
	node17 = StoryPlotNode("A gets in car", "enter vehicle")
	node17.AddParent(node16)
	node18 = StoryPlotNode("A drives away", "end")
	node18.AddParent(node17)
	nodes = [node1, node2, node3, node4, node5, node6, node7, node8, node9, node10, node11, node12, node13, node14, node15, node16, node17, node18]
	for n in nodes:
		robbery.AddNode(n)
	return robbery

#3 Movie 
def BuildMovie():
	movie = Story("movie")
	node1 = StoryPlotNode("A drives to B's house", "intro")
	node2 = StoryPlotNode("A meets B", "meet")
	node2.AddParent(node1)
	node3 = StoryPlotNode("A drives to theater", "transport")
	node3.AddParent(node2)
	node4 = StoryPlotNode("A parks car", "")
	node4.AddParent(node3)
	node5 = StoryPlotNode("A buys tickets", "")
	node5.AddParent(node4)
	node6 = StoryPlotNode("A and B enter the theater", "")
	node6.AddParent(node5)
	node7 = StoryPlotNode("A and B buy popcorn", "")
	node7.AddParent(node5)
	node8 = StoryPlotNode("A and B buy drinks", "")
	node8.AddParent(node5)
	node9 = StoryPlotNode("A and B buy popcorn and soda", "")
	node9.AddParent(node5)
	node7.AddNegation(node9)
	node9.AddNegation(node7)
	node8.AddNegation(node9)
	node9.AddNegation(node8)
	node10 = StoryPlotNode("A and B sit down", "")
	node10.AddParent(node6)
	node7.AddNegation(node10)
	node8.AddNegation(node10)
	node9.AddNegation(node10)
	node11 = StoryPlotNode("Movie begins", "")
	node11.AddParent(node10)
	node12 = StoryPlotNode("A and B talk", "social interaction")
	node12.AddParent(node11)
	node13 = StoryPlotNode("A and B hold hands", "social interaction")
	node13.AddParent(node12)
	node14 = StoryPlotNode("A and B enjoy the movie", "")
	node14.AddParent(node11)
	node15 = StoryPlotNode("A uses the bathroom", "")
	node15.AddParent(node11)
	node16 = StoryPlotNode("A and B kiss", "social interaction")
	node16.AddParent(node14)
	node17 = StoryPlotNode("Movie ends", "")
	node17.AddParent(node15)
	node17.AddParent(node14)
	node17.AddParent(node12)
	node18 = StoryPlotNode("A and B leave the theater", "")
	node18.AddParent(node17)
	node19 = StoryPlotNode("A and B walk to car", "enter vehicle")
	node19.AddParent(node18)
	node20 = StoryPlotNode("B says goodbye to A", "end")
	node20.AddParent(node19)

	nodes = [node1, node2, node3, node4, node5, node6, node7, node8, node9, node10, node11, node12, node13, node14, node15, node16, node17, node18, node19, node20]
	for n in nodes:
		movie.AddNode(n)
	return movie

#4 STAGECOACH
def BuildStageCoach():
	stagecoach = Story("stagecoach")
	node1 = StoryPlotNode("A arrives with Stagecoach", "intro")
	node2 = StoryPlotNode("A waits", "wait")
	node2.AddParent(node1)
	node3 = StoryPlotNode("B enters Stagecoach", "")
	node3.AddParent(node1)
	node2.AddNegation(node3)
	node4 = StoryPlotNode("B tells A to go to the White House", "")
	node4.AddParent(node3)
	node5 = StoryPlotNode("A departs with B", "")
	node5.AddParent(node4)
	node6 = StoryPlotNode("A converses with B", "social interaction")
	node6.AddParent(node5)
	node7 = StoryPlotNode("A informs B of arrival", "")
	node7.AddParent(node5)
	node8 = StoryPlotNode("A and B arrive at White House", "end")
	node8.AddParent(node7)

	nodes = [node1, node2, node3, node4, node5, node6, node7, node8]
	for n in nodes:
		stagecoach.AddNode(n)
	return stagecoach

#5 Tour Bus
def BuildTourBus():
	tourBus = Story("tourBus")
	node1 = StoryPlotNode("A arrives at Boarding Location", "intro")
	node2 = StoryPlotNode("A tells B to board bus", "")
	node2.AddParent(node1)
	node3 = StoryPlotNode("B boards bus", "")
	node3.AddParent(node2)
	node4 = StoryPlotNode("A welcomes B", "social interaction")
	node4.AddParent(node3)
	node5 = StoryPlotNode("A departs with B", "")
	node5.AddParent(node4)
	node6 = StoryPlotNode("A and B visit a Landmark", "")
	node6.AddParent(node5)
	node7 = StoryPlotNode("A asks B whats next", "social interaction")
	node7.AddParent(node6)
	node8 = StoryPlotNode("A and B arrive at Boarding Location", "end")
	node8.AddParent(node6)

	nodes = [node1, node2, node3, node4, node5, node6, node7, node8]
	for n in nodes:
		tourBus.AddNode(n)
	return tourBus

#6 Cat Lover
def BuildCatLover():
	catLover = Story("catLover")
	node1 = StoryPlotNode("A begins the day", "intro")
	node2 = StoryPlotNode("A feeds cats", "")
	node2.AddParent(node1)
	node3 = StoryPlotNode("A walks to river", "")
	node3.AddParent(node2)
	node5 = StoryPlotNode("A sees frightened cat at river", "")
	node5.AddParent(node3)
	node6 = StoryPlotNode("A puts on gloves", "")
	node6.AddParent(node5)
	node7 = StoryPlotNode("A rescues cat", "")
	node7.AddParent(node6)
	node8 = StoryPlotNode("Cat injures A", "")
	node8.AddParent(node7)

	node4 = StoryPlotNode("A slips", "")
	node4.AddParent(node2)
	node9 = StoryPlotNode("A hits the ground", "")
	node9.AddParent(node4)
	node10 = StoryPlotNode("A injures arm", "")
	node10.AddParent(node9)
	node11 = StoryPlotNode("A bandages arm", "")
	node11.AddParent(node10)

	node12 = StoryPlotNode("A arrives home with cat", "")
	node12.AddParent(node11)
	node12.AddParent(node8)

	node13 = StoryPlotNode("A sneezes", "end")
	node13.AddParent(node12)

	nodes = [node1, node2, node3, node4, node5, node6, node7, node8, node9, node10, node11, node12, node13]
	for n in nodes:
		catLover.AddNode(n)
	return catLover

#7 Cattle driver
def BuildCattleDriver():
	cattleDriver = Story("cattleDriver")
	node1 = StoryPlotNode("A begins the day", "intro")
	node2 = StoryPlotNode("A rides horse", "")
	node2.AddParent(node1)
	node3 = StoryPlotNode("A smacks saddle", "")
	node3.AddParent(node2)
	node4 = StoryPlotNode("A slips", "")
	node4.AddParent(node3)
	node5 = StoryPlotNode("A hits the ground", "")
	node5.AddParent(node4)
	node6 = StoryPlotNode("A injures arm", "")
	node6.AddParent(node5)
	node7 = StoryPlotNode("A bandages arm", "")
	node7.AddParent(node6)

	node8 = StoryPlotNode("A arrives at river", "")
	node8.AddParent(node3)
	node9 = StoryPlotNode("A finds a frightened cow", "")
	node9.AddParent(node8)
	node10 = StoryPlotNode("A rescues cow", "")
	node10.AddParent(node9)
	node11 = StoryPlotNode("A returns with cow", "end")
	node11.AddParent(node10)

	nodes = [node1, node2, node3, node4, node5, node6, node7, node8, node9, node10, node11]
	for n in nodes:
		cattleDriver.AddNode(n)
	return cattleDriver

#8 Fantasy
def BuildFantasy():
	fantasy = Story("fantasy")
	node1 = StoryPlotNode("Monster holds B captive", "intro")
	node2 = StoryPlotNode("A slays monster", "danger")
	node2.AddParent(node1)
	node3 = StoryPlotNode("A rescues B", "")
	node3.AddParent(node2)
	node4 = StoryPlotNode("B falls in love with A", "social interaction")
	node4.AddParent(node2)
	node5 = StoryPlotNode("A and B kiss", "")
	node5.AddParent(node3)
	node6 = StoryPlotNode("A and B get married", "")
	node6.AddParent(node5)
	node6.AddParent(node4)
	node7 = StoryPlotNode("A and B live happily ever after", "end")
	node7.AddParent(node6)

	nodes = [node1, node2, node3, node4, node5, node6, node7]
	for n in nodes:
		fantasy.AddNode(n)
	return fantasy

#9 Inheritance
def BuildInheritance():
	inheritance = Story("inheritance")
	node1 = StoryPlotNode("A gets partial inheritance", "intro")
	node2 = StoryPlotNode("A goes to bar", "intro")
	node3 = StoryPlotNode("A learns about uncle", "intro")
	node4 = StoryPlotNode("A attends funeral", "")
	node4.AddParent(node1)
	node5 = StoryPlotNode("A meets B", "meet")
	node5.AddParent(node4)
	node6 = StoryPlotNode("A refuses inheritance", "end")
	node6.AddParent(node5)
	node7 = StoryPlotNode("A collects inheritance", "end")
	node7.AddParent(node5)

	nodes = [node1, node2, node3, node4, node5, node6, node7]
	for n in nodes:
		inheritance.AddNode(n)
	return inheritance

#10 Anchorhead
def BuildAnchorhead():
	anchorhead = Story("anchorhead")
	node1 = StoryPlotNode("A leaves house", "intro")
	node2 = StoryPlotNode("A gets flask", "")
	node2.AddParent(node1)
	node3 = StoryPlotNode("A meets B", "meet")
	node3.AddParent(node1)
	node4 = StoryPlotNode("A gives B flask", "")
	node4.AddParent(node3)
	node4.AddParent(node2)
	node5 = StoryPlotNode("A talks to B", "social interaction")
	node5.AddParent(node4)
	node6 = StoryPlotNode("A finds magic shop", "")
	node6.AddParent(node1)
	node7 = StoryPlotNode("A gets amulet", "")
	node7.AddParent(node6)
	node8 = StoryPlotNode("A gives B amulet", "")
	node8.AddParent(node7)
	node8.AddParent(node3)
	node9 = StoryPlotNode("B tells A about sewer", "")
	node9.AddParent(node8)
	node10 = StoryPlotNode("A discovers book in sewer", "end")
	node10.AddParent(node9)
	node11 = StoryPlotNode("A finds secret observatory", "danger")
	node11.AddParent(node1)
	node12 = StoryPlotNode("A discovers safe", "")
	node12.AddParent(node1)
	node13 = StoryPlotNode("A learns safe combo", "")
	node13.AddParent(node1)
	node14 = StoryPlotNode("A opens safe", "")
	node14.AddParent(node12)
	node14.AddParent(node13)
	node15 = StoryPlotNode("A opens a puzzle box", "")
	node15.AddParent(node14)
	node15.AddParent(node6)
	node16 = StoryPlotNode("A sees evil god", "end")
	node16.AddParent(node15)
	node16.AddParent(node11)
	node17 = StoryPlotNode("A gets crypt key", "")
	node17.AddParent(node1)
	node18 = StoryPlotNode("A finds coffin", "")
	node18.AddParent(node17)
	node19 = StoryPlotNode("A gets skull", "")
	node19.AddParent(node18)
	node20 = StoryPlotNode("A shows B skull", "social interaction")
	node20.AddParent(node19)
	node20.AddParent(node3)

	nodes = [node1, node2, node3, node4, node5, node6, node7, node8, node9, node10, node11, node12, node13, node14, node15, node16, node17, node18, node19, node20]
	for n in nodes:
		anchorhead.AddNode(n)
	return anchorhead

#find all stories and return as questionData
def Submit(args, questionData):
	if len(args)==1 and isinstance(args[0], Story):
		questionData= []
		allActivated = False
		stories = [[args[0], ""]]
		attempts = 0
		while len(stories)>0 and attempts<1000:#cut off for potential cycles 
			attempts+=1
			currStory = stories[0]
			stories = stories[1:]
			allPossibleActivations = currStory[0].PossibleActivations()
			for node in allPossibleActivations:
				clone = currStory[0].Clone()
				newSentence = clone.nodes[currStory[0].nodes.index(node)].Activate()
				newStory = ""+currStory[1]+newSentence+". "
				stories.append([clone,newStory])
				if node.eventClass=="end" or len(allPossibleActivations)==1:
					questionData.append(newStory)
	return questionData

#find most similar story and find the distance [0,1]
def Score(questionData,target):
	targetSplits = target.split(". ")
	maxDifferences = 0
	relevantMaxLength = 0
	for story in questionData:
		storySplits = story.split(". ")
		differences = 0
		maxLength = max(len(targetSplits), len(storySplits))
		for t in range(0, maxLength):
			if t>len(storySplits)-1 or t>len(targetSplits)-1 or not targetSplits[t]==storySplits[t]:
				differences+=1
		if differences>maxDifferences:
			relevantMaxLength = maxLength
			maxDifferences = differences
	if relevantMaxLength==0:
		return relevantMaxLength
	return float((float(relevantMaxLength-maxDifferences))/float(relevantMaxLength))

#Clear
def Clear(questionData):
	return []

#Full formulation of problems as list of problemType, questionData, initialKnowledgeBase, function, numArguments, keyArgument, scoreFunction, target, clear
def GetProblems():
	storyTitleToGraphMapping = {}
	storyTitleToGraphMapping["pharmacy"] = BuildPharmacy
	storyTitleToGraphMapping["movie"] = BuildMovie
	storyTitleToGraphMapping["robbery"] = BuildRobbery
	storyTitleToGraphMapping["stagecoach"] = BuildStageCoach
	storyTitleToGraphMapping["tourBus"] = BuildTourBus
	storyTitleToGraphMapping["catLover"] = BuildCatLover
	storyTitleToGraphMapping["cattleDriver"] = BuildCattleDriver
	storyTitleToGraphMapping["fantasy"] = BuildFantasy
	storyTitleToGraphMapping["inheritance"] = BuildInheritance
	storyTitleToGraphMapping["anchorhead"] = BuildAnchorhead


	print ("loading story problems")
	questionData = questions.GetQuestions()
	problems = []
	for i in range(0, len(questionData)):
		storyGraphs = []
		for s in range(0, len(questionData[i])-1):
			storyGraphs.append(storyTitleToGraphMapping[questionData[i][s]]())

		problem = ["story", [], storyGraphs, Submit, 1, 0, Score, questionData[i][len(questionData[i])-1], Clear]
		problems.append(problem)
	print ("problems loaded")
	return problems