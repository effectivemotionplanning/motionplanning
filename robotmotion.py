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
#so bassically, we were able to reduce from like 9 hrs to 10 min per cspace by doing following changes:
#first we changed it so that the cspace generation method  doesn't have to call arm 2 generation and isoverlap, because each iterated thru  500x500
# this made it so that we only had to go thru 500 by 500 once.
    #originally, we generated arm 2's current position by iterating thru a 500 by 500 matrix. then , to check overlap, we iterated thru 500 by 500 matrix again to see if there were collisisons between arm matrix and obstacle matrix
    #we changed this so that while generating the 500 by 500 arm matrix itself, we check thru the obstacle list, that way we do not have to iterate thru a 500 by 500 matrix again
    #this wasnt neccessary for arm 1, sicne although we iterated 500 by 500 in arm 1 generation, when checking for overlap, we iterated thru obstacle coordinate list, and used the coordinates from there to access values in arm 1's 500 by 500 grid and seeing if those values also equalled 1, so we actually were only iterating thru 500 by 500 once, and thus there was not much to decrease
#then we also made it so that we only had to iterate thru arm coordinates (20 by 100) and the obstacle coordinates specifically, not the whole 500 by 500 matrixes

def doesarm2overlap(currentArm1Angle,currentArm2Angle, obstaclelist):
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
            holderArray = []
            holderArray.append(c+yprime)
            holderArray.append(startingx+z)
            array.append(holderArray)

            ## code above should be adding coordinates of arm 2 (prior rotation)into the 2d array named array
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
        for r in obstaclelist:
            if r[0] ==qy and r[1] ==qx:
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
                        m[499 - (y+r)][x+c] = 1
                        holderArray = []
                        holderArray.append(y+r)
                        holderArray.append(x+c)
                        array.append(holderArray)
    return m, array




def generatecspace(obstacleArray, obstacleCoordinateList):
    cspaceHolderGrid = np.zeros((360,360))
    for arm1degree in range(360):
        arm1array = generateArm1CurrentPosition(arm1degree)
        if isOverlap1(obstacleArray, obstacleCoordinateList, arm1array):
            continue
        for arm2degree in range(360):
            print(arm2degree)
            if doesarm2overlap(arm1degree, arm2degree, obstaclelist):
                cspaceHolderGrid[359 - arm2degree][arm1degree] = 1
            else:
                cspaceHolderGrid[359 - arm2degree][arm1degree] = 0
    print(cspaceHolderGrid)
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
        if array2[499-a][b] == 1:
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
