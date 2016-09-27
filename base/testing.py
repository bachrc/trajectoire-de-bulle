import numpy as np
import math as m


def angle(v1, v2):
    v1 /= np.linalg.norm(v1)
    v2 /= np.linalg.norm(v2)
    angle_rad = np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))
    angle_deg = 180.0 * angle_rad / m.pi
    return angle_deg if angle_deg < 90 else 180 - angle_deg


class SampleTest:
    def __init__(self, pset, tolerance, angle):
        self.pset = pset
        self.tolerance = tolerance
        self.angle = angle
        self.trajectories = []

    @property
    def score(self):
        return len(self.trajectories)

    def perform(self, candidates):
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

            # First, let's determine the planes in which the trajectory is
            # perceptible.
            orientations = {}
            if all(np.sign(d) == np.sign(dxs[0]) for d in dxs[1:]):
                # Trajectory has an x-axis orientation.
                orientations['x'] = sorted(points, key=lambda p: p.x)
            if all(np.sign(d) == np.sign(dys[0]) for d in dys[1:]):
                # Trajectory has a y-axis orientation.
                orientations['y'] = sorted(points, key=lambda p: p.y)
            if all(np.sign(d) == np.sign(dzs[0]) for d in dzs[1:]):
                # Trajectory has a z-axis orientation.
                orientations['z'] = sorted(points, key=lambda p: p.z)

            # Determine which planes we have to check.
            axes = list(orientations.keys())
            plane_checks = [(axes[i], axes[j])
                            for i in range(len(axes))
                            for j in range(i, len(axes))
                            if axes[i] != axes[j]]

            # With the points in a consecutive order, we can compute the slopes
            # and angles in each plane.
            angles = []
            distances = []

            for a1, a2 in plane_checks:
                slopes = []
                for i in range(4):
                    p1 = {'x': orientations[a1][i].x,
                          'y': orientations[a1][i].y,
                          'z': orientations[a1][i].z}
                    p2 = {'x': orientations[a1][i+1].x,
                          'y': orientations[a1][i+1].y,
                          'z': orientations[a1][i+1].z}

                    slopes.append((p1[a1] - p2[a1], p1[a2] - p2[a2]))

                angles += [angle(slopes[i], slopes[i+1]) for i in range(3)]
                for plane in a1, a2:
                    for i in range(4):
                        p1 = orientations[plane][i]
                        p2 = orientations[plane][i+1]
                        d = p1.distance(p2)
                        distances.append(d if i != 2 else d / 2.0)

            # Determine the acceptable range for distances.
            distance_max = (1 + self.tolerance) * candidate['radius']

            # Test everything!
            valid_angles = all(a <= self.angle for a in angles)
            valid_distances = all(d <= distance_max for d in distances)

            if valid_angles and valid_distances:
                # The 5 points appear to form a valid trajectory. Score +1!
                self.trajectories.append(points)
