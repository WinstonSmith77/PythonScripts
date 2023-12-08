import itertools
import math
import time
import pprint

def get_primes():
   
    yield 1
    yield 2
    primes_greater_2 =[]

    to_check = 3
    while True:
        max_to_check = math.floor(math.sqrt(to_check))
        is_prime = True
        for known_prime in primes_greater_2:
            if known_prime > max_to_check:
                break
            if to_check % known_prime == 0:
                is_prime = False
                break
        if is_prime:    
            primes_greater_2.append(to_check)
            yield to_check

        to_check += 2    

length = 100_000
start = time.time()

primes = list(itertools.islice(get_primes(), length))

end = time.time()    

print(end - start)

pprint.pprint(primes[:10])
pprint.pprint(primes[-10:])
pprint.pprint(sum(primes))
