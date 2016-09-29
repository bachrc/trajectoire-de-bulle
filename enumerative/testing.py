import numpy as np
import math as m
from itertools import permutations

from preprocessing.candidates import CandidateSearch


def angle(v1, v2):
    # TODO: not sure this is the angle we're interested in. Try a projection?
    v1 /= np.linalg.norm(v1)
    v2 /= np.linalg.norm(v2)
    return 180.0 * np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0)) / m.pi


class SampleTest:
    def __init__(self, pset, tolerance, angle):
        self.search = CandidateSearch(pset)
        self.tolerance = tolerance
        self.angle = angle
        self.trajectories = []

    @property
    def score(self):
        return len(self.trajectories)

    def validate_candidate(self, candidate):
        # Determine the order of the points. Simplest solution is to select
        # the sequence which creates the shortest path when connecting the
        # dots.
        sequence = min(permutations(candidate.points),
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

        distance_max = candidate.radius * (1 + self.tolerance)
        valid_angles = all(a <= self.angle for a in angles)
        valid_distances = all(d <= distance_max for d in distances)

        if valid_angles and valid_distances:
            candidate.points = sequence
            return candidate

        return None

    def perform(self):
        for candidate in self.search.iterate():
            validation = self.validate_candidate(candidate)
            if validation is not None:
                self.search.report_positive(candidate)
                self.trajectories.append(validation)
