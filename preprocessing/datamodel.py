from preprocessing.candidates import Candidate

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
        return "(%f, %f, %f)" % (self.x, self.y, self.z)


class PointSet:
    def __init__(self, filename):
        self.points = {}
        next_id = 1

        with open(filename) as resource:
            for line in resource:
                x, y, z = [float(s) for s in line.strip().split()[:3]]
                self.points[next_id] = Point(x, y, z)
                next_id += 1

    @property
    def size(self):
        return len(self.points)

    def get_by_id(self, point_id):
        try:
            return self.points[point_id]
        except KeyError:
            return None

    def nearest(self, ref):
        return min((p for p in self.points.values() if p != ref),
                   key=lambda p: p.distance(ref))

    def neighbours(self, ref, radius):
        neighbours = []
        for point in (p for p in self.points.values() if p != ref):
            if abs(point.x - ref.x) <= radius and \
               abs(point.y - ref.y) <= radius and \
               abs(point.z - ref.z) <= radius:
                neighbours.append(point)
        return neighbours


class LearningSet:
    def __init__(self, pset, trajectory_file):
        self.pset = pset
        self.resource = open(trajectory_file)

    def iterate(self):
        for line in self.resource:
            point_ids = [int(i) for i in line.strip().split()]
            trajectory = [self.pset.get_by_id(i) for i in point_ids]

            if any(p is None for p in trajectory):
                continue

            dists = [trajectory[i].distance(trajectory[i+1]) for i in range(4)]
            d_max = max(dists)
            dists = [d_max / 2 if d == d_max else d for d in dists]

            yield Candidate(trajectory, max(dists)).to_standard_order()
