import unittest
import numpy as np

from src.util.vec import Vec3

class VecSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.vecx = Vec3(10, 0, 0)
        self.vec1 = Vec3(1,2,3)
        self.vec45 = Vec3(2,-2,0)
        self.vecz = Vec3(0, 0, 5)

    def test_length(self):
        self.assertEquals(self.vecx.length(), 10)
    
    def test_normalized(self):
        self.assertEquals(self.vecx.normalized(), Vec3(1,0,0))

    def test_dot(self):
        dot = self.vec1.dot(self.vec45)
        self.assertEquals(dot, -2)
    
    def test_cross(self):
        cross = self.vecz.cross(self.vec1)
        self.assertEquals(cross, Vec3(-10,5,0))

    def test_flat(self):
        self.assertEquals(self.vec1.flat(), Vec3(1,2,0))

    def test_dist(self):
        distance = self.vecx.dist(self.vec1)
        self.assertEquals(round(distance, 4), 9.6954)

    def test_angle_to(self):
        angle = round(self.vecx.ang_to(self.vec45), 4)
        self.assertEquals(angle, round(np.pi/4, 4))