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

def get_hand_types(hand  : list):
    result = {HandType.HIGH}

    get_rank = lambda x : x.rank

    hand_by_rank =  sorted(hand, key= get_rank)
    print(hand_by_rank)
    groups = [(k, list(g)) for k,g in groupby(hand_by_rank, key= get_rank)]

    for rank, cards in groups:
        if len(cards) >= 2:
            result.add(HandType.PAIR)
        if len(cards) >= 3:
            result.add(HandType.THREE_OF_A_KIND)


    print(groups)    

    return result


hand = get_hand(5)
hand_types = get_hand_types(hand)

print(hand)
print(hand_types)
