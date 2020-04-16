import unittest

from src.util.vec import Vec3

class VecOperatorTestCase(unittest.TestCase):
    def setUp(self):
        self.vec1 = Vec3(1,2,3)
        self.vec2 = Vec3(10,20,30)

    def test_vec_equals(self):
        self.assertEquals(self.vec1, Vec3(1,2,3))

    def test_vec_add(self):
        sum = self.vec1 + self.vec2
        self.assertEquals(sum, Vec3(11,22,33))
        
    def test_vec_getitem(self):
        self.assertEquals(self.vec1.x, 1)

    def test_vec_subtract(self):
        self.assertEqual(self.vec2 - self.vec1, Vec3(9,18,27))

    def test_vec_negate(self):
        self.assertEquals(-self.vec1, Vec3(-1,-2,-3))

    def test_vec_subtract_negative(self):
        negVec = -self.vec1
        self.assertEquals(self.vec2 - negVec, Vec3(11,22,33))

    def test_vec_add_negative(self):
        negVec = -self.vec1
        self.assertEqual(self.vec2 + negVec, Vec3(9,18,27))

    def test_vec_scalar_multiply(self):
        scaledVec = self.vec1 * 10
        self.assertEquals(scaledVec, self.vec2)

    