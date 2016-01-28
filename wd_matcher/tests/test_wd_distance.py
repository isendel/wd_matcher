import unittest
from wd_matcher.wd_distance import WDDistance


class WDDistanceTest(unittest.TestCase):
    def test_get_distance(self):
        self.assertEquals(0, WDDistance.get_distance('test', 'test'))
        self.assertEquals(1, WDDistance.get_distance('test', 'test1'))
        self.assertEquals(2, WDDistance.get_distance('test', 'tset'))
        self.assertEquals(3, WDDistance.get_distance('test and nottest', 'test & nottest'))
