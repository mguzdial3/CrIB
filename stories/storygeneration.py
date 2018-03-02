import random

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

def checkForOverlap(storyA, storyB):
	#check event type overlap
	overlaps = set(storyA.eventClasses).intersection(set(storyB.eventClasses))
	if len(overlaps)>1 and random.randint(0,2)>1:
		return [0, overlaps]

	#check word overlap
	wordsA = []
	for n in storyA.nodes:
		wordSplits = n.eventName.split(" ")
		wordsA +=wordSplits
	wordsB = []
	for n in storyB.nodes:
		wordSplits = n.eventName.split(" ")
		wordsB +=wordSplits

	wordsA.remove("A")
	if "B" in wordsA:
		wordsA.remove("B")
	wordsB.remove("A")
	if "B" in wordsB:
		wordsB.remove("B")


	overlaps = set(wordsA).intersection(set(wordsB))
	if overlaps>2:
		return [1, overlaps]

	return []

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

stories = [BuildPharmacy(), BuildRobbery(), BuildMovie(), BuildStageCoach(), BuildTourBus(), BuildCattleDriver(), BuildCatLover(), BuildFantasy(), BuildInheritance(), BuildAnchorhead()]
storyFunctions= [BuildPharmacy, BuildRobbery, BuildMovie, BuildStageCoach, BuildTourBus, BuildCattleDriver, BuildCatLover, BuildFantasy, BuildInheritance, BuildAnchorhead]
#Combo stories
questions = []

