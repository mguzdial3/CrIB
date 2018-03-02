import random
from PIL import Image


def CircleDefine(canvas, minX, minY, maxX, maxY, color1, color2=None):
    center = [int((maxX-minX)/2.0)+minX, int((maxY-minY)/2.0)+minY]
    radius = min((((maxX-minX)/2.0)-1)**2,(((maxY-minY)/2.0)-1)**2)
    border = radius/8
    for x in range(minX, maxX):
        for y in range(minY, maxY):
            dist = ((x-center[0])**2)+((y-center[1])**2)
            if dist<radius-border:
                canvas[x][y] = color1
            elif dist<radius+border:
                if color2==None:
                    canvas[x][y] = color1
                else:
                    canvas[x][y] = color2
    return canvas

def SquareDefine(canvas, minX, minY, maxX, maxY, color1, color2=None):
    size = min(maxX-minX, maxY-minY)
    for x in range(minX, size+minX):
        for y in range(minY,size+minY):
            if x==minX or y==minY or x==(minX+size-1) or y==(minY+size-1):
                if color2==None:
                    canvas[x][y] = color1
                else:
                    canvas[x][y] = color2
            else:
                canvas[x][y] = color1
    return canvas

def RectangleDefine(canvas, minX, minY, maxX, maxY, color1, color2=None):
    for x in range(minX, maxX):
        for y in range(minY,maxY):
            if x==minX or y==minY or x==(maxX-1) or y==(maxY-1):
                if color2==None:
                    canvas[x][y] = color1
                else:
                    canvas[x][y] = color2
            else:
                canvas[x][y] = color1
    return canvas

def FindColorCombo(colors):
    goalColor = random.choice(colors)
    additiveDiff = 2
    subtractionDiff = 2
    inputColors = []
    while additiveDiff>0.5 and subtractionDiff>0.5 and len(inputColors)<3:
        rColor = random.choice(colors)
        if not rColor in inputColors and not rColor==goalColor:
            inputColors.append(rColor)

            totalColor =[0,0,0]
            maxColor = [0,0,0]
            maxSum = 0
            for i in inputColors:
                totalColor[0]+=i[0]
                totalColor[1]+=i[1]
                totalColor[2]+=i[2]
                if (sum(i)>maxSum):
                    maxColor = [i[0], i[1], i[2]]
                    maxSum = sum(i)

            for i in inputColors:
                if not i==maxColor:
                    maxColor[0]-=i[0]
                    maxColor[1]-=i[1]
                    maxColor[2]-=i[2]

            additiveDiff = abs(goalColor[0]-totalColor[0])+abs(goalColor[1]-totalColor[1])+abs(goalColor[2]-totalColor[2])
            subtractionDiff = abs(goalColor[0]+maxColor[0])+abs(goalColor[1]+maxColor[1])+abs(goalColor[2]+maxColor[2])

    if (additiveDiff<=0.5 or subtractionDiff<=0.5):
        return [inputColors,goalColor]
    else:
        return []

def ConstructCanvas():
    canvas = []
    for y in range(0, 100):
        line = []
        for x in range(0, 100):
            line.append([1,1,1])
        canvas.append(line)
    return canvas

primaryColors = [[1,0,0], [0,1,0], [0,0,1], [0.5,0,0], [0,0.5,0], [0,0,0.5]]
secondaryColors = [[1,1,0], [0,1,1], [1,0,1]]
tertiaryColors = [[1,0,0.5], [1,0.5,0], [0.5,1,0], [0,1,0.5], [0,0.5,1], [0.5,0,1]]

allowedColors = primaryColors+secondaryColors+tertiaryColors

colorCombos = []
for i in range(0, 10000):
    colorCombo = FindColorCombo(allowedColors)

    if not colorCombo in colorCombos and len(colorCombo)>0 and len(colorCombo[0])>1:
        colorCombos.append(colorCombo)

print(len(colorCombos))

shapeOptions = ["circle", "square", "rectangle"]
questions = []

while( len(questions)<400):
    if random.randint(0, 3)==0:
        #2 colors
        colorCombo1 = random.choice(colorCombos)
        colorCombo2 = random.choice(colorCombos)
        if not colorCombo1==colorCombo2:
            if random.randint(0,2)==0:
                #1 shape
                shape = random.choice(shapeOptions)
                question = [colorCombo1, colorCombo2, [shape]]
                if not question in questions:
                    questions.append(question)
            else:
                shape = random.choice(shapeOptions)
                shape2 = random.choice(shapeOptions)
                if not shape==shape2:
                    question = [colorCombo1, colorCombo2, [shape, shape2]]
                    if not question in questions:
                        questions.append(question)
    else:
        #2 colors
        colorCombo1 = random.choice(colorCombos)
        if random.randint(0,2)==0:
            #1 shape
            shape = random.choice(shapeOptions)
            question = [colorCombo1, [shape]]
            if not question in questions:
                questions.append(question)
        else:
            shape = random.choice(shapeOptions)
            shape2 = random.choice(shapeOptions)
            if not shape==shape2:
                question = [colorCombo1, [shape, shape2]]
                if not question in questions:
                    questions.append(question)

