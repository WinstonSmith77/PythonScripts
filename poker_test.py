from poker import ALL_CARDS, SUITS, RANKS, Card, Rank, Suit, HandType, get_hand_types
import unittest
import itertools
import pprint

class CardTests(unittest.TestCase):
    cards_per_rank = len(RANKS)
    cards_per_suits = len(SUITS)
    total_number_of_cards = cards_per_suits * cards_per_rank
    
    def test_number_of_distinct_cards(self):
        self.assertEqual(len(sorted(list(itertools.groupby(ALL_CARDS)))), CardTests.total_number_of_cards)

    def test_str_and_parse_works(self):
        for card in ALL_CARDS:
            text = str(card)
            parsed = Card.parse(text)

            self.assertEqual(card, parsed)

    def _test_inner(self, cards_and_conds):
         for cards, cond in cards_and_conds:
            cards = list(map(Card.parse, cards))
            self.assertTrue(cond(get_hand_types(cards)))

    def test_highCard(self):
        cards_and_conds = [
            (['h2'], lambda cards : HandType.HIGH in cards),
            ([], lambda cards : HandType.HIGH not in cards)
            ]
        
        self._test_inner(cards_and_conds)

    def test_pair(self):
        cards_and_conds = [
            (['h2', 'c2'], lambda cards : HandType.PAIR in cards),
            ([], lambda cards : HandType.PAIR not in cards)
            ]

        self._test_inner(cards_and_conds)      

if __name__ == '__main__':
    unittest.main(verbosity=4)

