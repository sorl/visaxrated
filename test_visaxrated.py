import datetime
import unittest
from visaxrated import xrate


class VisaxratedTestCase(unittest.TestCase):
    def test_simple(self):
        v = xrate('SEK', 'USD', 1.65, datetime.date(year=2014, month=10, day=16), 40)
        self.assertEqual(v, 296.228298328)


if __name__ == '__main__':
    unittest.main()
