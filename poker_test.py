from poker import ALL_CARDS, SUITS, RANKS
import unittest
import itertools


class CardTests(unittest.TestCase):
    cards_per_rank = len(RANKS)
    cards_per_suits = len(SUITS)
    total_number_of_cards = cards_per_suits * cards_per_rank
    
    def test_number_of_distinct_cards(self):
        self.assertEqual(len(sorted(list(itertools.groupby(ALL_CARDS)))), CardTests.total_number_of_cards)

if __name__ == '__main__':
    unittest.main()
