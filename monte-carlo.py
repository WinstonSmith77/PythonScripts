import random
import math

total = 0
in_circle = 0 

random = random.Random(86621)
diff, old_diff = 1, 1
diff_to_break = 1/5000_000_000

while diff > diff_to_break:
    total += 1
    x,y = random.random(), random.random()
    if x * x + y * y < 1:
        in_circle += 1

    pi = 4 * in_circle / total    
    diff = abs(pi - math.pi)

    new_min_diff = diff < old_diff 

    if new_min_diff:
          old_diff = diff    

    if new_min_diff  or total % 1_000_000==0:
        print(round(pi, 7), diff, total)
         
