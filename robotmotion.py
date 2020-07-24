import keras
from keras.layers import Input, Conv2D, Dropout
from keras.layers.normalization import BatchNormalization
from keras.models import Model, load_model
from keras.callbacks import EarlyStopping, ModelCheckpoint
import random
import numpy as np
import pandas

import matplotlib.pyplot as plt

##initializing matrix
m =   np.zeros((500,500))


for x in range(500):
    row =  np.zeros(500)
    for y in range(500):
        num = random.random()
        if num<=.01:
            for z in range(5):
                for a in range(5):
                    holder = m[x-z]
                    holder[y-a] = 1

        else:
            row[y] = 0
    m[x] = row
print( m)
##generating a random angle for the arm
randomangle1 = random.randint(0,360)
randomangle2 = random.randint(0,360)
arm1length = 200
arm2length = 200
arm1Grid = np.zeros((200,15))

##begin conversion to cspace
cspace =  np.zeros((360,360))
print (arm1Grid)
