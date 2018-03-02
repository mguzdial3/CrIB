import random, glob, os
from PIL import Image

filenames = []
countsOfDashes = []
for f in glob.glob("./questions/*.jpeg"):
    fileName = f.split("/")[-1]
    filenames.append(fileName)
    countsOfDashes.append(len(fileName.split("-")))

sortedFilenames = [x for _,x in sorted(zip(countsOfDashes,filenames))]
print (sortedFilenames)
