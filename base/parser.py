from elements import Point


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

    def shallow_copy(self):
        return [p for p in self.points]

    def get_nearest(self, ref):
        d_min = -1
        nearest = None
        for point in self.points:
            coords = ((point.x, ref.x), (point.y, ref.y), (point.z, ref.z))
            d = sum([pow(p - r, 2) for p, r in c] for c in coords)
            if d_min < 0 or d < d_min:
                d_min = d
                nearest = point
        return nearest
