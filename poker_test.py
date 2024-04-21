from poker import ALL_CARDS, SUITS, RANKS, Card, Rank, Suit
import unittest
import itertools
from pprint import pprint


class CardTests(unittest.TestCase):
    cards_per_rank = len(RANKS)
    cards_per_suits = len(SUITS)
    total_number_of_cards = cards_per_suits * cards_per_rank
    
    def test_number_of_distinct_cards(self):
        self.assertEqual(len(sorted(list(itertools.groupby(ALL_CARDS)))), CardTests.total_number_of_cards)

    def test_str_and_parse_works(self):
        for card in ALL_CARDS:
            if card.suit == Suit.HEARTS and card.rank == Rank.JACK:
                pass
            text = str(card)
            pprint(text)
           
            parsed = Card.parse(text)
            self.assertEqual(card, parsed)

if __name__ == '__main__':
    unittest.main()
