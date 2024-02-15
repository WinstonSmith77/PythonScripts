import random
import math

total = 0
in_circle = 0 

random = random.Random()

while True:
    total += 1
    x,y = random.random(), random.random()
    if x * x + y * y < 1:
        in_circle += 1

    pi = 4 * in_circle / total    

    if total % 1_000_000 == 0:

        print(round(pi, 7), abs(pi - math.pi))       

