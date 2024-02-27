from enum import IntEnum
from random import choices
from dataclasses import dataclass


class Suit(IntEnum):
    HEARTS = 0,
    DIAMONDS = 1,
    CLUBS = 2,
    SPADES = 3

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class Rank(IntEnum):
    TWO = 0,
    THREE = 1,
    FOUR = 2,
    FIVE = 3,
    SIXES = 4,
    SEVEN = 5,
    EIGHT = 6,
    NINE = 7,
    TEN = 8,
    JACK = 9,
    QUEEN = 10,
    KING = 11,
    ACE = 12

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


suits = list(Suit)
ranks = list(Rank)


@dataclass(frozen=True, order=True)
class Card:
    rank: Rank
    suit: Suit

    def __str__(self):
        return f'({self.rank} {self.suit})'

    def __repr__(self):
        return str(self)


def get_all_cards():
    all = [Card(rank=rank, suit=suit) for rank in ranks for suit in suits]
    return all

allCards = get_all_cards()
for _ in range(10):
    hand = sorted(choices(allCards, k=5), reverse=True)
    print(hand)
