from poker import ALL_CARDS, SUITS, RANKS, Card, HandType, HandUtils
import unittest
import itertools
from random import Random


class CardTests(unittest.TestCase):
    cards_per_rank = len(RANKS)
    cards_per_suits = len(SUITS)
    total_number_of_cards = cards_per_suits * cards_per_rank

    def _shuffle_and_add(self, cards_and_conds, random=None, number_of_shuffle=100):
        if not random:
            random = Random(42)

        result = []

        for hand, cond in cards_and_conds:
            clones = set()
            for _ in range(number_of_shuffle):
                hand_clone = list(hand)
                random.shuffle(hand_clone)
                clones.add(tuple(hand_clone))
            for hand_clone_distinct in clones:
                result.append((hand_clone_distinct, cond))

        return result

    def test_number_of_distinct_cards(self):
        self.assertEqual(
            len(sorted(list(itertools.groupby(ALL_CARDS)))),
            CardTests.total_number_of_cards,
        )

    def test_str_and_parse_works(self):
        for card in ALL_CARDS:
            text = str(card)
            parsed = Card.parse(text)

            self.assertEqual(card, parsed)

    def _true_for_all_cards(self, type_2_expect):
        cards_and_conds = [
            (ALL_CARDS, lambda cards: type_2_expect in cards),
            ([], lambda cards: type_2_expect not in cards),
        ]

        return cards_and_conds

    def _test_inner(self, cards_and_conds):
        def str_2_card(card):
            if isinstance(card, str):
                return Card.parse(card)
            return card

        cards_and_conds = self._shuffle_and_add(cards_and_conds)

        for hand, cond in cards_and_conds:
            hand = list(map(str_2_card, hand))
            self.assertTrue(cond(HandUtils.get_hand_types(hand)), hand)

    def test_highCard(self):
        type_2_expect = HandType.HIGH
        cards_and_conds = [
            (["h2"], lambda cards: type_2_expect in cards),
        ]
        cards_and_conds += self._true_for_all_cards(type_2_expect)

        self._test_inner(cards_and_conds)

    def test_pair(self):
        type_2_expect = HandType.PAIR
        cards_and_conds = [
            (["h2", "c2"], lambda cards: type_2_expect in cards),
        ]
        cards_and_conds += self._true_for_all_cards(type_2_expect)

        self._test_inner(cards_and_conds)

    def test_three_of_a_kind(self):
        type_2_expect = HandType.THREE_OF_A_KIND
        cards_and_conds = [
            (["h2", "c2", "s2"], lambda cards: type_2_expect in cards),
        ]
        cards_and_conds += self._true_for_all_cards(type_2_expect)

        self._test_inner(cards_and_conds)

    def test_four_of_a_kind(self):
        type_2_expect = HandType.FOUR_OF_A_KIND
        cards_and_conds = [
            (["h2", "c2", "s2", "D2"], lambda cards: type_2_expect in cards),
        ]
        cards_and_conds += self._true_for_all_cards(type_2_expect)

        self._test_inner(cards_and_conds)

    def test_full_house(self):
        type_2_expect = HandType.FULL_HOUSE
        cards_and_conds = [
            (["h2", "c2", "s3", "D3", "h3"], lambda cards: type_2_expect in cards),
            (["h2", "c2", "s3", "D3"], lambda cards: type_2_expect not in cards),
            (
                ["h2", "c2", "s3", "D3", "h3", "h3"],
                lambda cards: type_2_expect in cards,
            ),
        ]
        cards_and_conds += self._true_for_all_cards(type_2_expect)

        self._test_inner(cards_and_conds)

    def test_flush(self):
        type_2_expect = HandType.FLUSH
        cards_and_conds = [
            (["h2", "h3", "h4", "hq", "ha"], lambda cards: type_2_expect in cards),
        ]
        cards_and_conds += self._true_for_all_cards(type_2_expect)

        self._test_inner(cards_and_conds)

    def test_straight(self):
        type_2_expect = HandType.STRAIGHT
        cards_and_conds = [
            (["c2", "h3", "h4", "h5", "h6"], lambda cards: type_2_expect in cards),
            (["h2", "h3", "h4", "h5", "h7"], lambda cards: type_2_expect not in cards),
            (["ha", "h2", "h3", "h4", "h5"], lambda cards: type_2_expect in cards),
        ]
        cards_and_conds += self._true_for_all_cards(type_2_expect)

        self._test_inner(cards_and_conds)

    def test_straight_flush(self):
        type_2_expect = HandType.STRAIGHT_FLUSH
        cards_and_conds = [
            (["c2", "h3", "h4", "h5", "h6"], lambda cards: type_2_expect not in cards),
            (["h2", "h3", "h4", "h5", "h7"], lambda cards: type_2_expect not in cards),
            (["ha", "h2", "h3", "h4", "h5"], lambda cards: type_2_expect in cards),
            (["h6", "h2", "h3", "h4", "h5"], lambda cards: type_2_expect in cards),
        ]
        cards_and_conds += self._true_for_all_cards(type_2_expect)

        self._test_inner(cards_and_conds)

    def test_royal_flush(self):
        type_2_expect = HandType.ROYAL_FLUSH
        cards_and_conds = [
            (["c2", "h3", "h4", "h5", "h6"], lambda cards: type_2_expect not in cards),
            (["h2", "h3", "h4", "h5", "h7"], lambda cards: type_2_expect not in cards),
            (["ha", "hk", "hq", "hj", "h10"], lambda cards: type_2_expect in cards),
            #(["h6", "h2", "h3", "h4", "h5"], lambda cards: type_2_expect in cards),
        ]
        cards_and_conds += self._true_for_all_cards(type_2_expect)

        self._test_inner(cards_and_conds)    


if __name__ == "__main__":
    unittest.main(
        verbosity=4,
    )
