from enum import IntEnum
from random import choices
from itertools import groupby
from dataclasses import dataclass


class CardComponentBase(IntEnum):
    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class HandType(CardComponentBase):
    HIGH = 0,
    PAIR = 1
    THREE_OF_A_KIND = 2
   


class Suit(CardComponentBase):
    HEARTS = 0,
    DIAMONDS = 1,
    CLUBS = 2,
    SPADES = 3


class Rank(CardComponentBase):
    TWO = 0,
    THREE = 1,
    FOUR = 2,
    FIVE = 3,
    SIX = 4,
    SEVEN = 5,
    EIGHT = 6,
    NINE = 7,
    TEN = 8,
    JACK = 9,
    QUEEN = 10,
    KING = 11,
    ACE = 12


@dataclass(frozen=True, order=True)
class Card:
    rank: Rank
    suit: Suit

    def __str__(self):
        return f'({self.rank} {self.suit})'

    def __repr__(self):
        return str(self)

SUITS= list(Suit)
RANKS = list(Rank)

ALL_CARDS = [Card(rank=rank, suit=suit) for rank in RANKS for suit in SUITS]


def get_hand(length):
    result = choices(ALL_CARDS, k = length)
    return result

def get_hand_types(hand):
    result = {HandType.HIGH}

    def get_rank(x):
        return x.rank

    hand_by_rank =  sorted(hand, key= get_rank)
    groups = [(k, list(g)) for k,g in groupby(hand_by_rank, key= get_rank)]

    has_pair = any(map(lambda x : len(x[1]) == 2, groups))
    has_three = any(map(lambda x : len(x[1]) == 3, groups))
                                           
    if has_pair:
        result.add(HandType.PAIR)
    if has_three:
        result.add(HandType.THREE_OF_A_KIND)

    return result    

   

number = 100_000
length = 5

has_pair = 0
has_three = 0

for i in range(number):

    hand = get_hand(length)  
    hand_types = get_hand_types(hand)

    if HandType.PAIR in hand_types:
        has_pair += 1

    if HandType.THREE_OF_A_KIND in hand_types:
        has_three += 1

print(has_pair / number)
print(has_three / number)