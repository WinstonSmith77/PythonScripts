import itertools
import math
import time
import pprint
import statistics

def get_primes():
   
    yield 2
    primes_greater_2 = []

    for to_check in itertools.count(3, 2):
        max_to_check = math.floor(math.sqrt(to_check))
       
        is_prime = True
        for known_prime in  primes_greater_2:
            if known_prime > max_to_check:
                break
            if not to_check % known_prime:
                #print(to_check, to_check / known_prime, known_prime, primes_greater_2)
                is_prime = False
                break
        if is_prime:    
            primes_greater_2.append(to_check)
            yield to_check

def format(number):
    return f'{number:.3f}'

repeats = 10
length = 100_000

def benchmark(index):
   
    start = time.time()
    primes = list(itertools.islice(get_primes(), length))
    end = time.time()   

    diff = end - start

    print(index, format(diff))
    return primes, diff



results = list(map(benchmark, range(repeats)))

print(format(statistics.mean(map(lambda item : item[1], results))))

primes = results[0][0]

show = 15

pprint.pprint(primes[:show])
pprint.pprint(primes[-show:])
pprint.pprint(sum(primes))

#inspect.getsource(sum)