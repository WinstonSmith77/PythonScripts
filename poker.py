from enum import IntEnum
from random import choices
from itertools import groupby
from dataclasses import dataclass
from  pprint import pprint


class CardComponentBase(IntEnum):
    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class HandType(CardComponentBase):
    HIGH = 0,
    PAIR = 1
    THREE_OF_A_KIND = 2,
    FULL_HOUSE = 3,
    FOUR_OF_A_KIND = 4


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
    _subst_suits = {
        Suit.HEARTS: ['♥'],
        Suit.DIAMONDS: ['♦'],
        Suit.CLUBS: ['♣'],
        Suit.SPADES: ['♠']
        }
    rank: Rank
    rank: Rank
    rank: Rank
    suit: Suit

    def __str__(self):
        suit = self.suit
        suit = self._subst_suits.get(suit, [str(suit)])[0]

        return f'({suit} {self.rank})'

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
    groups_cards = [(k, list(g)) for k,g in groupby(hand_by_rank, key= get_rank)]
    len_groups = sorted([ len(g) for k , g in groups_cards], reverse=True)

    has_three = 3 in len_groups
    has_pair =  2 in len_groups
    has_four =  4 in len_groups

    if has_pair:
        result.add(HandType.PAIR)
    if has_three:
        result.add(HandType.THREE_OF_A_KIND)
        #result.add(HandType.PAIR)
    if has_three and has_pair:
        result.add(HandType.FULL_HOUSE)
    if has_four:
        result.add(HandType.FOUR_OF_A_KIND)

    return result    


for c in ALL_CARDS:
    pprint(c)

number = 5
length = 8

total = {type : 0 for type in  HandType}

for i in range(number):

    hand = get_hand(length)  
    hand_types = get_hand_types(hand)

    for type in total:
        total[type] += 1 if type in hand_types else 0

for type in total:
    total[type] = (total[type], total[type] / number)

total = sorted(total.items(), key= lambda x: x[1][1])    

pprint(total)