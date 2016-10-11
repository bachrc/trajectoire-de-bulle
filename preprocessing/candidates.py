from itertools import permutations


class Candidate:
    """
    A candidate is a cluster of 5 points which appears to be a viable
    trajectory. Candidates are taken from PointSet instances.
    """

    def __init__(self, points, radius):
        """
        Create a candidate.
        :param points: The list containing 5 Point instances.
        :param radius: The radius used when building the cluster.
        """
        self.points = points
        self.radius = radius

    def __hash__(self):
        return '-'.join(p.__hash__() for p in self.points)

    def __eq__(self, other):
        return self.matches(other.points)

    def __repr__(self):
        return ", ".join(str(p.__repr__()) for p in self.points)

    def matches(self, points):
        """
        Tells whether a candidate represents a given set of points.
        :param points: The point to match against.
        :return: True if all points in "points" are in the candidate.
        """
        return all(p in self.points for p in points)

    def raw(self, smooth=False):
        """
        Returns a basic representation of a candidate, as a matrix of
        coordinates.
        :param smooth: If true, the matrix will be flattened (3x5 => 15x1).
        :return: The candidate's values.
        """
        coords = [(p.x, p.y, p.z) for p in self.points]
        return [c for tp in coords for c in tp] if smooth else coords

    def to_standard_order(self):
        """
        Orders the candidate's points in the "most likely" arrangement. This
        basically iterates over all positions 120 possibles arrangements, and
        picks the one which creates the shortest node-to-node path.
        :return: The current candidate : the modification is made in-place.
        """
        self.points = min(permutations(self.points),
                          key=lambda p: sum([p[i].distance(p[i+1])
                                             for i in range(4)]))
        return self


class CandidateSearch:
    """
    This class is responsible for the search of candidates in a given PointSet.
    The iterate() method should be used as the generator giving access to these
    candidates.
    """

    def __init__(self, pset, radius_flex=2):
        """
        Initialises the search.
        :param pset: The associated PointSet.
        :param radius_flex: A tolerance ratio applied when doing the neighbours
        radial search. Makes the algorithm more tolerance to small movement
        variations in the whirlwind.
        """
        self.pset_bak = pset
        self.pset = None
        self.radius_flex = radius_flex
        self.banned_starts = set()

    def iterate(self, raw_smooth=False):
        """
        Yields a new candidate every time it's called.
        :param raw_smooth: Set to true if you want to receive the candidates in
        raw() form.
        :return: A candidate, or None when done. Use this function as a
        generator.
        """
        if self.pset is None:
            # First call: copy the PointSet so we can remove points when needed.
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

            candidate = Candidate(subset, search_radius)
            candidate.to_standard_order()

            yield candidate.raw(True) if raw_smooth else candidate

        self.pset = None

    def report_positive(self, candidate):
        """
        Reports a given candidate as positive, effectively removing its points
        from the in-cache PointSet, making sure they never come up again, and
        don't misguide the rest of the search.
        :param candidate: A positive candidate.
        """
        for point in candidate.points:
            try:
                self.pset.remove(point)
                self.banned_starts.remove(point)
            except (ValueError, KeyError):
                pass