outputStories = []
#Am I looking for a story or a new plot graph
for i in range(0, 10000):
	print str(i)
	storyA = random.choice(stories)

	storyACopy = storyFunctions[stories.index(storyA)]()
	storyA = storyACopy
	storyB = random.choice(storyFunctions)()
	#storyC = random.choice(storyFunctions)()
	#storyD = random.choice(storyFunctions)()

	someReplacement = False
	if not storyA.storyName==storyB.storyName: #and not storyA.storyName==storyC.storyName and not storyB.storyName==storyC.storyName:
		overlaps = checkForOverlap(storyA, storyB)
		differences = 0
		if overlaps[0]==0:
			#Find and swap overlaps at uniform random probability
			replacements =[]
			for nA in storyA.nodes:
				if nA.eventClass in overlaps[1]:
					options = []
					for nB in storyB.nodes:
						if nB.eventClass==nA.eventClass:
							options.append(nB)
					if (random.randint(0,2)==1):
						replacements.append([nA, random.choice(options)])
			for r in replacements:
				someReplacement = True
				indexA = storyA.nodes.index(r[0])
				storyA.nodes[indexA] = r[1]
				r[1].parents = r[0].parents
				r[1].negations = r[0].negations

				indexB = storyB.nodes.index(r[1])
				for i in range(indexB+1, len(storyB.nodes)):
					storyA.AddNode(storyB.nodes[i])
		elif overlaps[0]==1:
			#Find and swap overlaps at uniform random probability
			replacements =[]
			for nA in storyA.nodes:
				anOverlap = False
				wordOverlap = ""
				words = nA.eventName.split(" ")
				for word in words:
					if word in overlaps[1]:
						anOverlap = True
						wordOverlap = word
						break
				if anOverlap:
					options = []
					for nB in storyB.nodes:
						if wordOverlap in nB.eventName:
							options.append(nB)
					if (random.randint(0,2)==1):
						replacements.append([nA, random.choice(options)])
			for r in replacements:
				someReplacement = True
				indexA = storyA.nodes.index(r[0])
				storyA.nodes[indexA] = r[1]
				r[1].parents = r[0].parents
				r[1].negations = r[0].negations

				for node in storyA.nodes:
					if r[0] in node.parents:
						node.parents.remove(r[0])
						node.parents.append(r[1])
					elif r[0] in node.negations:
						node.negations.remove(r[0])
						node.negations.append(r[1])


				indexB = storyB.nodes.index(r[1])
				for i in range(indexB+1, len(storyB.nodes)):
					storyA.AddNode(storyB.nodes[i])
		'''
		#STORYC
		overlaps = checkForOverlap(storyA, storyC)
		differences = 0
		if overlaps[0]==0:
			#Find and swap overlaps at uniform random probability
			replacements =[]
			for nA in storyA.nodes:
				if nA.eventClass in overlaps[1]:
					options = []
					for nB in storyC.nodes:
						if nB.eventClass==nA.eventClass:
							options.append(nB)
					if (random.randint(0,2)==1):
						replacements.append([nA, random.choice(options)])
			for r in replacements:
				someReplacement = True
				indexA = storyA.nodes.index(r[0])
				storyA.nodes[indexA] = r[1]
				r[1].parents = r[0].parents
				r[1].negations = r[0].negations

				indexB = storyC.nodes.index(r[1])
				for i in range(indexB+1, len(storyC.nodes)):
					storyA.AddNode(storyC.nodes[i])
		elif overlaps[0]==1:
			#Find and swap overlaps at uniform random probability
			replacements =[]
			for nA in storyA.nodes:
				anOverlap = False
				wordOverlap = ""
				words = nA.eventName.split(" ")
				for word in words:
					if word in overlaps[1]:
						anOverlap = True
						wordOverlap = word
						break
				if anOverlap:
					options = []
					for nB in storyC.nodes:
						if wordOverlap in nB.eventName:
							options.append(nB)
					if (random.randint(0,2)==1):
						replacements.append([nA, random.choice(options)])
			for r in replacements:
				someReplacement = True
				indexA = storyA.nodes.index(r[0])
				storyA.nodes[indexA] = r[1]
				r[1].parents = r[0].parents
				r[1].negations = r[0].negations

				for node in storyA.nodes:
					if r[0] in node.parents:
						node.parents.remove(r[0])
						node.parents.append(r[1])
					elif r[0] in node.negations:
						node.negations.remove(r[0])
						node.negations.append(r[1])


				indexB = storyC.nodes.index(r[1])
				for i in range(indexB+1, len(storyC.nodes)):
					storyA.AddNode(storyC.nodes[i])
		'''
		'''
		#STORYD
		overlaps = checkForOverlap(storyA, storyD)
		differences = 0
		if overlaps[0]==0:
			#Find and swap overlaps at uniform random probability
			replacements =[]
			for nA in storyA.nodes:
				if nA.eventClass in overlaps[1]:
					options = []
					for nB in storyD.nodes:
						if nB.eventClass==nA.eventClass:
							options.append(nB)
					if (random.randint(0,2)==1):
						replacements.append([nA, random.choice(options)])
			for r in replacements:
				someReplacement = True
				indexA = storyA.nodes.index(r[0])
				storyA.nodes[indexA] = r[1]
				r[1].parents = r[0].parents
				r[1].negations = r[0].negations

				indexB = storyD.nodes.index(r[1])
				for i in range(indexB+1, len(storyD.nodes)):
					storyA.AddNode(storyD.nodes[i])
		elif overlaps[0]==1:
			#Find and swap overlaps at uniform random probability
			replacements =[]
			for nA in storyA.nodes:
				anOverlap = False
				wordOverlap = ""
				words = nA.eventName.split(" ")
				for word in words:
					if word in overlaps[1]:
						anOverlap = True
						wordOverlap = word
						break
				if anOverlap:
					options = []
					for nB in storyD.nodes:
						if wordOverlap in nB.eventName:
							options.append(nB)
					if (random.randint(0,2)==1):
						replacements.append([nA, random.choice(options)])
			for r in replacements:
				someReplacement = True
				indexA = storyA.nodes.index(r[0])
				storyA.nodes[indexA] = r[1]
				r[1].parents = r[0].parents
				r[1].negations = r[0].negations

				for node in storyA.nodes:
					if r[0] in node.parents:
						node.parents.remove(r[0])
						node.parents.append(r[1])
					elif r[0] in node.negations:
						node.negations.remove(r[0])
						node.negations.append(r[1])


				indexB = storyD.nodes.index(r[1])
				for i in range(indexB+1, len(storyD.nodes)):
					storyA.AddNode(storyD.nodes[i])
		'''
		#Generate a story
		storyText = ""
		notEnded = True
		activatedNodes = 0
		attempts = 0
		initialLength = len(storyA.nodes)
		storiesRepresented = []

		while (len(storyA.nodes)>0 and notEnded and attempts<500):
			attempts+=1
			currNode = random.choice(storyA.nodes)
			if activatedNodes==0 and attempts>10:
				currNode = storyA.nodes[0]
			if not currNode.activated:
				output = currNode.Activate()
				if len(output)>0:

					if not currNode.fromStory in storiesRepresented:
						storiesRepresented.append(currNode.fromStory)

					storyText+=output+". "
					if currNode.eventClass=="end":
						notEnded = False
					activatedNodes+=1
					storyA.nodes.remove(currNode)
		print (str([activatedNodes,len(storyA.nodes), notEnded, attempts]))
		if attempts<500 and len(storiesRepresented)==2:#CHANGE ME

			newQuestion = [storyA.storyName, storyB.storyName, storyText]
			if not newQuestion in outputStories:
				#print ("NEW QUESTION: "+str(newQuestion))
				outputStories.append(newQuestion)

print(outputStories)
print (len(outputStories))










