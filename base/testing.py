from random import choice
import numpy as np
import math as m


def unit_vector(vector):
    return vector / np.linalg.norm(vector)


def angle(v1, v2):
    v1 /= np.linalg.norm(v1)
    v2 /= np.linalg.norm(v2)
    angle_rad = np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))
    return abs(180.0 * angle_rad / m.pi)


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
        self.find_trajectories(self.find_candidates())

    def find_candidates(self):
        points_left = [p for p in self.pset.points]
        candidates = []

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
                base = choice([k for k in subset if not subset[k]])
                subset[base] = True
                for neighbour in self.pset.neighbours(base, radius):
                    if neighbour not in subset:
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

    def find_trajectories(self, candidates):
        for candidate in candidates:
            points = candidate['points']

            # points is a set of 5 points. If it matches the criteria for a
            # trajectory given the current parameters (tolerance, angle), add
            # it to self.trajectories. This test's score is the number of valid
            # trajectories it managed to find.

            # First, compute the distances between consecutive points in each
            # plane in order to determine orientation.
            pxs = [(p1, p2) for p1 in points for p2 in points if p1.x <= p2.x]
            pys = [(p1, p2) for p1 in points for p2 in points if p1.y <= p2.y]
            pzs = [(p1, p2) for p1 in points for p2 in points if p1.z <= p2.z]
            dxs = [p1.x - p2.x for p1, p2 in pxs if p1 != p2]
            dys = [p1.y - p2.y for p1, p2 in pys if p1 != p2]
            dzs = [p1.z - p2.z for p1, p2 in pzs if p1 != p2]

            # Note that trajectories might have more than one orientation, but
            # sorting is merely here to help construct a valid slope.
            # TODO: try and check all valid orientations?
            if all(d == dxs[0] for d in dxs[1:]):
                # Trajectory has an x-axis orientation.
                points.sort(key=lambda p: p.x)
            elif all(d == dys[0] for d in dys[1:]):
                # Trajectory has an z-axis orientation.
                points.sort(key=lambda p: p.y)
            elif all(d == dzs[0] for d in dzs[1:]):
                # Trajectory has an y-axis orientation.
                points.sort(key=lambda p: p.z)
            else:
                # Trajectory doesn't appear to be oriented, forget it.
                continue

            # With the points in a consecutive order, we can compute the slopes.
            slopes = [(points[i].x - points[i+1].x,
                       points[i].y - points[i+1].y,
                       points[i].z - points[i+1].z) for i in range(4)]
            # Now the angles...
            angles = [angle(slopes[i], slopes[i+1]) for i in range(4)]
            # And the distances... (excluding the 3rd distance)
            distances = [points[i].distance(points[i+1]) for i in range(4)
                         if i != 2]

            # Determine the acceptable range for distances.
            radius_min = (1 - self.tolerance) * candidate['radius']
            radius_max = (1 + self.tolerance) * candidate['radius']

            # Test everything!
            valid_angles = all(a <= self.angle for a in angles)
            valid_distances = all(radius_min <= d <= radius_max
                                  for d in distances)
            valid_3rd = radius_min <= distances[2] / 2.0 <= radius_max

            if valid_angles and valid_distances and valid_3rd:
                # The 5 points appear to form a valid trajectory. Score +1!
                self.trajectories.append(points)
