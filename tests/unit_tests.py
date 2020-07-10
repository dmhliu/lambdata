#!/usr/bin/env python
import unittest
import numpy as np
from . import lambdata_dmhliu
from lambdata_dmhliu.hd_km import hd


class HaversineDistanceTest(unittest.TestCase):
    """Making sure our example module works haversine(θ) = sin²(θ/2)
    The haversine formula is a very accurate way of computing distances between
     two points on the surface of a sphere using the latitude and longitude of the two points.
    """

    def setUp(self):
        self.zerodist = [1, 1, 1, 1]

        self.test1 = [36.12, -86.67, 33.94, -118.40]
        self.test1Expected = 2887.26

    def testHdZero(self):
        self.assertEqual(hd(self.zerodist), 0)

    def testHDArbitrary(self):
        self.assertEqual(hd(test1), test1Expected)

if __name__ == '__main__':
    unittest.main()
