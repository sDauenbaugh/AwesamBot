import unittest

import src.util.util as util

class UtilSmokeTestCase(unittest.TestCase):
    def test_turn_radius_slow(self):
        v = 200.0
        radius = util.turn_radius(v)
        self.assertEquals(round(radius, 4), 174.4592)
    
    def test_turn_radius_fast(self):
        v = 2435.7
        radius = util.turn_radius(v)
        self.assertEquals(round(radius, 4), 1211.0643)