from random import seed
import random
from numpy import *
##initializing matrix
m = array([[0, 0,0,0,0,0,0,0,0,0],[0, 0,0,0,0,0,0,0,0,0],
		   [0, 0,0,0,0,0,0,0,0,0],[0, 0,0,0,0,0,0,0,0,0],
		   [0, 0,0,0,0,0,0,0,0,0],[0, 0,0,0,0,0,0,0,0,0],
		   [0, 0,0,0,0,0,0,0,0,0], [0, 0,0,0,0,0,0,0,0,0], [0, 0,0,0,0,0,0,0,0,0], [0, 0,0,0,0,0,0,0,0,0]])

row = 10
col =10
current = 0 ## represents how many obstacles (represented by the number 1) currently  exist, a max of 35 can exist
created = 0 ## bassically a boolean that checks whether or not the the arm's starting position has been already added to the matrix, the arm is represented by the number 2
#this for loop adds all the obstacles, each block has a 60% chance of being an obstacle, but a max of 35 obstacles can exist
#keep playing around w obstacle density for optimal density 
for i in range (row):
    for x in range (col):
        num = random.random()
        if num>.6 and current<35:
            m[i][x] =1
            current+=1
## adds the arm's initial position as the number 2
for i in range (1, 9):
    for x in range (1, col-1):
        if (m[i-1][x] ==0) and (m[i][x] == 0) and (m[i+1][x] == 0):
            if m[i][x-1] == 0  and m[i][x] == 0 and m[i][x+1]==0:
                if created == 0:
                    m[i][x] = 2
                    m[i][x+1]=2
                    m[i+1][x] = 2
                    created = 1
finishpos = 0 ##bassically a boolean that represents if finish position has been created already, finish pos of arm represented by 3
for i in range (1, 9):
    for x in range (1, col-1):
        if (m[i-1][x] ==0) and (m[i][x] == 0) and (m[i+1][x] == 0):
            if m[i][x-1] == 0  and m[i][x] == 0 and m[i][x+1]==0:
                if finishpos == 0:
                    m[i][x] = 3
                    m[i][x+1]=3
                    m[i+1][x] = 3
                    finishpos =1

print(m)
