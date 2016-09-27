from math import sqrt


class Point:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def distance(self, point):
        dx = pow(self.x - point.x, 2)
        dy = pow(self.y - point.y, 2)
        dz = pow(self.z - point.z, 2)
        return sqrt(dx + dy + dz)

    def __lt__(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.y - other.z
        return dx if dx != 0 else dy if dy != 0 else dz

    def __hash__(self):
        return hash("%s%s%s" % (self.x, self.y, self.z))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self):
        return "(%f ; %f ; %f)" % (self.x, self.y, self.z)


class PointSet:
    def __init__(self, filename):
        self.points = []
        with open(filename) as resource:
            for line in resource:
                x, y, z = [float(s) for s in line.strip().split()[:3]]
                self.points.append(Point(x, y, z))

    @property
    def size(self):
        return len(self.points)

    def nearest(self, ref):
        return min(self.points, key=lambda p: p.distance(ref))

    def neighbours(self, ref, radius):
        neighbours = []
        for point in self.points:
            if abs(point.x - ref.x) <= radius and \
               abs(point.y - ref.y) <= radius and \
               abs(point.z - ref.z) <= radius:
                neighbours.append(point)
        return neighbours
