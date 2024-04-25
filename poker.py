from enum import IntEnum
from random import choices
from itertools import groupby
from dataclasses import dataclass
from pprint import pprint


class CardComponentBase(IntEnum):
    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class HandType(CardComponentBase):
    HIGH = 0
    PAIR = 1
    THREE_OF_A_KIND = 2
    FULL_HOUSE = 3
    FLUSH = 4
    FOUR_OF_A_KIND = 5


class Suit(CardComponentBase):
    HEARTS = 0
    DIAMONDS = 1
    CLUBS = 2
    SPADES = 3


class Rank(CardComponentBase):
    TWO = 0
    THREE = 1
    FOUR = 2
    FIVE = 3
    SIX = 4
    SEVEN = 5
    EIGHT = 6
    NINE = 7
    TEN = 8
    JACK = 9
    QUEEN = 10
    KING = 11
    ACE = 12


@dataclass(frozen=True, order=True)
class Card:
    _subst_suits = {
        Suit.HEARTS: ["♥", "H"],
        Suit.DIAMONDS: ["♦", "D"],
        Suit.CLUBS: ["♣", "C"],
        Suit.SPADES: ["♠", "S"],
    }

    _subst_ranks = {
        Rank.TWO: ["2"],
        Rank.THREE: ["3"],
        Rank.FOUR: ["4"],
        Rank.FIVE: ["5"],
        Rank.SIX: ["6"],
        Rank.SEVEN: ["7"],
        Rank.EIGHT: ["8"],
        Rank.NINE: ["9"],
        Rank.TEN: ["10"],
        Rank.JACK: ["J"],
        Rank.KING: ["K"],
        Rank.QUEEN: ["Q"],
        Rank.ACE: ["A"],
    }
    rank: Rank
    suit: Suit

    def __str__(self):
        suit = self.suit
        suit = self._subst_suits.get(suit, [str(suit)])[0]
        rank = self.rank
        rank = self._subst_ranks.get(rank, [str(rank)[0]])[0]

        return f"({suit}{rank})"

    def __repr__(self):
        return str(self)

    @staticmethod
    def resubs(enumType, shortText, subs):
        for enumValue in enumType:
            if shortText.upper() in subs[enumValue]:
                return enumValue

    @classmethod
    def parse(cls, shortText: str):
        shortText = shortText.strip("()")

        suitText = shortText[0].upper()
        rankText = shortText[1:].upper()

        suit = Card.resubs(Suit, suitText, cls._subst_suits)
        rank = Card.resubs(Rank, rankText, cls._subst_ranks)

        return Card(rank, suit)
    
    def __getattr__(self, name):
        return self.parse(name)


SUITS = list(Suit)
RANKS = list(Rank)

ALL_CARDS = [Card(rank=rank, suit=suit) for rank in RANKS for suit in SUITS]


def get_hand(length):
    result = choices(ALL_CARDS, k=length)
    return result

def find_len_groups(hand, key, found_at_least_length):
    found_at_least_length = {length:0 for length in found_at_least_length}
    hand_by_key = sorted(hand, key=key)
    len_groups = sorted([len(list(g)) for _, g in groupby(hand_by_key, key=key)])

    for _length in len_groups:
        for repeat in found_at_least_length:
            if _length >= repeat:
                found_at_least_length[repeat] += 1

    return found_at_least_length            

def get_hand_types(hand):
    result = {HandType.HIGH} if hand else set()
  
    found_at_least_rank=find_len_groups(hand, lambda c : c.rank, [2,3,4])
       
    if found_at_least_rank[2]:
        result.add(HandType.PAIR)
    if found_at_least_rank[2] >= 2 and found_at_least_rank[3]:
        result.add(HandType.FULL_HOUSE)
    if found_at_least_rank[3]:
        result.add(HandType.THREE_OF_A_KIND)
    if found_at_least_rank[4]:
        result.add(HandType.FOUR_OF_A_KIND)
  
    found_at_least_suit=find_len_groups(hand,  lambda c : c.suit, [5])

    if found_at_least_suit[5]:
          result.add(HandType.FLUSH)

    return result


if __name__ == "__main__":
    number = 1_000_000
    length = 5

    total = {type: 0 for type in HandType}

    for i in range(number):
        hand = get_hand(length)
        hand_types = get_hand_types(hand)

        for type in total:
            total[type] += 1 if type in hand_types else 0

    for type in total:
        total[type] = (total[type], total[type] / number)

    total = sorted(total.items(), key=lambda x: x[1][1])

    pprint(total)
