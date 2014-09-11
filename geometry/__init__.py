from math import cos, sin, degrees, radians, atan2, acos, hypot

from boundingbox import BoundingBox

Zero = 0.0000001


############################################################################
# routine takes an x and a y coords and does a coordinate transformation   #
# to a new coordinate system at angle from the initial coordinate system   #
# Returns new x,y tuple                                                    #
############################################################################
def Transform(x, y, angle):
    newx = x * cos(angle) - y * sin(angle)
    newy = x * sin(angle) + y * cos(angle)
    return newx, newy


############################################################################
# routine takes an sin and cos and returns the angle (between 0 and 360)   #
############################################################################
def Get_Angle(s, c):
    if (s >= 0.0 and c >= 0.0):
        angle = degrees(acos(c))
    elif (s >= 0.0 and c < 0.0):
        angle = degrees(acos(c))
    elif (s < 0.0 and c <= 0.0):
        angle = 360 - degrees(acos(c))
    elif (s < 0.0 and c > 0.0):
        angle = 360 - degrees(acos(c))
    else:
        pass

    if angle < 0.001 and s < 0:
        angle == 360.0
    if angle > 359.999 and s >= 0:
        angle == 0.0
    return angle


############################################################################
# routine takes an x and y the point is rotated by angle returns new x,y   #
############################################################################
def Rotn(x, y, angle, radius):
    if radius > 0.0:
        alpha = x / radius
        xx = (radius + y) * sin(alpha)
        yy = (radius + y) * cos(alpha)
    elif radius < 0.0:
        alpha = x / radius
        xx = (radius + y) * sin(alpha)
        yy = (radius + y) * cos(alpha)
    else:
        # radius is exacly 0
        alpha = 0
        xx = x
        yy = y

    rad = hypot(xx, yy)
    theta = atan2(yy, xx)
    newx = rad * cos(theta + radians(angle))
    newy = rad * sin(theta + radians(angle))
    return newx, newy, alpha


############################################################################
# routine takes an x and a y scales are applied and returns new x,y tuple  #
############################################################################
def CoordScale(x, y, xscale, yscale):
    newx = x * xscale
    newy = y * yscale
    return newx, newy


class Character(object):
    def __init__(self, key):
        self.key = key
        self.stroke_list = []

    def __repr__(self):
        return "%%s" % (self.stroke_list)

    def bounds(self):
        return BoundingBox(
            self.get_xmin(),
            self.get_xmax(),
            self.get_ymin(),
            self.get_ymax())

    def get_xmin(self):
        try:
            return min([s.xmin for s in self.stroke_list[:]])
        except ValueError:
            return 0

    def get_xmax(self):
        try:
            return max([s.xmax for s in self.stroke_list[:]])
        except ValueError:
            return 0

    def get_ymax(self):
        try:
            return max([s.ymax for s in self.stroke_list[:]])
        except ValueError:
            return 0

    def get_ymin(self):
        try:
            return min([s.ymin for s in self.stroke_list[:]])
        except ValueError:
            return 0


class Line(object):
    def __init__(self, coords):
        self.xstart, self.ystart, self.xend, self.yend = coords

        self.xmin = min(self.xstart, self.xend)
        self.xmax = max(self.xstart, self.xend)
        self.ymin = min(self.ystart, self.yend)
        self.ymax = max(self.ystart, self.yend)

    def bounds(self):
        return BoundingBox(self.xmin, self.xmax, self.ymin, self.ymax)

    def __repr__(self):
        return "Line([%s, %s, %s, %s])" % (self.xstart, self.ystart, self.xend, self.yend)


def point_inside_polygon(self, x, y, poly):
    '''
    determine if a point is inside a given polygon or not
    Polygon is a list of (x,y) pairs.
    http://www.ariel.com.au/a/python-point-int-poly.html
    '''
    n = len(poly)
    inside = -1
    p1x = poly[0][0]
    p1y = poly[0][1]
    for i in range(n + 1):
        p2x = poly[i % n][0]
        p2y = poly[i % n][1]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = inside * -1
        p1x, p1y = p2x, p2y

    return inside