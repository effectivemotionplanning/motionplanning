import keras
from keras.layers import Input, Conv2D, Dropout
from keras.layers.normalization import BatchNormalization
from keras.models import Model, load_model
from keras.callbacks import EarlyStopping, ModelCheckpoint
import random
import numpy as np
import pandas
import math

import matplotlib.pyplot as plt

def rotate1counterclockwise(mylist, angle):
    angle = math.radians(angle)
    matrix = np.zeros((500,500))
    for x in range(500):
        for y in range(500):
            if mylist[x][y] == 1:
                center_x = 249
                center_y = 249
                xprime = (x - center_x) * math.cos(angle) - (y - center_y) * math.sin(angle) + center_x
                yprime = (x - center_x) * math.sin(angle) + (y - center_y) * math.cos(angle) + center_y
                xprime = round(xprime)
                yprime = round(yprime)
                matrix[xprime][yprime] = 1
    return matrix

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
#generates array with arm2 position based on Arm1 configuration
def generateArm2CurrentPosition(currentArm1Angle,currentArm2Angle):
    arm2holderGrid = np.zeros((500,500))
    angle = currentArm1Angle
    center_x = 249
    center_y = 249
    x = 249
    y = 349
    xprime = (x - center_x) * math.cos(angle) - (y - center_y) * math.sin(angle) + center_x
    yprime = (x - center_x) * math.sin(angle) + (y - center_y) * math.cos(angle) + center_y
    xprime = round(xprime)
    yprime = round(yprime)
    for z in range(20):
        for c in range(arm2length):
            arm2holderGrid[c+250][240+z] =1
    plt.imshow(arm2holderGrid)
    plt.gca().invert_yaxis()
    plt.show()
    for x in range(500):
        for y in range(500):
            if arm2holderGrid[x][y] == 1:
                angle = currentArm2Angle
                center_x = xprime
                center_y = yprime
                xprime = (x - center_x) * math.cos(angle) - (y - center_y) * math.sin(angle) + center_x
                yprime = (x - center_x) * math.sin(angle) + (y - center_y) * math.cos(angle) + center_y
                xprime = round(xprime)
                yprime = round(yprime)
                arm2holderGrid[yprime][xprime] = 1
    plt.imshow(arm2holderGrid)
    plt.gca().invert_yaxis()
    plt.show()

    return arm2holderGrid
def generateObstacleGrid():
    m =   np.zeros((500,500))
    for x in range(495):
        for y in range(495):
            num = random.random()
            if num<.00003:
                for r in range(20):
                    for c in range(20):
                        if not(x+r > 499) or not(y+c > 499) or not(y+c < 0) or not (x+r < 0) :
                            m[x+r][y+c] = 1
    return m

##initializing matrix with random 5 by 5 obstacles
obstacleMatrix = generateObstacleGrid();
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
        #arm1Grid[240+z][c+250] =1
        arm1Grid[100][400] = 1
plt.imshow(arm1Grid)
#plt.gca().invert_yaxis()
plt.show()

#same thing, just for arm grid 2
for z in range(20):
    for c in range(arm2length):
        arm2Grid[240+z][c+250] =1


#this is a work in progresss




#printing information
print("total pixel collision between arm matrix 1 and  matrix and total  matrix obstacles")
overlapcount(arm1Grid, obstacleMatrix)
countobstacles(obstacleMatrix)
print("total pixel collision between arm matrix 2 and  matrix and total  matrix obstacles")
overlapcount(arm2Grid, obstacleMatrix)
countobstacles(obstacleMatrix)
generateArm2CurrentPosition(90,45)
#show obstacle map
plt.imshow(obstacleMatrix)
#inverts y axis to look regular
plt.gca().invert_yaxis()
plt.show()
#show original arm configuration
plt.imshow(arm1Grid)
plt.gca().invert_yaxis()
plt.show()
#show roated arm config

##begin conversion to cspace
cspace =  np.zeros((360,360))
##print (arm1Grid)
