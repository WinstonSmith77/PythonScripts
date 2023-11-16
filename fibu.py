import itertools

def fibu_yield():
    first, second = 1,1 
    while True:
        yield first 
        first, second = second, first + second 


class Fibu:
    def __iter__(self):
        self.first = 1
        self.second = 1
        return self

    def __next__(self):
        to_return = self.first
        self.first, self.second = self.second, self.first + self.second 
        return to_return  
       

a = fibu_yield()
l = list(itertools.islice(a, 5000))


a2 = Fibu()
l2 = list(itertools.islice(a2, 5000))


print(dir(a))
for i, n in enumerate(itertools.islice(l, 100)):
    print(i, n)
    
print(dir(a2))   
for i, n in enumerate(itertools.islice(l2, 100)):
    print(i, n)    
