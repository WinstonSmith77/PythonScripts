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
         def mapper(card):
             if isinstance(card, str):
                 return Card.parse(card)
             return card
        
         for cards, cond in cards_and_conds:
            cards = list(map(mapper, cards))
            self.assertTrue(cond(get_hand_types(cards)))

    def test_highCard(self):
        typeToTest = HandType.HIGH
        cards_and_conds = [
            (ALL_CARDS, lambda cards : typeToTest in cards),
            (['h2'], lambda cards : typeToTest in cards),
            ([], lambda cards : typeToTest not in cards)
            ]
        
        self._test_inner(cards_and_conds)

    def test_pair(self):
        typeToTest = HandType.PAIR
        cards_and_conds = [
            (ALL_CARDS, lambda cards : typeToTest in cards),
            (['h2', 'c2'], lambda cards : typeToTest in cards),
            ([], lambda cards : typeToTest not in cards)
            ]

        self._test_inner(cards_and_conds)      

    def test_three_of_a_kind(self):
        typeToTest = HandType.THREE_OF_A_KIND
        cards_and_conds = [
            (ALL_CARDS, lambda cards : typeToTest in cards),
            (['h2', 'c2', 's2'], lambda cards : typeToTest in cards),
            ([], lambda cards : typeToTest not in cards)
            ]

        self._test_inner(cards_and_conds)        

    def test_four_of_a_kind(self):
        typeToTest = HandType.FOUR_OF_A_KIND
        cards_and_conds = [
            (ALL_CARDS, lambda cards : typeToTest in cards),
            (['h2', 'c2', 's2', 'D2'], lambda cards : typeToTest in cards),
            ([], lambda cards : typeToTest not in cards)
            ]

        self._test_inner(cards_and_conds)     

    def test_full_house(self):
        typeToTest = HandType.FULL_HOUSE
        cards_and_conds = [
            (ALL_CARDS, lambda cards : typeToTest in cards),
           # (['h2', 'c2', 's3', 'D3', 'h3'], lambda cards : typeToTest in cards),
            #([], lambda cards : typeToTest not in cards)
            ]

        self._test_inner(cards_and_conds)              

if __name__ == '__main__':
    unittest.main(verbosity=4)

