import unittest
import numpy as np

import src.util.util as util
from util.vec import Vec3


class UtilSmokeTestCase(unittest.TestCase):
    def test_turn_radius_slow(self):
        v = 200.0
        radius = util.turn_radius(v)
        self.assertEquals(round(radius, 4), 174.4592)
    
    def test_turn_radius_fast(self):
        v = 2435.7
        radius = util.turn_radius(v)
        self.assertEquals(round(radius, 4), 1211.0643)

    def test_sign_positive(self):
        self.assertEquals(util.sign(5), 1)
    
    def test_sign_negative(self):
        self.assertEquals(util.sign(-5), -1)
    
    def test_sign_zero(self):
        self.assertEquals(util.sign(0), -1)
    
    def test_sin_lookup(self):
        lookup = np.round(util.generate_sin_lookup(np.pi/4), 4)
        root = 1/np.sqrt(2)
        table = np.round(np.array([0.00, root, 1.00, root, 0.00, -root, -1, -root]), 4)
        self.assertTrue(np.array_equal(lookup, table))

    def test_cos_lookup(self):
        lookup = np.round(util.generate_cos_lookup(np.pi/4), 4)
        root = 1/np.sqrt(2)
        table = np.round(np.array([1.00, root, 0.00, -root, -1.00, -root, 0.00, root]), 4)
        self.assertTrue(np.array_equal(lookup, table))

    def test_on_target_2d(self):
        pos = Vec3(100, 100, 0)
        vel = Vec3(10, 10, 73)
        left = Vec3(230, 200, 0)
        right = Vec3(190, 200, 0)
        self.assertTrue(util.is_on_target_2d(pos, vel, left, right))
