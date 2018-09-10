import rnn.initializers as initi
# import tflearn as tf
import keras
from keras.optimizers import RMSprop
from keras.models import Sequential
from keras.layers import Activation, SimpleRNN, Reshape, Dense, LSTM

import interface
import random
import numpy as np


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
    inputIngredients = set(questionData[1])
    targetIngredients = set(target[1])
    ingredientDifferences = len(inputIngredients.intersection(targetIngredients))
    ingredientsScore = 0.5*(float(ingredientDifferences)/float(len(targetIngredients)))
    # total += titleScore+ingredientsScore
    total += ingredientsScore
  return float(total)/len(y_pred)

def train_rnn(x_train, y_train, init):

    batch_size = 32
    num_classes = 10
    epochs = 200
    hidden_units = 100
    learning_rate = 1e-6
    clip_norm = 1.0

    print('Evaluate IRNN...')
    model = Sequential()
    # print x_train.shape
    model.add(SimpleRNN(hidden_units,
                        activation='relu',
                        input_shape=x_train.shape[1:],
                        return_sequences=True))
    model.add(Dense(num_classes))
    model.add(Activation('softmax'))
    rmsprop = RMSprop(lr=learning_rate)
    model.compile(loss='categorical_crossentropy',
                  optimizer=rmsprop,
                  # metrics=allScore)
                  metrics=['acc'])

    # # define LSTM
    # # model = Sequential()
    # # print y_train.shape
    # model = Sequential()
    # # model.add(Dense(32, input_shape=x_train.shape[1:]))
    # model.add(LSTM(hidden_units, input_dim=x_train.shape[1:][0], return_sequences=True))
    # model.add(TimeDistributed(Dense(num_classes, activation='sigmoid')))
    # model.compile(optimizer='rmsprop',
    #               loss='categorical_crossentropy',
    #               metrics=['acc'])


    model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              verbose=1)
    return model


myInterface = interface.TestInterface()
initializers = [initi.Dessert()]
initializers[0].initialize(interface)
currentProblem = myInterface.GetNextProblem()
scores = []
p = 1
xtrain, ytrain, xtest, ytest = None,None,None,None
while not currentProblem is None:
    print("problem2: " + str(p))
    p += 1

    if currentProblem.problemType is "dessert":
        init = initializers[0]
        x,y = init.initXY(currentProblem)
        if p <= 300:
          if xtrain is None:
            xtrain = x
            ytrain = y
          else:
            xtrain = np.vstack((xtrain, x))
            ytrain = np.vstack((ytrain, y))
            # print xtrain.shape
        else:
          if xtest is None:
            xtest = x
            ytest = y
          else:
            xtest = np.vstack((xtest, x))
            ytest = np.vstack((ytest, y))
            # print xtest.shape
    currentProblem = myInterface.GetNextProblem()
print ("training")
# print np.asarray(xtrain)  
model = train_rnn(xtrain, ytrain, init)
print ("evaluating")
sc = model.evaluate(xtest, ytest)

print ("score:")
print (sc)
