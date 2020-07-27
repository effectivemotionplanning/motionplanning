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

def generateArm1CurrentPosition(angle): ##defines the function for rotation
    mylist = np.zeros((500,500))
    for z in range(20):
        for c in range(arm1length):
            mylist[499 - (240+c)][z+250] =1

    angle = math.radians(angle) ##converts into radians
    matrix = np.zeros((500,500))  ##fill a 500x500 array with 0s
    for x in range(500): ##x coordinate
        for y in range(500): ##y coordinate
            if mylist[499-y][x] == 1:##this is the arm and this code does rotation and at every point that equals one, it rotates it and creates a new matrix
                center_x = 249
                center_y = 249
                xprime = (x - center_x) * math.cos(angle) - (y - center_y) * math.sin(angle) + center_x
                yprime = (x - center_x) * math.sin(angle) + (y - center_y) * math.cos(angle) + center_y
                xprime = round(xprime)
                yprime = round(yprime)
                matrix[499 - yprime][xprime] = 1
    return matrix  ##returns the matrix with the rotated arm

#prints total overlapped pixels of arm and matrix
def overlapcount(armgrid, matrix):
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
    arm2holderGrid = np.zeros((500,500))

    angle = math.radians(currentArm1Angle)
    center_x = 249
    center_y = 249
    x = 249
    y = 349
    xprime = (x - center_x) * math.cos(angle) - (y - center_y) * math.sin(angle) + center_x  #coordinates of edge pixel, end of arm 1, point of rotation for arm 2
    yprime = (x - center_x) * math.sin(angle) + (y - center_y) * math.cos(angle) + center_y
    xprime = round(xprime)
    yprime = round(yprime)
    startingx = xprime - 10
    for z in range(20):
        for c in range(arm2length):
            arm2holderGrid[499 - (c+yprime)][startingx+z] =1
    newRotatedArm2Grid = np.zeros((500,500))
    angle =math.radians(currentArm2Angle)
    for x in range(500): ##x coordinate
        for y in range(500): ##y coordinate
            if arm2holderGrid[499-y][x] == 1:##this is the arm and this code does rotation and at every point that equals one, it rotates it and creates a new matrix
                ox = xprime
                oy = yprime
                px = x
                py = y
                qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
                qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
                qx = round(qx)
                qy = round(qy)
                newRotatedArm2Grid[499-qy][qx] = 1


    return newRotatedArm2Grid
def generateObstacleGrid():
    m =   np.zeros((500,500))
    array = []
    for x in range(480):
        for y in range(480):
            num = random.random()
            if num<.00003:
                for r in range(20):
                    for c in range(20):
                        m[y+r][x+c] = 1
                        holderArray = []
                        holderArray.append(y+r)
                        holderArray.append(x+c)
                        array.append(holderArray)
    return m, array




def generatecspace(obstacleArray, obstacleCoordinateList):
    cspaceHolderGrid = np.zeros((500,500))
    for arm1degree in range(360):
        arm1array = generateArm1CurrentPosition(arm1degree)
        if isOverlap1(obstacleArray, obstacleCoordinateList, arm1array):
            continue
        print(arm1degree)
        for arm2degree in range(360):
            print(arm2degree)
            arm2array = generateArm2CurrentPosition(arm1degree,arm2degree)
            if not isOverlap(obstacleArray,obstacleCoordinateList,arm1array,arm2array):
                cspaceHolderGrid[arm2degree][arm1degree] = 0
            else:
                cspaceHolderGrid[arm2degree][arm1degree] = 1
    return cspaceHolderGrid


def isOverlap(array1, coordinateList, array2, array3):
    ##for x in range(500):
        ##for y in range(500):
        ##    if array1[y][x] == 1 and array2[y][x] == 1 or array1[y][x] == 1 and array3[y][x]:
            ##    return True
    ##return False
    for p in coordinateList:
        a = p[0]
        b = p[1]
        if array2[a][b] == 1 or array3[a][b] == 1:
            return True
    return False

def isOverlap1(array1, coordinateList, array2):
    ##for x in range(500):
        ##for y in range(500):
        ##    if array1[y][x] == 1 and array2[y][x] == 1 or array1[y][x] == 1 and array3[y][x]:
            ##    return True
    ##return False
    for p in coordinateList:
        a = p[0]
        b = p[1]
        if array2[a][b] == 1:
            return True
    return False




##initializing matrix with random 5 by 5 obstacles
obstacleMatrix, obstaclelist = generateObstacleGrid();
##generating a random angle for the arms initial and final configs
#each arm is 100 long
arm1length = 100
arm2length = 100
arm1Grid = np.zeros((500,500))
arm2Grid = np.zeros((500,500))


#bassically making arm 1 grid w arm at center . arm has a width of 20 and a length of 200

#MAKING ARM 1 GRID AND SHOWING IT, FIRST IMAGE U SEE IS THIS


#same thing, just for arm grid 2

#this is a work in progresss

#imshow generates image, show reveales that image

plt.imshow(obstacleMatrix)
#THIS IS THE 3RD IMAGE U SEE
plt.show()
#printing information
plt.imshow(generateArm1CurrentPosition(45))
plt.show()
plt.imshow(generateArm2CurrentPosition(45,180))
plt.show()
plt.imshow(generatecspace(obstacleMatrix, obstaclelist))
plt.show()
##begin conversion to cspace
cspace =  np.zeros((360,360))
##print (arm1Grid)
