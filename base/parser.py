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
        return min((p for p in self.points if p != ref),
                   key=lambda p: p.distance(ref))

    def neighbours(self, ref, radius):
        neighbours = []
        for point in (p for p in self.points if p != ref):
            if abs(point.x - ref.x) <= radius and \
               abs(point.y - ref.y) <= radius and \
               abs(point.z - ref.z) <= radius:
                neighbours.append(point)
        return neighbours

    def find_trajectory_candidates(self):
        points_left = [p for p in self.points]
        candidates = []

        while len(points_left) > 0:
            # Pick a point to start with, find its nearest neighbour, and
            # compute the associated radius for the remainder of the process.
            start = points_left.pop()
            nearest = self.nearest(start)
            radius = start.distance(nearest)

            # True: the point has been explored. False: it hasn't. Keep
            # expanding the subset until we've found 5 points.
            subset = {start: True, nearest: False}
            while len(subset) < 5 and not all(subset.values()):
                # Pick an unexplored point, explore it.
                base = [k for k in subset if not subset[k]][0]
                subset[base] = True
                for neighbour in self.neighbours(base, radius):
                    if neighbour not in subset.keys():
                        subset[neighbour] = False

            subset = list(subset.keys())
            if len(subset) < 5:
                # The point appears to be isolated.
                continue

            if len(subset) > 5:
                # Too many points, we might have a trajectory conflict. Let's
                # keep the points closest to our starting point.
                subset = sorted(subset, key=lambda p: p.distance(start))[:5]

            # Save the subset and its search radius for further processing.
            candidates.append({'radius': radius, 'points': subset})
            for point in subset:
                try:
                    points_left.remove(point)
                except ValueError:
                    pass

        return candidates
