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
m =  []
for x in range(500):
    m.append(np.zeros(500))

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
print(m)

##generating a random angle for the arm
import random
randomangle = random.randint(0,360)

