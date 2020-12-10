import unittest

from main import coalesce, Room, Point

class CoalesceTests(unittest.TestCase):
    def test_coalescence(self):
        source = [
            [1, 12],
            [35, 38],
            [1, 12, 17, 25, 35, 38, 40],
            [1, 12, 17, 35, 40],
            [2,3], # A disjoint set just to make it interesting
            [1, 12, 25, 35, 38],
            [7, 20, 24, 37, 39],
            [7, 20, 37],
            [11, 19, 21, 36, 41],
            [11, 19, 36]
        ]
        expected = [
            {2,3},
            {1, 12, 17, 25, 35, 38, 40},
            {7, 20, 24, 37, 39},
            {11, 19, 21, 36, 41}
        ]
        result = list(coalesce(source))
        self.assertEqual(expected, result)

    def test_periphery(self):
        x = Room(Point(0, 0), 2, 5)
        expected = {
            Point(0,0), Point(1,0),
            Point(0,1), Point(1,1),
            Point(0,2), Point(1,2),
            Point(0,3), Point(1,3),
            Point(0,4), Point(1,4)
        }
        self.assertSetEqual(expected, set(x.periphery()))

    def test_periphery_of_larger_room(self):
        x = Room(Point(0,0), 3, 3)
        p = list(x.periphery())
        expected = 8 # should be 3 at top, 3 at bottom, and 2 at middle (center point isn't peripheral)
        self.assertEqual(expected, len(p), "Too many points counted as periphery")

    def test_periphery_of_ten_by_ten_room(self):
        x = Room(Point(0,0), 10, 10)
        p = set(x.periphery())
        expected = 10 + (2*8) + 10
        self.assertEqual(expected, len(p), "Unexpected number of periphery points")
        self.assertIn((0,1), p)

