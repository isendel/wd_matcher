import unittest
from wd_matcher.wd_distance import WDDistance


class WDDistanceTest(unittest.TestCase):

    def test_get_fuzzy_distance(self):
        # print(WDDistance.get_fuzzy_distance('test', 'tset'))
        # print(WDDistance.get_fuzzy_distance('test and nottest', 'test & nottest'))
        print(WDDistance.get_fuzzy_distance('Freund', 'FREUND PUBLISHING HOUSE, LTD.'))
