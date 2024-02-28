from poker import get_all_cards, Suit, Rank
import unittest
import itertools


class CardTests(unittest.TestCase):
    cards_per_rank = 13
    cards_per_suits = 4
    total_number_of_cards = cards_per_suits * cards_per_rank
    
    def test_number_of_distinct_cards(self):
        self.assertEqual(len(sorted(list(itertools.groupby(get_all_cards())))), CardTests.total_number_of_cards)

    def test_number_of_suits(self):
        self.assertEqual(len(Suit), CardTests.cards_per_suits)

    def test_number_of_ranks(self):
        self.assertEqual(len(Rank), CardTests.cards_per_rank)


if __name__ == '__main__':
    unittest.main()
