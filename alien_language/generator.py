import random


def FindComponentWords(chosenWord, l, words):
    inputWords = []
    foundQ = False
    if len(chosenWord)>2:
        for i in range(1, len(chosenWord)-1):
            wordA = chosenWord[0:i]
            wordB = chosenWord[i:len(chosenWord)]

            if wordA in l and wordB in l and (len(wordA)>1 or len(wordB)>1):
                foundQ = True
                for w in words:
                    if not w==chosenWord:
                        inputWords.append(w)
                inputWords.append(wordA)
                inputWords.append(wordB)

            if foundQ:
                break

            for j in range(i, len(chosenWord)-1):
                wordA = chosenWord[0:i]
                wordB = chosenWord[i:j]
                wordC = chosenWord[j:len(chosenWord)]
                if wordA in l and wordB in l and wordC in l and (len(wordA)>1 or len(wordB)>1):
                    foundQ = True
                    for w in words:
                        if not w==chosenWord:
                            inputWords.append(w)
                    inputWords.append(wordA)
                    inputWords.append(wordB)
                    inputWords.append(wordC)
                if foundQ:
                    break
            if foundQ:
                break
    return inputWords

# min word length is 2
# only contains characters ABCDWXYZ
# max sentence length is 5
# min sentence len is 2

# following function from: https://stackoverflow.com/questions/17174891/how-can-i-generate-all-possible-strings-given-a-grammar-rule
def generate_strings(rule):
    if not rule:
        yield ""
    else:
        begin, end = rule[0], rule[1:]
        if begin == '[':
            i = end.find(']')
            if i == -1:
                raise ValueError("Unmatched '['")
            optional, end = end[:i], end[i+1:]
            for e in generate_strings(end):
                yield e
                yield optional + e
        elif begin == '(':
            i = end.find(')')
            if i == -1:
                raise ValueError("Unmatched '('")
            parts, end = end[:i].split('|'), end[i+1:]

            for e in generate_strings(end):
                for p in parts:
                    yield p + e
        elif begin in '])|':
            raise ValueError("Unexpected " + begin)
        else:
            for e in generate_strings(end):
                yield begin + e

# l = list(generate_strings("A(B|C)D[X]YZ"))
# (A|S|D|E|R|T|N|)
# (P|Z|O|W|N|J|C|T|A|S|D|E|R|T|N|)
# (P|Z|O|W|N|J|C|T|)

# (A|B|C|D|)
# (W|X|Y|Z|)
# (A|B|C|D|W|X|Y|Z|)

# print list(generate_strings("(P|Z|O|W|N|J|C|T|A|S|D|E|R|T|N|)(P|Z|O|W|N|J|C|T|A|S|D|E|R|T|N|)(P|Z|O|W|N|J|C|T|A|S|D|E|R|T|N|)(P|Z|O|W|N|J|C|T|A|S|D|E|R|T|N|)(P|Z|O|W|N|J|C|T|A|S|D|E|R|T|N|)"))
# print list(generate_strings("(P|Z|O|W|N|J|C|T|A|S|D|E|R|T|N|)(P|Z|O|W|N|J|C|T|A|S|D|E|R|T|N|)(P|Z|O|W|N|J|C|T|A|S|D|E|R|T|N|)(P|Z|O|W|N|J|C|T|A|S|D|E|R|T|N|)(P|Z|O|W|N|J|C|T|A|S|D|E|R|T|N|)"))
l = list(set(generate_strings("(A|B|C|D|W|X|Y|Z)(A|B|C|D|W|X|Y|Z)(A|B|C|D|W|X|Y|Z|)(A|B|C|D|W|X|Y|Z|)")))
# print l

if '' in l:
    l.remove('')

for j in range(0, 2):
    for i in range(0, len(l)):
        randomOption = random.randint(0,4)
        if randomOption==0:
            l[i] = random.choice(l[i])
        elif randomOption==1:
            if (i+1)<(len(l)):
                l[i] = l[i]+l[i+1]
            else:
                l[i] = l[i]+l[i-1]
        elif randomOption ==2:
            l[i] = l[i][0:random.randint(1,len(l[i]))]
    l = list(set(l))

print
print len(l), " total words"
#print l



def valid_sentences(words, sentence_len, num_examples):
    # rules contains the letters that are NOT allowed to follow
    # i.e. a word ending with 'A' CANNOT be followed by a word beginning with 'D', 'X', or 'Z'
    rules = {'A':['D', 'X', 'Z'], 'B':['B', 'C', 'Z', 'X'], 'C':['A', 'B'], 'D':['B', 'D', 'W', 'Y',
    'Z'], 'W':['B', 'D', 'Z'], 'X':['B'], 'Y':[], 'Z':['C', 'D', 'Z']}
    sentences = []
    for x in range(num_examples):
        elem = []
        while len(elem) < sentence_len:
            next_word = words[int(random.random() * len(words))]
            if len(elem) is 0 or next_word[0] not in rules[elem[-1][-1]]:
                elem.append(next_word)
        # print elem
        sentences.append(elem)
    return sentences

# sentences = valid_sentences(l, 1, 10)
questions = []

#print "2 word sentences"
sentences = valid_sentences(l, 2, 200)

for sentence in sentences:
    words = sentence
    chosenWord = random.choice(words)
    foundQ = False
    inputWords = FindComponentWords(chosenWord, l, words)
    outputSentence = sentence
    if len(inputWords)>0:
        questions.append([inputWords,outputSentence])


    

#print sentences
#print
#print "3 word sentences"
sentences = valid_sentences(l, 3, 200)


for sentence in sentences:
    words = sentence
    chosenWord = random.choice(words)
    foundQ = False
    inputWords = FindComponentWords(chosenWord, l, words)
    outputSentence = sentence
    if len(inputWords)>0:
        questions.append([inputWords,outputSentence])



#print sentences
#print
#print "4 word sentences"
sentences = valid_sentences(l, 4, 200)

for sentence in sentences:
    words = sentence
    chosenWord = random.choice(words)
    foundQ = False
    inputWords = FindComponentWords(chosenWord, l, words)
    outputSentence = sentence

    if len(inputWords)>0:
        if random.randint(0,2)==0:
            questions.append([inputWords,outputSentence])
        else:
            chosenWord2 = random.choice(words)
            if not chosenWord2==chosenWord:
                inputWords2 = FindComponentWords(chosenWord2, l, words)
                if len(inputWords2)>0:
                    finalWords = list(set(inputWords+inputWords2))
                    finalQ = [finalWords, outputSentence]
                    questions.append(finalQ)

#print ("Question Size: "+str(len(questions)))
#print ("Questions: "+str(questions))
#print sentences
#print
#print "5 word sentences"
sentences = valid_sentences(l, 5, 200)

for sentence in sentences:
    words = sentence
    chosenWord = random.choice(words)
    foundQ = False
    inputWords = FindComponentWords(chosenWord, l, words)
    outputSentence = sentence

    if len(inputWords)>0:
        if random.randint(0,2)==0:
            questions.append([inputWords,outputSentence])
        else:
            chosenWord2 = random.choice(words)
            if not chosenWord2==chosenWord:
                inputWords2 = FindComponentWords(chosenWord2, l, words)
                if len(inputWords2)>0:
                    finalWords = list(set(inputWords+inputWords2))
                    finalQ = [finalWords, outputSentence]
                    questions.append(finalQ)


print ("Question Size: "+str(len(questions)))

finalQuestions = []
while len(finalQuestions)<400:
    q = random.choice(questions)
    questions.remove(q)
    finalQuestions.append(q)

print (finalQuestions)
#print sentences


