from enum import IntEnum
from itertools import product
from random import choices
from dataclasses import dataclass

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

@dataclass(frozen = True, order=True)
class Card:
   rank : Rank
   suit : Suit


all = [Card(rank=rank, suit=suit)  for rank in ranks for suit in suits]
hand =  sorted(choices(all, k = 5), reverse=True)

print(hand)



