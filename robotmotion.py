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
            mylist[499 - (240+c)][z+250] = 1
    angle = math.radians(angle) ##converts into radians
    matrix = np.zeros((500,500))  ##fill a 500x500 array with 0s
    for x in range(500): ##x coordinate
        for y in range(500): ##y coordinate
            if mylist[499-y][x] == 1:##this is the arm and this code does rotation and at every point that equals one (which is the arm 1), it rotates it and creates a new matrix
                center_x = 249 ##rotation around the center
                center_y = 249
                xprime = (x - center_x) * math.cos(angle) - (y - center_y) * math.sin(angle) + center_x
                yprime = (x - center_x) * math.sin(angle) + (y - center_y) * math.cos(angle) + center_y
                xprime = round(xprime)
                yprime = round(yprime)
                matrix[499 - yprime][xprime] = 1 ##marks the rotated arm
    return matrix  ##returns the matrix with the rotated arm

def doesarm1overlap(angle, obstacelist): ##defines the function for rotation
    ##mylist = np.zeros((500,500))
    array = []
    for z in range(20):
        for c in range(arm1length):
            ##mylist[499 - (240+c)][z+250] = 1
            holderArray = [] ## code should be adding coordinates of arm 2 (prior rotation)into the 2d array named array
            holderArray.append(499 - (240+c))
            holderArray.append(z+250)
            array.append(holderArray)
    angle = math.radians(angle) ##converts into radians
    ##matrix = np.zeros((500,500))  ##fill a 500x500 array with 0s
    ##for x in range(500): ##x coordinate
        ##for y in range(500): ##y coordinate
            ##if mylist[499-y][x] == 1:##this is the arm and this code does rotation and at every point that equals one (which is the arm 1), it rotates it and creates a new matrix
    for f in array:
                #x = f[0]
                #y = f[1]
                #center_x = 249 ##rotation around the center
                #center_y = 249
                #xprime = (x - center_x) * math.cos(angle) - (y - center_y) * math.sin(angle) + center_x
                #yprime = (x - center_x) * math.sin(angle) + (y - center_y) * math.cos(angle) + center_y
                #xprime = round(xprime)
                #yprime = round(yprime)


                    ox = 249
                    oy = 249
                    #anotherholderarray = []
                    #anotherholderarray.append(array[f])
                    px = f[0]
                    py = f[1]
                    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
                    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
                    qx = round(qx)
                    qy = round(qy)
                    ##matrix[499 - yprime][xprime] = 1 ##marks the rotated arm
                    ##for z in range(20):
                    ##for c in range(arm1length):
                    ## holderArray = [] ## code should be adding coordinates of arm 1 (after rotation) into the 2d array named array
                    ##holderArray.append(499-(c+yprime))
                    ##holderArray.append(xprime+z)
                    ##array.append(holderArray)
                    for r in obstaclelist: ##checks the obstacles during generation to speed it up
                        if r[0] == qy and r[1] == qx: ##checks if row 1 and 2 in the obstaclelist are the same as the rotated arm
                            return True
                    return False

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
    center_x = 249 ##rotation around the center to see where the first arm is
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
            arm2holderGrid[499 - (c+yprime)][startingx+z] = 1 ##marks the unrotated second arm
    newRotatedArm2Grid = np.zeros((500,500))
    angle =math.radians(currentArm2Angle)
    for x in range(500): ##x coordinate
        for y in range(500): ##y coordinate
            if arm2holderGrid[499-y][x] == 1:##begins the rotation for the second arm around the point for the first arm
                ox = xprime
                oy = yprime
                px = x
                py = y
                qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
                qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
                qx = round(qx)
                qy = round(qy)
                newRotatedArm2Grid[499-qy][qx] = 1 ##marks the rotated second arm
    return newRotatedArm2Grid


#so bassically, we were able to reduce cspace generation from like 9 hrs to 10 min per cspace by doing following changes:
#first we changed it so that the cspace generation method  doesn't have to call arm 2 generation and isoverlap, because each iterated thru 500 by 500x500
# this made it so that we only had to go thru 500 by 500 once.
#then we also made it so that we only had to iterate thru arm coordinates (20 by 100) and the obstacle coordinates specifically, not the whole 500 by 500 matrixes
def doesarm2overlap(currentArm1Angle,currentArm2Angle,obstaclelist): ##this method is basically the generatearm2 with a built in checker to determine collisions with obstacles during generation
    #arm2holderGrid = np.zeros((500,500))
    array = []
    #finalarray = []
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
            #arm2holderGrid[499 - (c+yprime)][startingx+z] =1
            holderArray = [] ## code should be adding coordinates of arm 2 (prior rotation)into the 2d array named array
            holderArray.append(499-(c+yprime))
            holderArray.append(startingx+z)
            array.append(holderArray)
    #newRotatedArm2Grid = np.zeros((500,500))
    angle =math.radians(currentArm2Angle)
    for f in array:
        ox = xprime
        oy = yprime
        #anotherholderarray = []
        #anotherholderarray.append(array[f])
        px = f[0]
        py = f[1]
        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        qx = round(qx)
        qy = round(qy)
        for r in obstaclelist: ##checks the obstacles during generation to speed it up
            if r[0] == qy and r[1] == qx: ##checks if row 1 and 2 in the obstaclelist are the same as the rotated arm
                return True
        return False
        #xxholderarray = []
        #xxholderarray.append(qx)
        #xxholderarray.append(qy)
        #finalarray.append(xxholderarray)

count = 0
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
                        array.append(holderArray) ##saving the coordinates of the obstacles
    return m, array


def generatecspace(obstacleArray, obstacleCoordinateList):
    cspaceHolderGrid = np.zeros((360,360))
    for arm1degree in range(360):
        print(arm1degree)
        if doesarm1overlap(arm1degree, obstacleCoordinateList):
            #cspaceHolderGrid[359-arm2degree] = 1
            print("test")
            continue
        for arm2degree in range(360):
            if doesarm2overlap(arm1degree, arm2degree, obstaclelist):
                cspaceHolderGrid[359 - arm2degree][arm1degree] = 1
            else:
                cspaceHolderGrid[359 - arm2degree][arm1degree] = 0
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
        if array2[a][b] == 1 or array3[a][b] == 1: ##2d array
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
        if array2[a][b] == 1: ##2d array
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
plt.imshow(generateArm1CurrentPosition(10))
plt.show()
plt.imshow(generateArm2CurrentPosition(10,10))
plt.show()
plt.imshow(generatecspace(obstacleMatrix, obstaclelist))
plt.show()
##begin conversion to cspace
cspace =  np.zeros((360,360))
##print (arm1Grid)
