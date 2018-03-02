import random

class Recipe:
	def __init__(self, _name, _ingredients):
		self.name = _name
		self.ingredients = _ingredients

recipes = []
with open("./List of desserts.txt") as f:
    content = f.readlines()
    splits = content[0].split("\r")
    for c in splits:
    	nameAndInstructions = c.split("\t")
    	if len(nameAndInstructions)>1:
    		name = nameAndInstructions[0]
    		instructions = nameAndInstructions[1]
    		instructions = instructions.split(", ")
    		recipes.append(Recipe(name, instructions))

recipeListRep = []
for r in recipes:
	recipeListRep.append([r.name,r.ingredients])

#Construct combo options
comboOptions = []
for recipe in recipes:
	thisComboOptions = []
	for recipe2 in recipes:
		if not recipe.name==recipe2.name:
			numCommon = set(recipe.ingredients).intersection(set(recipe2.ingredients))
			if len(numCommon)>0:
				thisComboOptions.append(recipe2)
	#Check for complete coverage
	totalIngredients = []
	for c in thisComboOptions:
		for i in c.ingredients:
			if i in recipe.ingredients:
				totalIngredients.append(i)
	numCommon = set(recipe.ingredients).intersection(set(totalIngredients))
	if len(numCommon)==len(recipe.ingredients):
		comboOptions.append(thisComboOptions)
		
	else:
		comboOptions.append([])

#Construct combos
questions = []
for i in range(0, len(comboOptions)):
	if len(comboOptions[i])>0:
		goal = set(recipes[i].ingredients)
		for j in range(0, 500):
			size = random.randint(1,len(comboOptions[i]))
			inputs = []
			for z in range(0, size):
				inputs.append(random.choice(comboOptions[i]))

			#Check if valid
			totalIngredients = []
			for inp in inputs:
				for ing in inp.ingredients:
					if ing in goal:
						totalIngredients.append(ing)

			numCommon = goal.intersection(set(totalIngredients))
			if len(numCommon)==len(goal):
				stringRepInput = []
				for inp in inputs:
					stringRepInput.append([inp.name, inp.ingredients])
				stringRepOutput = [recipes[i].name, recipes[i].ingredients]
				question = [stringRepInput, stringRepOutput]
				if not question in questions:

					questions.append(question)

finalQuestions = []
while len(finalQuestions)<400:
    q = random.choice(questions)
    questions.remove(q)
    recipeIndexes = []
    for recipe in q[0]:
    	recipeIndexes.append(recipeListRep.index(recipe))
    finalQuestions.append([recipeIndexes, recipeListRep.index(q[1])])

print (finalQuestions)


finalQuestions.sort(lambda x,y: cmp(len(x[0]), len(y[0])))

print ("")
print ("SORTED")
print (finalQuestions)




