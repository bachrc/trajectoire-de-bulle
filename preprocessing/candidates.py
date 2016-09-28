from collections import deque


class Candidate:
    def __init__(self, points, radius):
        self.points = points
        self.radius = radius

    def __repr__(self):
        return ", ".join(p.__repr__() for p in self.points)

    def matches(self, points):
        return all(p in self.points for p in points)


class CandidateSearch:
    def __init__(self, pset):
        self.pset = pset
        self.left = deque()

    def iterate(self):
        if len(self.left) == 0:
            self.left = deque([p for p in self.pset.points.values()])

        while len(self.left) > 0:
            # Pick a point to start with, find its nearest neighbour, and
            # compute the associated radius for the remainder of the process.
            start = self.left.popleft()
            nearest = self.pset.nearest(start)
            radius = start.distance(nearest)

            # True: the point has been explored. False: it hasn't. Keep
            # expanding the subset until we've found 5 points.
            subset = {start: True, nearest: False}
            while len(subset) < 5 and not all(subset.values()):
                # Pick an unexplored point, explore it.
                base = [k for k in subset if not subset[k]][0]
                subset[base] = True
                for neighbour in self.pset.neighbours(base, radius):
                    if neighbour not in subset.keys():
                        subset[neighbour] = False

            subset = list(subset.keys())
            if len(subset) < 5:
                # The point appears to be isolated. Ignore it.
                # TODO: we can try and come back to it (right now, that fails).
                continue

            if len(subset) > 5:
                # Too many points, we might have a trajectory conflict. Let's
                # keep the points closest to our starting point.
                subset = sorted(subset, key=lambda p: p.distance(start))[:5]

            yield Candidate(subset, radius)

    def report_positive(self, candidate):
        for point in candidate.points:
            try:
                self.left.remove(point)
            except ValueError:
                pass
