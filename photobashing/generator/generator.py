import random, glob, os
from PIL import Image

directories = ["./camel/", "./cow/", "./deer/", "./rhino/", "./pig/", "./zebra/", "./kangaroo/"]
animalNames = ["camel", "cow", "deer", "rhino", "pig", "zebra", "kangaroo"]

torsoToPartsInfo ={}

torsoToPartsInfo["./camel/torso-54x11.jpg"] = [[54, 98, 62, 88], [127, 86, 35, 98], [161, 40, 74, 56]]
torsoToPartsInfo["./cow/torso-22x15.jpg"] = [[50, 78, 51, 143], [194, 126, 49, 88], [243, 20, 90, 73]]
torsoToPartsInfo["./deer/torso-30x83.jpg"] = [[38, 141, 37, 66], [95, 144, 61, 67], [104, 9, 84, 127]]
torsoToPartsInfo["./kangaroo/torso-0x0.jpg"] = [[104, 84, 86, 125], [191, 90, 51, 32], [241, 2, 59, 95]]
torsoToPartsInfo["./pig/torso-0x0.jpg"] = [[42, 93, 62, 88], [150, 110, 40, 65], [184, 40, 95, 134]]
torsoToPartsInfo["./rhino/torso-0x0.jpg"] = [[7, 83, 64, 66], [143, 90, 54, 66], [197, 12, 117, 146]]
torsoToPartsInfo["./zebra/torso-0x0.jpg"] = [[0, 73, 57, 96], [100, 92, 107, 90], [189, 8, 88, 122]]

imageNames = []
for d in directories:

    for images in glob.glob(d+"*.jpg"):
        imageNames.append(images)

finalFilenames = []
for images in glob.glob("./output/*.jpeg"):
    filename = images.split("/")
    finalFilenames.append(filename[2])


combinations = []
parts = ["torso", "backlegs", "frontlegs", "head"]
for i in range(0, 3000):
    #print ("I: "+str(i))
    finished = False
    thisCombo = ["", "", "", ""]
    while not finished:
        #print (thisCombo)
        randomChoice = random.choice(imageNames)
        for p in range(0, len(parts)):
            if parts[p] in randomChoice:
                if len(thisCombo[p])==0:
                    thisCombo[p]=randomChoice

        finished = ("torso" in thisCombo[0]) and ("backlegs" in thisCombo[1]) and ("frontlegs" in thisCombo[2]) and ("head" in thisCombo[3])
        #print ([("torso" in thisCombo[0]), ("backlegs" in thisCombo[1]), ("frontlegs" in thisCombo[2]), ("head" in thisCombo[3])])
    directoriesIn = []
    for d in directories:
        for j in range(0, 4):
            if d in thisCombo[j]:
                if not d in directoriesIn:
                    directoriesIn.append(d)

    if len(directoriesIn)>1 and not thisCombo in combinations:
        combinations.append(thisCombo)

print (len(combinations))
#combinations
from PIL import Image

for c in range(0, len(combinations)):
    im = Image.new("RGB", (350, 350), "white")
    pixels = im.load()

    outputName = ""

    for i in range(0, 4):
        for a in animalNames:
            if a in combinations[c][i]:
                if not a in outputName:
                    outputName+=a+"-"

        fileName = combinations[c][i]
        fileName = fileName.split(parts[i])[1]
        fileName = fileName.split("-")[1]
        fileName = fileName.split(".")[0]
        xy = fileName.split("x")
        loadedIm = Image.open(combinations[c][i])
        width, height = loadedIm.size
        xy[0] = int(xy[0])
        xy[1] = int(xy[1])
        if i>0:
            xy = [torsoToPartsInfo[combinations[c][0]][i-1][0], torsoToPartsInfo[combinations[c][0]][i-1][1]]
            #print (xy)
            oldWidth = torsoToPartsInfo[combinations[c][0]][i-1][2]
            oldHeight = torsoToPartsInfo[combinations[c][0]][i-1][3]
            maxMultiple = max(float(oldWidth/float(width)), float(oldHeight/float(height)))
            #if (maxMultiple<2):
            #print ("")
            #print (combinations[c][i])
            #print(combinations[c][0])
            #print (maxMultiple)
            if(abs(maxMultiple-1.0))<0.5:
                loadedIm = loadedIm.resize([oldWidth, oldHeight])
        #print (xy)
        
        width, height = loadedIm.size
        firstHit = False
        for x in range(xy[0], width+xy[0]):
            for y in range(xy[1], height+xy[1]):
                px = loadedIm.getpixel((x-xy[0], y-xy[1]))
                if i==0:
                    pixels[x,y] = px
                elif (255-px[0])>5 and (255-px[1])>5 and (255-px[2])>5:
                    pixels[x,y] = px

    maxX = 0
    maxY = 0
    for y in range(0, 350):
        for x in range(0, 350):
            px = im.getpixel((x,y))
            
            if not px==(255,255,255):
                if x>maxX:
                    maxX = x+5
                if y>maxY:
                    maxY = y+5
    im = im.crop([0,0,maxX,maxY])
    outputName = outputName[0:len(outputName)-1]
    #print (outputName)
    test = "./output/"+outputName+".jpeg"

    if not test in finalFilenames:
        im.save("./extras/"+outputName+".jpeg", "JPEG")

