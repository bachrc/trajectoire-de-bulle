import numpy as np
import math as m
from itertools import permutations


def angle(v1, v2):
    # TODO: not sure this is the angle we're interested in. Try a projection?
    v1 /= np.linalg.norm(v1)
    v2 /= np.linalg.norm(v2)
    return 180.0 * np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0)) / m.pi


class SampleTest:
    def __init__(self, pset, tolerance, angle):
        self.pset = pset
        self.tolerance = tolerance
        self.angle = angle
        self.trajectories = []

    @property
    def score(self):
        return len(self.trajectories)

    def validate_candidate(self, candidate, radius):
        # Determine the order of the points. Simplest solution is to select
        # the sequence which creates the shortest path when connecting the
        # dots.
        sequence = min(permutations(candidate),
                       key=lambda p: sum([p[i].distance(p[i+1])
                                          for i in range(4)]))

        # Compute the slopes and the angles.
        slopes = [(sequence[i+1].x - sequence[i].x,
                   sequence[i+1].y - sequence[i].y,
                   sequence[i+1].z - sequence[i].z) for i in range(4)]
        angles = [angle(slopes[i], slopes[i+1]) for i in range(3)]

        distances = []
        for i in range(4):
            new_distance = sequence[i].distance(sequence[i+1])
            distances.append(new_distance / 2.0 if i == 2 else new_distance)

        distance_max = radius * (1 + self.tolerance)
        valid_angles = all(a <= self.angle for a in angles)
        valid_distances = all(d <= distance_max for d in distances)

        return sequence if valid_angles and valid_distances else None

    def perform(self):
        points_left = [p for p in self.pset.points]

        while len(points_left) > 0:
            # Pick a point to start with, find its nearest neighbour, and
            # compute the associated radius for the remainder of the process.
            start = points_left.pop()
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
                # The point appears to be isolated.
                continue

            if len(subset) > 5:
                # Too many points, we might have a trajectory conflict. Let's
                # keep the points closest to our starting point.
                subset = sorted(subset, key=lambda p: p.distance(start))[:5]

            # Check the candidate immediately to see which points need to be
            # removed from the system.
            validation = self.validate_candidate(subset, radius)
            if validation is not None:
                for point in subset:
                    try:
                        points_left.remove(point)
                    except ValueError:
                        pass
                self.trajectories.append(validation)
