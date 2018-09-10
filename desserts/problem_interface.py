import questions

def Submit(args, questionData):
	if len(args)==1 and len(args[0])==2:
		questionData = args[0]
	return questionData

def Score(questionData,target):
	#titleScore
	inputTitle = questionData[0].split(' ')
	targetTitle = target[0].split(' ')
	titleDifferences = len(set(inputTitle).intersection(set(targetTitle)))
	titleScore = 0.5*(float(titleDifferences)/float(len(targetTitle)))
	#ingredientsScore
	inputIngredients = set(questionData[1])
	targetIngredients = set(target[1])
	ingredientDifferences = len(inputIngredients.intersection(targetIngredients))
	ingredientsScore = 0.5*(float(ingredientDifferences)/float(len(targetIngredients)))
	return (titleScore+ingredientsScore)

def allScore(y_true,y_pred):
	#titleScore
	total = 0
	for y in range(len(y_pred)):
		questionData = y_pred[y]
		target = y_true[y]

		inputTitle = questionData[0].split(' ')
		targetTitle = target[0].split(' ')
		titleDifferences = len(set(inputTitle).intersection(set(targetTitle)))
		titleScore = 0.5*(float(titleDifferences)/float(len(targetTitle)))
		#ingredientsScore
		inputIngredients = set(questionData[1])
		targetIngredients = set(target[1])
		ingredientDifferences = len(inputIngredients.intersection(targetIngredients))
		ingredientsScore = 0.5*(float(ingredientDifferences)/float(len(targetIngredients)))
		total += titleScore+ingredientsScore
	return float(total)/len(y_pred)

def Clear(questionData):
	return ['', []]

#Full formulation of problems as list of problemType, questionData, initialKnowledgeBase, function, numArguments, keyArgument, scoreFunction, target, clear
def GetProblems():
	recipes = []
	with open("./desserts/List of desserts.txt") as f:
	    content = f.readlines()
	    splits = content[0].split("\r")
	    for c in splits:
	    	nameAndInstructions = c.split("\t")
	    	if len(nameAndInstructions)>1:
	    		name = nameAndInstructions[0]
	    		instructions = nameAndInstructions[1]
	    		instructions = instructions.split(", ")
	    		recipes.append([name, instructions])


	print ("loading dessert problems")
	questionData = questions.GetQuestions()
	problems = []
	for i in range(0, len(questionData)):
		inputRecipes = []
		for inputRecipeIndex in questionData[i][0]:
			inputRecipes.append(recipes[inputRecipeIndex])


		problem = ["dessert", ['', ['']], inputRecipes, Submit, 1, 0, Score, recipes[questionData[i][1]], Clear]
		problems.append(problem)
	print ("problems loaded")
	return problems