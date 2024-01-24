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

result = [i for i in collatz(10000 ** 340 -1)]

print(len(result))
        
