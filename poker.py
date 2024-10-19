from enum import IntEnum
from random import Random
from itertools import groupby, repeat
from dataclasses import dataclass
from pprint import pprint

from multiprocessing.pool import Pool
import functools
import time
import cProfile


def benchmark(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        stop_time = time.time()
        delta = stop_time - start_time
        pprint(f"{f.__name__} Delta {delta}")
        return result

    return wrapper


class CardComponentBase(IntEnum):
    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class HandType(CardComponentBase):
    HIGH = 0
    PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9


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


SUITS = tuple(Suit)
RANKS = tuple(Rank)

ALL_CARDS = tuple([Card(rank=rank, suit=suit) for rank in RANKS for suit in SUITS])


class HandUtils:
    @classmethod
    def get_hand(cls, length, random):
        result = random.choices(ALL_CARDS, k=length)
        return result

    @classmethod
    def find_len_groups(cls, hand_by_key, key, found_at_least_length):
        len_groups = sorted([len(tuple(g)) for _, g in groupby(hand_by_key, key=key)])

        result = {
            number_of_repeats: sum(len_of_group >= number_of_repeats for len_of_group in len_groups)
            for number_of_repeats in found_at_least_length
        }

        return result

    @classmethod
    def split_suits(cls, hand_by_rank):
        def key_suit(card):
            return card.suit

        sorted_by_suit = sorted(hand_by_rank, key=key_suit)
        cards_by_suit = tuple(
            [tuple(v) for _, v in groupby(sorted_by_suit, key=key_suit)]
        )
        return cards_by_suit

    @classmethod
    def is_straight_flush_or_royal(cls, cards_by_suit, *, royal=False):
        return any(cls.is_straight(cards, royal) for cards in cards_by_suit)

    @classmethod
    def is_straight(cls, hand_by_rank, royal=False):
        result = False
        if hand_by_rank:
            last_card = hand_by_rank[0]
            last_card_rank_value = last_card.rank.value
            length_straight = 1

            for i in range(1, len(hand_by_rank)):
                if (
                    royal
                    and last_card.rank != cls._order_royal_flush[length_straight - 1]
                ):
                    length_straight = 1
                    last_card = hand_by_rank[i]
                    last_card_rank_value = last_card.rank.value
                    continue

                current_card = hand_by_rank[i]
                current_card_rank_value = current_card.rank.value

                if current_card_rank_value == last_card_rank_value:
                    continue
                elif current_card_rank_value == last_card_rank_value + 1 or (
                    last_card_rank_value == Rank.FIVE.value
                    and current_card_rank_value == Rank.ACE.value
                ):  # Ace as start of straight
                    length_straight += 1
                else:
                    length_straight = 1
                if length_straight == 5:
                    result = True
                    break
                last_card = current_card
                last_card_rank_value = current_card_rank_value

        return result

    _order_royal_flush = tuple([Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING, Rank.ACE])
    _flush_group_length = tuple([5])
    _rank_group_lengths = tuple({2, 3, 4})
    

    @classmethod
    def get_hand_types(cls, hand, highpythinest_only=False):
        results = {HandType.HIGH} if hand else set()

        hand_by_rank = sorted(hand, key=lambda c: c.rank)
        found_at_least_rank = cls.find_len_groups(
            hand_by_rank, lambda c: c.rank, HandUtils._rank_group_lengths
        )

        if found_at_least_rank[2]:
            results.add(HandType.PAIR)
            if found_at_least_rank[3]:
                results.add(HandType.THREE_OF_A_KIND)
                if found_at_least_rank[2] >= 2:
                    results.add(HandType.FULL_HOUSE)
            if found_at_least_rank[4]:
                results.add(HandType.FOUR_OF_A_KIND)
            if found_at_least_rank[2] >= 2:
                results.add(HandType.TWO_PAIR)

        cards_by_suit = cls.split_suits(hand_by_rank)

        if cls.is_straight(hand_by_rank):
            results.add(HandType.STRAIGHT)
            if cls.is_straight_flush_or_royal(cards_by_suit):
                results.add(HandType.STRAIGHT_FLUSH)
                if cls.is_straight_flush_or_royal(cards_by_suit, royal=True):
                    results.add(HandType.ROYAL_FLUSH)

        len_flush = 5
        if any(map(lambda c: len(c) >= len_flush, cards_by_suit)):
            results.add(HandType.FLUSH)

        if highest_only:
            highest = sorted(results, reverse=True)[0]
            results = set()
            results.add(highest)

        return results


def doit(param):
    number, length, seed = param
    total = {type: 0 for type in HandType}

    ran = Random(seed)
    for _ in range(number):
        hand = HandUtils.get_hand(length, ran)
        hand_types = HandUtils.get_hand_types(hand, True)

        for type in total:
            total[type] += 1 if type in hand_types else 0

    return total


@benchmark
def to_bench(use_parallel, scale=1):
    total_number = 2_000_000 // scale
    chunks = 500
    per_chunks = total_number // chunks

    hand_size = 8

    ran = Random(42)

    input = list(repeat((per_chunks, hand_size), chunks))
    input = [(a, b, ran.random()) for a, b in input]
    if use_parallel:
        with Pool() as pool:
            results = list(pool.map(doit, input))
    else:
        results = list(map(doit, input))

    all_types = {hand: 0 for hand in HandType}
    for result in results:
        for type in result:
            all_types[type] += result[type]

    sum = 0
    for type in all_types:
        sum += all_types[type]
        all_types[type] = (all_types[type], all_types[type] / total_number)

    all_types = sorted(all_types.items(), key=lambda x: x[1][1], reverse=True)

    pprint(f"Multiprocessing {use_parallel}")
    pprint(sum, underscore_numbers=True)
    pprint(all_types, underscore_numbers=True)


if __name__ == "__main__":
    to_bench(True)
    to_bench(False)

    #cProfile.run("to_bench(False, 10)", sort="tottime")