#print (questions)
#print (len(questions))
functionMap = {}
functionMap["circle"] = CircleDefine
functionMap["square"] = SquareDefine
functionMap["rectangle"] = RectangleDefine

finalQuestions = []
complexity = []
for q in questions:
    thisCanvas = ConstructCanvas()
    inputCs = []
    outputCs = []
    if len(q[len(q)-1])==1:
        if len(q)==2:
            outputCs.append(q[0][1])
            thisCanvas =  functionMap[q[1][0]](thisCanvas, random.randint(0,10), random.randint(0,10), random.randint(90,100), random.randint(90,100),  q[0][1])
            inputCs=q[0][0]
            complexity.append(2+len(inputCs))
        else:
            outputCs.append(q[0][1])
            outputCs.append(q[1][1])
            thisCanvas =  functionMap[q[2][0]](thisCanvas, random.randint(0,10), random.randint(0,10), random.randint(90,100), random.randint(90,100),  q[0][1], q[1][1])
            for i in q[0][0]:
                if not i in inputCs:
                    inputCs.append(i)
            for i in q[1][0]:
                if not i in inputCs:
                    inputCs.append(i)
            complexity.append(3+len(inputCs))

    else:
        if len(q)==2:
            outputCs.append(q[0][1])
            inputCs=q[0][0]
            if random.randint(0,2)==0:
                thisCanvas =  functionMap[q[1][0]](thisCanvas, random.randint(0,10), random.randint(0,10), random.randint(40,50), random.randint(90,100),  q[0][1])
                thisCanvas =  functionMap[q[1][1]](thisCanvas, random.randint(50,60), random.randint(0,10), random.randint(90,100), random.randint(90,100),  q[0][1])
            else:
                thisCanvas =  functionMap[q[1][0]](thisCanvas, random.randint(0,10), random.randint(0,10), random.randint(90,100), random.randint(40,50),  q[0][1])
                thisCanvas =  functionMap[q[1][1]](thisCanvas, random.randint(0,10), random.randint(50,60), random.randint(90,100), random.randint(90,100),  q[0][1])
            complexity.append(3+len(inputCs))
        else:
            outputCs.append(q[0][1])
            outputCs.append(q[1][1])
            for i in q[0][0]:
                if not i in inputCs:
                    inputCs.append(i)
            for i in q[1][0]:
                if not i in inputCs:
                    inputCs.append(i)
            complexity.append(4+len(inputCs))
            if random.randint(0,2)==0:
                if random.randint(0,2)==0:
                    thisCanvas =  functionMap[q[2][0]](thisCanvas, random.randint(0,10), random.randint(0,10), random.randint(40,50), random.randint(90,100),  q[0][1], q[1][1])
                    thisCanvas =  functionMap[q[2][1]](thisCanvas, random.randint(50,60), random.randint(0,10), random.randint(90,100), random.randint(90,100),  q[0][1], q[1][1])
                else:
                    thisCanvas =  functionMap[q[2][0]](thisCanvas, random.randint(0,10), random.randint(0,10), random.randint(40,50), random.randint(90,100),  q[1][1])
                    thisCanvas =  functionMap[q[2][1]](thisCanvas, random.randint(50,60), random.randint(0,10), random.randint(90,100), random.randint(90,100),  q[1][1])
            else:
                if random.randint(0,2)==0:
                    thisCanvas =  functionMap[q[2][0]](thisCanvas, random.randint(0,10), random.randint(0,10), random.randint(90,100), random.randint(40,50),  q[0][1], q[1][1])
                    thisCanvas =  functionMap[q[2][1]](thisCanvas, random.randint(0,10), random.randint(50,60), random.randint(90,100), random.randint(90,100),  q[0][1], q[1][1])
                else:
                    thisCanvas =  functionMap[q[2][0]](thisCanvas, random.randint(0,10), random.randint(0,10), random.randint(90,100), random.randint(40,50), q[1][1])
                    thisCanvas =  functionMap[q[2][1]](thisCanvas, random.randint(0,10), random.randint(50,60), random.randint(90,100), random.randint(90,100), q[1][1])
    thisQuestion = [inputCs,thisCanvas,outputCs]
    finalQuestions.append(thisQuestion)
finalQuestions = [x for _,x in sorted(zip(complexity,finalQuestions))]
justInputs = []
justOutputs = []
for i in range(0, 400):
    justInputs.append([finalQuestions[i][0]])
    justOutputs.append(finalQuestions[i][2])
    #print out image at this index
    im2 = Image.new("RGB", (100,100))
    pixels = im2.load()
    for x in range(0, 100):
        for y in range(0, 100):
            pixels[x,y] = (int(finalQuestions[i][1][x][y][0]*254), int(finalQuestions[i][1][x][y][1]*254), int(finalQuestions[i][1][x][y][2]*254))#so the half works out evenly
    im2.save("./questions/"+str(i)+".png", "PNG")
print("")
print (justInputs)
