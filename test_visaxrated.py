import datetime
import unittest
from visaxrated import xrate


class VisaxratedTestCase(unittest.TestCase):
    def test_simple(self):
        v = xrate('SEK', 'USD', 1.65, datetime.date(year=2014, month=10, day=16), 40)
        self.assertEqual(v, 296.23)

    def test_large(self):
        v = xrate('SEK', 'GBP', 1.65, datetime.date(year=2014, month=1, day=1), 1000000)
        self.assertEqual(v, 10820160.73)

if __name__ == '__main__':
    unittest.main()
