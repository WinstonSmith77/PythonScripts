import string
import random
import ubelt
import itertools
import time

valid_key_elements = string.digits + string.ascii_letters
#valid_key_elements = list(string.digits) + list(string.ascii_letters)
#print((valid_key_elements))
randomGen = random.Random()
length = 4


def get_pw(valid_key_elements, l, r : random.Random) -> str:
    return tuple(r.choices(valid_key_elements, None, k= l))

def hash_it(pw):
    return ubelt.hash_data(pw , hasher='md5')

pw_to_find = get_pw(valid_key_elements, length, randomGen)
#hash_to_find = hash_it(pw_to_find)

print(pw_to_find) 

# def get_pw(ke, random : random.Random, l) -> str:
#     result = ''
#     for _ in range(1, l):
#         result += random.
#     return result    

start = time.time()
for pw in itertools.product(*itertools.repeat(valid_key_elements, length)):
   
    #hash = hash_it(pw)
    if pw == pw_to_find:
        end = time.time()
        print(f'found {pw} {end - start}')
        break



