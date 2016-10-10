from preprocessing.candidates import Candidate

from collections import deque
from math import sqrt


class Point:
    def __init__(self, p_id, x, y, z):
        self.p_id = p_id
        self.x, self.y, self.z = x, y, z

    def distance(self, point):
        # 3D shortest distance between two points.
        dx = pow(self.x - point.x, 2)
        dy = pow(self.y - point.y, 2)
        dz = pow(self.z - point.z, 2)
        return sqrt(dx + dy + dz)

    def distance_to_line(self, p1, p2):
        # Point-to-line distance using a projection of the target point onto the
        # line. Useful when trying to keep points around an axis.
        l2 = pow(p1.x - p2.x, 2) + pow(p1.y - p2.y, 2) + pow(p1.z - p2.z, 2)
        l2 = sqrt(l2)
        if l2 == 0:
            return self.distance(p1)

        t = (self.x - p1.x) * (p2.x - p1.x)
        t += (self.y - p1.y) * (p2.y - p1.y)
        t += (self.z - p1.z) * (p2.z - p1.z)
        t = max(0, min(1, t / l2))
        proj = Point(0, p1.x + t * (p2.x - p1.x),
                     p1.y + t * (p2.y - p1.y),
                     p1.z + t * (p2.z - p1.z))
        return self.distance(proj)

    def __hash__(self):
        return self.p_id

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self):
        return "(%f, %f, %f)" % (self.x, self.y, self.z)


class PointSet:
    def __init__(self, filename=None):
        self.points = deque()
        self.ids = {}
        next_id = 1

        if filename is not None:
            with open(filename) as resource:
                for line in resource:
                    x, y, z = [float(s) for s in line.strip().split()[:3]]
                    point = Point(next_id, x, y, z)
                    self.ids[next_id] = point
                    self.points.append(point)
                    next_id += 1

    def copy(self):
        pcopy = PointSet()
        for point in self.points:
            pcopy.ids[point.p_id] = point
            pcopy.points.append(point)
        return pcopy

    def size(self):
        return len(self.points)

    def push_back(self, point):
        if point.p_id not in self.ids:
            self.ids[point.p_id] = point
            self.points.append(point)

    def remove(self, point):
        if point.p_id not in self.ids:
            return

        del self.ids[point.p_id]
        self.points.remove(point)

    def get_by_id(self, point_id):
        try:
            return self.ids[point_id]
        except KeyError:
            return None

    def pop_iterate(self):
        while len(self.points) > 0:
            point = self.points.popleft()
            del self.ids[point.p_id]
            yield point

    def nearest(self, ref):
        try:
            return min((p for p in self.points if p != ref),
                       key=lambda p: p.distance(ref))
        except ValueError:
            return None

    def neighbours(self, ref, radius):
        for point in (p for p in self.points if p != ref):
            if abs(point.x - ref.x) <= radius and \
               abs(point.y - ref.y) <= radius and \
               abs(point.z - ref.z) <= radius:
                yield point


class LearningSet:
    def __init__(self, pset, trajectory_file):
        self.pset = pset
        self.trajectory_file = trajectory_file

    def iterate(self):
        with open(self.trajectory_file) as resource:
            for line in resource:
                point_ids = [int(i) for i in line.strip().split()]
                trajectory = [self.pset.get_by_id(i) for i in point_ids]

                if any(p is None for p in trajectory):
                    continue

                dists = [trajectory[i].distance(trajectory[i+1])
                         for i in range(4)]
                d_max = max(dists)
                dists = [d_max / 2.0 if d == d_max else d for d in dists]

                yield Candidate(trajectory, max(dists)).to_standard_order()
