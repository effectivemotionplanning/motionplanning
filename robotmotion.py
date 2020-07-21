from random import seed
import random
from numpy import *
##initializing matrix
m = array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

row = 20
col =20

created = 0 ## bassically a boolean that checks whether or not the the arm's starting position has been already added to the matrix, the arm is represented by the number 2
## adds the start position,, center (cant move this position/not a joint), is represnted by a 9, rest is represented by a 2
for i in range (4, (row-4)):
    for x in range (4, col-4):
        num = random.random()
        if  m[i-4][x] ==0 and (m[i-3][x] ==0)  and(m[i-2][x] ==0) and (m[i-1][x] ==0) and (m[i][x] == 0) and (m[i+1][x] == 0) and (m[i+2][x] ==0) and (m[i+3][x] ==0) and m[i+4][x] ==0:
            if  m[i][x-4] == 0  and m[i][x-3] == 0 and m[i][x-2] == 0 and  m[i][x-1] == 0  and m[i][x] == 0 and m[i][x+1]==0 and m[i][x+2] == 0 and  m[i][x+3] == 0 and m[i][x+4] == 0 :
                if num <.1 and created == 0:
                    m[i-4][x] = 2
                    m[i-3][x] = 2
                    m[i-2][x] = 2
                    m[i-1][x] = 2
                    m[i][x] = 9
                    m[i][x+1]=2
                    m[i][x+2]=2
                    m[i][x+3]=2
                    m[i][x+4]=2
                    created = 1
#this for loop adds all the obstacles, each block has a 60% chance of being an obstacle
#keep playing around w obstacle density for optimal density
for i in range (row):
    for x in range (col):
        num = random.random()
        if num>.6 and m[i][x] ==0:
            m[i][x] =1

print(m)
