from enum import IntEnum
from itertools import product
from random import choices

class Suit(IntEnum):
    HEARTS = 0,
    DIAMONTS = 1,
    CLUBS = 2,
    SPADES = 3

    def __str__(self):
       return self.name    
    def __repr__(self):
      return str(self) 

class Rank(IntEnum):
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

    def __str__(self):
       return self.name   
    def __repr__(self):
       return str(self) 

suits = list(Suit)
ranks = list(Rank)



all = list(product(ranks, suits))
hand =  sorted(choices(all, k = 5), key = lambda x : x[0].value, reverse=True)

for card in hand:
      print(card)



