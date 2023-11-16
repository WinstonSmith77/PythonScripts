import itertools

def fibu():
    first, second = 1,1 
    yield first 
    while True:
        yield second 
        first, second = second, first + second 
       


a = fibu()

l = list(itertools.islice(a, 5000))

print(dir(a))
count = 0
for i, n in enumerate(itertools.islice(l, 10)):
    print(i, n)
    
