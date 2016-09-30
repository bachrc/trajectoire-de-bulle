from itertools import permutations


class Candidate:
    def __init__(self, points, radius):
        self.points = points
        self.radius = radius

    def __repr__(self):
        return ", ".join(p.__repr__() for p in self.points)

    def matches(self, points):
        return all(p in self.points for p in points)

    def to_standard_order(self):
        self.points = min(permutations(self.points),
                          key=lambda p: sum([p[i].distance(p[i+1])
                                             for i in range(4)]))
        return self


class CandidateSearch:
    def __init__(self, pset, radius_flex=2):
        self.pset_bak = pset
        self.pset = None
        self.radius_flex = radius_flex
        self.banned_starts = set()

    def iterate(self):
        if self.pset is None:
            self.pset = self.pset_bak.copy()

        while self.pset.size() > len(self.banned_starts):
            # Pick a point to start with, and make sure we don't come back
            # twice. This process stops when all possible starts have been
            # exhausted.
            start = next(self.pset.pop_iterate())
            if start in self.banned_starts:
                self.pset.push_back(start)
                continue
            self.banned_starts.add(start)

            # Find the nearest neighbour, and compute a search radius.
            nearest = self.pset.nearest(start)
            if nearest is None:
                continue
            search_radius = start.distance(nearest) * self.radius_flex

            # True: the point has been explored. False: it hasn't. Keep
            # expanding the subset until we've found 5 points.
            subset = {start: False, nearest: False}
            while len(subset) < 5 and not all(subset.values()):
                # Pick an unexplored point, explore it.
                base = [k for k in subset if not subset[k]][0]
                subset[base] = True
                for neighbour in self.pset.neighbours(base, search_radius):
                    if neighbour not in subset.keys():
                        subset[neighbour] = False

            subset = list(subset.keys())
            if len(subset) < 5:
                # Starting from here wasn't interesting, but this point can
                # still come up as useful as part of a trajectory once other
                # candidate have been ruled out. We'll push it back.
                self.pset.push_back(start)
                continue

            if len(subset) > 5:
                # Too many points, we might have a trajectory conflict. We used
                # to keep the points closest to the start, but it turns out
                # using a point-to-line distance also helps keep a descent
                # trajectory axis.
                subset = sorted(subset,
                                key=lambda p:
                                p.distance_to_line(start, nearest))[:5]

            yield Candidate(subset, search_radius).to_standard_order()

        self.pset = None

    def report_positive(self, candidate):
        for point in candidate.points:
            try:
                self.pset.remove(point)
                self.banned_starts.remove(point)
            except (ValueError, KeyError):
                pass
