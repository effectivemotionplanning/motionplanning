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

def rotate1counterclockwise(mylist, angle): ##defines the function for rotation
    angle = math.radians(angle) ##converts into radians
    matrix = np.zeros((500,500))  ##fill a 500x500 array with 0s
    for x in range(500): ##x coordinate
        for y in range(500): ##y coordinate
            if mylist[x][y] == 1:##this is the arm and this code does rotation and at every point that equals one, it rotates it and creates a new matrix
                center_x = 249
                center_y = 249
                xprime = (x - center_x) * math.cos(angle) - (y - center_y) * math.sin(angle) + center_x
                yprime = (x - center_x) * math.sin(angle) + (y - center_y) * math.cos(angle) + center_y
                xprime = round(xprime)
                yprime = round(yprime)
                matrix[xprime][yprime] = 1
    return matrix  ##returns the matrix with the rotated arm

#prints total overlapped pixels of arm and matrix
def overlapcount(armgrid, matrix): ##defines the function
    overlapCount = 0
    for x in range (500):
        for y in range(500):
            if armgrid[x,y] == 1 and matrix[x,y] ==1: ##if x and y corodiantes point to a place that is 1, then it will increase the overlap count to determine the number of collisions
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
    arm2holderGrid = np.zeros((500,500))                                                                            what is the arm2holderGrid
    angle = currentArm1Angle
    center_x = 249                                                                                                  what does all of this begin to do
    center_y = 249
    x = 249
    y = 349
    xprime = (x - center_x) * math.cos(angle) - (y - center_y) * math.sin(angle) + center_x  #coordinates of edge pixel, end of arm 1, point of rotation for arm 2
    yprime = (x - center_x) * math.sin(angle) + (y - center_y) * math.cos(angle) + center_y
    xprime = round(xprime)
    yprime = round(yprime)
    for z in range(20):
        for c in range(arm2length):
            arm2holderGrid[c+350][240+z] =1
    plt.imshow(arm2holderGrid)
    print("4th image is  arm 2 ")
    #plt.gca().invert_yaxis()
    plt.show()
    for r in range(500):
        for l in range(500):
            if arm2holderGrid[r][l] == 1:
                angle = currentArm2Angle
                center_x = xprime
                center_y = yprime

                xprime = (x - center_x) * math.cos(angle) - (y - center_y) * math.sin(angle) + center_x
                yprime = (x - center_x) * math.sin(angle) + (y - center_y) * math.cos(angle) + center_y
                xprime = round(xprime)
                yprime = round(yprime)

                arm2holderGrid[yprime][xprime] = 1#switched both
    plt.imshow(arm2holderGrid)
    #plt.gca().invert_yaxis()
    print("5th image and arm 2 after arm 1 and 2 rotation")
    plt.show()

    return arm2holderGrid
def generateObstacleGrid():
    m =   np.zeros((500,500))
    for x in range(480):                                                                                                why does the obstacle grid have a range of 480? is it cuz its 5x5
        for y in range(480):
            num = random.random()
            if num<.00003:                                                                                              why less than .00003
                for r in range(20):                                                                                     why range of 20
                    for c in range(20):                                                                                 why range of 20
                        m[y+r][x+c] = 1                                                                                 what does this mean?
    return m                                                                                                            why return m

##initializing matrix with random 5 by 5 obstacles
obstacleMatrix = generateObstacleGrid();
##generating a random angle for the arms initial and final configs
randomangle1 = random.randint(0,360)
randomangle2 = random.randint(0,360)
finalangle1 =int( random.random() * 360)                                                                                what is this doing
finalangle2 =int( random.random() * 360)
#each arm is 100 long
arm1length = 100
arm2length = 100
arm1Grid = np.zeros((500,500))
arm2Grid = np.zeros((500,500))


#bassically making arm 1 grid w arm at center . arm has a width of 20 and a length of 200

#MAKING ARM 1 GRID AND SHOWING IT, FIRST IMAGE U SEE IS THIS
for z in range(20):                                                                                                        what is this doing
    for c in range(arm1length):
        arm1Grid[240+c][z+250] =1
        arm1Grid[100][400] = 1
plt.imshow(arm1Grid)
#plt.gca().invert_yaxis()
print("arm 1 grid and image 1 ")
plt.show()

#same thing, just for arm grid 2
print("arm 2 grid and 2nd image")
# THIS IS THE 2ND IMAGE U SEE
for z in range(20):
    for c in range(arm2length):
        arm2Grid[340+c][z+250] =1
plt.imshow(arm2Grid)
#plt.gca().invert_yaxis()
plt.show()

#this is a work in progresss

#imshow generates image, show reveales that image

print("3rd image and the obstacle matrix grid")
plt.imshow(obstacleMatrix)
#THIS IS THE 3RD IMAGE U SEE
plt.show()
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
#plt.gca().invert_yaxis()
print("6th image and obstacle matrix again")
plt.show()
#show original arm configuration
plt.imshow(arm1Grid)
#plt.gca().invert_yaxis()
print("7th image which is arm 1 grid")
plt.show()
#show roated arm config
print("arm 1 rotation test")

plt.imshow(rotate1counterclockwise(arm1Grid, 69))
plt.show()

##begin conversion to cspace
cspace =  np.zeros((360,360))
##print (arm1Grid)
