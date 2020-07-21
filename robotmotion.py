from random import seed
from random import random
seed(1)
print("hello")
width = 10
height = 10
grid = []
i = int(0)
x = 0
seed(1)


for i in range (width):
    value = random()
    if value > .6:
        grid.append("X")
    else:
        grid.append("_")
for i in range(width):
    print(grid)
