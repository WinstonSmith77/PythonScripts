from poker import get_all_cards
import unittest

class CardTests(unittest.TestCase):

    def test_number_of_cards(self):
        self.assertEqual(len( get_all_cards()), 52)

if __name__ == '__main__':
    unittest.main()



