import matplotlib.pyplot as plt

def collatz(start):
    n = start
    while True:
        yield n
        if n == 1:
            break
        else:
            half, remainder = divmod(n, 2)
            if remainder == 0:
                n = half
            else:
                n = 3 * n + 1

y = [i for i in collatz(10000 ** 5 -1)]
x = range(0, len(y))

plt.figure(num = 0, dpi= 120)

plt.plot(x,y)
plt.yscale('log')
plt.show()

        
