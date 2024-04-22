class Fibonacci_below:
    def __init__(self, max):
        self.max = max

    def __iter__(self):
        self.first = self.second = 1
        return self

    def __next__(self):
        to_return = self.first
        if to_return >= self.max:
            raise StopIteration
        self.first, self.second = self.second, self.first + self.second 
        return to_return  



x = Fibonacci_below(5)

for i in iter(x):
    print(i)
    break

print('')

for i in iter(x):
    print(i)    