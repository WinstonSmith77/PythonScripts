from poker import get_all_cards
import unittest


class CardTests(unittest.TestCase):
    cards_per_suit = 13
    suits = 4
    total_number_of_cards = suits * cards_per_suit
    def test_number_of_cards(self):
        self.assertEqual(len(get_all_cards()), CardTests.total_number_of_cards)


if __name__ == '__main__':
    unittest.main()
