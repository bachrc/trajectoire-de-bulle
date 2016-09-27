from random import choice


class SampleTest:
    def __init__(self, pset, tolerance, angle):
        self.pset = pset
        self.tolerance = tolerance
        self.angle = angle
        self.trajectories = []

    @property
    def score(self):
        return len(self.trajectories)

    def perform(self):
        points_left = [p for p in self.pset.points]
        candidates = []

        while len(points_left) > 0:
            start = points_left.pop()
            nearest = self.pset.nearest(start)
            radius = start.distance(nearest)

            subset = {start: True, nearest: False}
            while len(subset) < 5 and not all(subset.values()):
                base = choice([k for k in subset if not subset[k]])
                subset[base] = True
                for neighbour in self.pset.neighbours(base, radius):
                    if neighbour not in subset:
                        subset[neighbour] = False

            subset = list(subset.keys())
            if len(subset) < 5:
                continue

            if len(subset) > 5:
                subset = sorted(subset, key=lambda p: p.distance(start))[:5]

            candidates.append(subset)
            for point in subset:
                try:
                    points_left.remove(point)
                except ValueError:
                    pass

        for points in candidates:
            # points is a set of 5 points. If it matches the critera for a
            # trajectory given the current parameters (tolerance, angle), add
            # it to trajectories. This test's score is the number of valid
            # trajectories it managed to find.
            pass
