import keras
from keras.layers import Input, Conv2D, Dropout
from keras.layers.normalization import BatchNormalization
from keras.models import Model, load_model
from keras.callbacks import EarlyStopping, ModelCheckpoint
import random
import numpy as np
import pandas

import matplotlib.pyplot as plt

##initializing matrix with random 5 by 5 obstacles
m =   np.zeros((500,500))
for x in range(495):
    for y in range(495):
        num = random.random()
        if num<.00003:
            for r in range(5):
                for c in range(5):
                    m[x+r][y+c] = 1

##generating a random angle for the arms initial and final configs
randomangle1 = random.randint(0,360)
randomangle2 = random.randint(0,360)
finalangle1 =int( random.random() * 360)
finalangle2 =int( random.random() * 360)
#each arm is 100 long
arm1length = 100
arm2length = 100
arm1Grid = np.zeros((500,500))
arm2Grid = np.zeros((500,500))


#bassically making arm 1 grid w arm at center . arm has a width of 20 and a length of 200

for z in range(20):
    for c in range(arm1length):
        arm1Grid[240+z][c+250] =1

#same thing, just for arm grid 2
for z in range(20):
    for c in range(arm2length):
        arm2Grid[240+z][c+250] =1


#this is a work in progresss
def rotate1counterclockwise(mylist, angle):
    for x in range(500):
        row =  np.zeros(500) #making a new row which will take place of old one in matrix
        for y in range(500):
            initialxposofpixel = arm1grid[x]
            b = 250 #rotation y coordinate
            a = 250 #rotation x coordinate
            thetarotation = angle



#prints total overlapped pixels of arm and matrix
def overlapcount(armgrid, matrix):
    overlapCount = 0
    for x in range (500):
        for y in range(500):
            if armgrid[x,y] == 1 and matrix[x,y] ==1:
                overlapCount+=1
    print(overlapCount)

#prints how many obstacles are there
def countobstacles(matrix):
    count = 0
    for x in range(500):
        for y in range(500):
            if matrix[x,y] ==1:
                count+=1
    print (count)

#printing information
print("total pixel collision between arm matrix 1 and  matrix and total  matrix obstacles")
overlapcount(arm1Grid, m)
countobstacles(m)
print("total pixel collision between arm matrix 2 and  matrix and total  matrix obstacles")
overlapcount(arm2Grid, m)
countobstacles(m)




##begin conversion to cspace
cspace =  np.zeros((360,360))
##print (arm1Grid)
