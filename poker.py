from enum import Enum
from itertools import product

class Suit(Enum):
    HEARTS = 0,
    DIAMONTS = 1,
    CLUBS = 2,
    SPADES = 3

class Rank(Enum):
    TWOS = 0,    
    THREES = 1,
    FOURS = 2,
    FIVES = 3,
    SIXES = 4,
    SEVENS = 5,
    EIGHTS = 6,
    NINE = 7,
    TENS = 8,
    JACKS = 9,
    QUEENS = 10,
    KINGS = 11,
    ACES = 12

suits = list(map(lambda x: x.name, Suit))
ranks = list(map(lambda x: x.name, Rank))

all = list(product(ranks, suits))


print(all, len(all))
