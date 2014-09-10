import unittest

from util.mathutil import *


class BoundingBoxTest(unittest.TestCase):

    def test_initizialize(self):
        bbox = BoundingBox()

        self.assertEquals(bbox.xmin, 1e40)
        self.assertEquals(bbox.xmax, -1e40)
        self.assertEquals(bbox.ymin, 1e40)
        self.assertEquals(bbox.ymax, -1e40)

        xmin, xmax, ymin, ymax = (0, 12, 123, 400)
        bbox = BoundingBox(xmin, xmax, ymin, ymax)

        self.assertEquals(bbox.xmin, xmin)
        self.assertEquals(bbox.xmax, xmax)
        self.assertEquals(bbox.ymin, ymin)
        self.assertEquals(bbox.ymax, ymax)

    def test_extend_with_bbox(self):
        bbox = BoundingBox()
        bbox.extend(BoundingBox(0, 1.0, 2, 4))
        bbox.extend(BoundingBox(1, 4, 8, 100))

        self.assertEquals(bbox, BoundingBox(0.0, 4, 2, 100))

    def test_extend_with_2tuple(self):
        bbox = BoundingBox(0, 1, 2, 4).extend(100, 500)

        self.assertEquals(bbox, BoundingBox(0, 100, 2, 500))

    def test_extend_with_4tuple(self):
        bbox = BoundingBox(0, 1, 2, 4).extend(0, 1, 3, 8)

        self.assertEquals(bbox, BoundingBox(0, 1, 2, 8))

    def test_extend_with_line(self):
        bbox = BoundingBox(0, 0, 0, 0)

        bbox.extend(Line((0, 0, 100, 100)))

        self.assertEquals(bbox, BoundingBox(0, 100, 0, 100))

    def test_pad(self):
        bbox = BoundingBox(0, 100, 0, 100).pad(10)

        self.assertEquals(bbox, BoundingBox(-10, 110, -10, 110))

    def test_str(self):
        bbox = BoundingBox(0, 1, 2, 3)

        self.assertEquals(str(bbox), 'BoundingBox([0.0, 1.0, 2.0, 3.0])')

