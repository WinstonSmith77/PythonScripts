import string
import random
import ubelt
import itertools
import time

valid_key_elements = list(string.ascii_letters) + list(string.digits)
#print(len(valid_key_elements))
randomGen = random.Random()
length = 4


def get_pw(valid_key_elements, l, r : random.Random) -> str:
    return ''.join(r.choices(valid_key_elements, None, k= l))

def hash_it(pw):
    return ubelt.hash_data(pw , hasher='md5')

pw_to_find = get_pw(valid_key_elements, length, randomGen)
hash_to_find = hash_it(pw_to_find)

print(pw_to_find, hash_to_find) 

# def get_pw(ke, random : random.Random, l) -> str:
#     result = ''
#     for _ in range(1, l):
#         result += random.
#     return result    

start = time.time()
for pw in map(lambda c : ''.join(c), itertools.permutations(valid_key_elements, length)):
    hash = hash_it(pw)
    
    if hash_to_find == hash:
        end = time.time()
        print(f'found {pw_to_find} {hash} {end - start}')
        break



