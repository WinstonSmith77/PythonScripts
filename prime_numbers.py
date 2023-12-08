import itertools
import math
import time
import pprint

def get_primes():
   
    yield 1
    yield 2
    primes_greater_2 =[]

    for to_check in itertools.count(3, 2):
        max_to_check = math.floor(math.sqrt(to_check))
       
        for known_prime in range(3, max_to_check, 2):
            if to_check % known_prime == 0:
                break
        else:    
            primes_greater_2.append(to_check)
            yield to_check
       


start = time.time()

primes = list(itertools.islice(get_primes(), 100_000))

end = time.time()    

print(end - start)

pprint.pprint(primes[:20])