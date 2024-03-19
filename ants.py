#https://www.codewars.com/kata/65ee024f99785f0906e65bee/train/python

from array import array

def to_str(counters):
    result = ''

    for c in counters:
        result += str(c) + ' '    

    return result.strip()

def bump_counter(ants : str):
    ants =  array('i', map(lambda x: int(x), ants.encode()))
    L = ord('L')
    R = ord('R')
    
    number_of_ants = len(ants)
    counters = array('i' , [0] * number_of_ants)
    any_bump = True

    while any_bump:
        any_bump = False
        for i, l in enumerate(ants):
            if i == number_of_ants - 1:
                break 
            j = i + 1
            if l == R and  ants[j] == L:
                counters[i] += 1
                counters[j] += 1
                ants[i] = L
                ants[j] = R
                any_bump = True
 
    return to_str(counters)

print(bump_counter('RRLRRRLL'))





