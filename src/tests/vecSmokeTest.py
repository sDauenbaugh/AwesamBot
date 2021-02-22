import unittest
import numpy as np

from src.util.vec import Vec3


class VecSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.vec_x = Vec3(10, 0, 0)
        self.vec1 = Vec3(1, 2, 3)
        self.vec45 = Vec3(2, -2, 0)
        self.vec_z = Vec3(0, 0, 5)

    def test_length(self):
        self.assertEqual(self.vec_x.length(), 10)
    
    def test_normalized(self):
        self.assertEqual(self.vec_x.normalized(), Vec3(1, 0, 0))

    def test_dot(self):
        dot = self.vec1.dot(self.vec45)
        self.assertEqual(dot, -2)
    
    def test_cross(self):
        cross = self.vec_z.cross(self.vec1)
        self.assertEqual(cross, Vec3(-10, 5, 0))

    def test_flat(self):
        self.assertEqual(self.vec1.flat(), Vec3(1, 2, 0))

    def test_dist(self):
        distance = self.vec_x.dist(self.vec1)
        self.assertEqual(round(distance, 4), 9.6954)

    def test_angle_to(self):
        angle = round(self.vec_x.ang_to(self.vec45), 4)
        self.assertEqual(angle, round(np.pi/4, 4))

    def test_angle_of(self):
        angle = round(self.vec1.angle_of(), 4)
        self.assertEqual(angle, -1.1071)
