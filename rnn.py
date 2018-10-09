import rnn.initializers as initi

import interface
import random, time
import numpy as np
import random
import tflearn
# from sklearn.model_selection import train_test_split

def allScore(y_true,y_pred):
  #titleScore
  total = 0
  for y in range(len(y_pred)):
    questionData = y_pred[y]
    target = y_true[y]

    # inputTitle = questionData[0].split(' ')
    # targetTitle = target[0].split(' ')
    # titleDifferences = len(set(inputTitle).intersection(set(targetTitle)))
    # titleScore = 0.5*(float(titleDifferences)/float(len(targetTitle)))
    #ingredientsScore
    inputIngredients = set(questionData)
    targetIngredients = set(target)
    ingredientDifferences = len(inputIngredients.intersection(targetIngredients))
    ingredientsScore = 0.5*(float(ingredientDifferences)/float(len(targetIngredients)))
    # total += titleScore+ingredientsScore
    total += 2*ingredientsScore
  return float(total)/len(y_pred)

def train_rnn(x_train, y_train, init):

    # Network building
    net = tflearn.input_data([None, int(x_train.shape[1])])
    net = tflearn.embedding(net, input_dim=int(x_train.shape[0]), output_dim=int(x_train.shape[1]))
    net = tflearn.lstm(net, int(x_train.shape[1]), dropout=0.9, return_seq=True)
    net = tflearn.lstm(net, int(x_train.shape[1]/2), dropout=0.9)
    # net = tflearn.lstm(net, int(x_train.shape[1]/2))
    net = tflearn.fully_connected(net, int(x_train.shape[1]), activation='softmax')
    net = tflearn.regression(net, optimizer='rmsprop', learning_rate=1e-6,
                             loss='categorical_crossentropy')


    model = tflearn.DNN(net, tensorboard_verbose=0)
    model.fit(x_train, y_train, show_metric=True,
              batch_size=1, n_epoch=10)

    return model

def random_seq_list(l, maxlen):
    random.seed(int(round(time.time.time() * 1000)))
    idx0 = random.sample(range(len(l)), 1)
    idx1 = idx0 + random.randint(0, maxlen - 1)
    if idx1 >= len(l):
        return l[idx0:]
    return l[idx0:idx1]


def lstm(text, word_idx, maxlen):

    g = tflearn.input_data(shape=[None, maxlen, len(word_idx)])
    g = tflearn.lstm(g, 512, return_seq=True)
    g = tflearn.dropout(g, 0.5)
    g = tflearn.lstm(g, 512)
    g = tflearn.dropout(g, 0.5)
    g = tflearn.fully_connected(g, len(word_idx), activation='softmax')
    g = tflearn.regression(g, optimizer='adam', loss='categorical_crossentropy',
                           learning_rate=0.001)

    vec = [x for x in map(word_idx.get, text) if x is not None]

    sequences = []
    next_words = []
    for i in range(0, len(vec) - maxlen, 3):
        sequences.append(vec[i: i + maxlen])
        next_words.append(vec[i + maxlen])

    X = np.zeros((len(sequences), maxlen, len(word_idx)), dtype=np.bool)
    Y = np.zeros((len(sequences), len(word_idx)), dtype=np.bool)
    for i, seq in enumerate(sequences):
        for t, idx in enumerate(seq):
            X[i, t, idx] = True
            Y[i, next_words[i]] = True

    m = tflearn.SequenceGenerator(g, dictionary=word_idx,
                                  seq_maxlen=maxlen,
                                  clip_gradients=5.0,
                                  checkpoint_path='model_dessert')
    # m.fit(X, Y, show_metric=True,
    #           batch_size=1, n_epoch=10)

    m.fit(X, Y, validation_set=0.1, batch_size=128,
          n_epoch=1, run_id='dessert')

    return m

def generate_seqs(m, testSet, targetSet, maxlen, temp):
    # seqs = 
    print "maxlen: ", maxlen
    print("-- TESTING...")
    print("-- Test with temperature of 1.2 --")
    for i in range(len(testSet)):
        seed = random.sample(range(len(testSet)), 1)[0]
        tgt = targetSet[seed]
        seed = random.sample(testSet[seed], maxlen)
        # print ("seed", seed)

        ytrue, ypred = [],[]
        
        # print "seed lenL ", len(seed)
        pred = m.generate(maxlen, temperature=temp, seq_seed=seed)
        # pred = list(set(pred))
        # print(i, pred)
        ytrue.append(tgt)
        ypred.append(pred)
        # print("-- Test with temperature of 1.0 --")
        # print(m.generate(30, temperature=1.0, seq_seed=seed).encode('utf-8'))
        # print("-- Test with temperature of 0.5 --")
        # print(m.generate(30, temperature=0.5, seq_seed=seed).encode('utf-8'))
    return ytrue, ypred

myInterface = interface.TestInterface()
initializers = [initi.Dessert()]
text, word_idx, maxlen, testSet, targetSet = initializers[0].initialize(interface)
currentProblem = myInterface.GetNextProblem()
scores = []
p = 1
xtrain, ytrain, xtest, ytest = None,None,None,None
# while not currentProblem is None:
#     # print("problem2: " + str(p))
#     p += 1

#     if currentProblem.problemType is "dessert":
#         init = initializers[0]
#         x,y = init.initXY(currentProblem)
#         if p % 4 != 0:
#           if xtrain is None:
#             xtrain = x
#             ytrain = y
#           else:
#             xtrain = np.vstack((xtrain, x))
#             ytrain = np.vstack((ytrain, y))
#             # print xtrain.shape
#         else:
#           if xtest is None:
#             xtest = x
#             ytest = y
#           else:
#             xtest = np.vstack((xtest, x))
#             ytest = np.vstack((ytest, y))
#             # print xtest.shape
#     currentProblem = myInterface.GetNextProblem()
print ("training")
# print np.asarray(xtrain)  
# model = train_rnn(xtrain, ytrain, init)
model = lstm(text, word_idx, maxlen)
print ("evaluating")
# print (len(testSet))
# exit()

y_true, y_pred = generate_seqs(model, testSet, targetSet, maxlen, temp=2.0)
print ("2.0 score:")
# 0.2
print allScore(y_true, y_pred)

y_true, y_pred = generate_seqs(model, testSet, targetSet, maxlen, temp=1.2)
print ("1.2 score:")
# 0.0
print allScore(y_true, y_pred)
y_true, y_pred = generate_seqs(model, testSet, targetSet, maxlen, temp=1.0)
print ("1.0 score:")
# 0.4
print allScore(y_true, y_pred)
y_true, y_pred = generate_seqs(model, testSet, targetSet, maxlen, temp=0.8)
print ("0.8 score:")
# 0.5
print allScore(y_true, y_pred)




# print ("evaluating")
# sctrain = model.evaluate(xtrain, ytrain, batch_size=1)
# print ("train score:")
# print (sctrain)
# sc = model.evaluate(xtest, ytest, batch_size=1)
# # model.predict(xtest)
# print ("score:")
# print (sc)

# [0.40594059523969594] LSTM

# ypred_test = model.predict_labels(xtest)
# sc = allScore(ytest, ypred_test)
# print ("score:")
# print (sc)
