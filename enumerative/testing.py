from builtins import print

from preprocessing.candidates import CandidateSearch

from itertools import permutations
import numpy as np
import math as m


def angle(v1, v2):
    angles = []
    for c1, c2 in (p for p in permutations(range(3), 2) if p[0] < p[1]):
        u = (v1[c1], v1[c2])
        v = (v2[c1], v2[c2])
        angle_cos = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
        angle_deg = abs(180.0 * np.arccos(angle_cos) / m.pi)
        angles.append(180.0 - angle_deg if angle_deg > 90 else angle_deg)

    return sum(angles) / len(angles)

#auteur matduf
def calcAngleDeg(p1, p2, p3):
    return calcAngleRadXY(p1, p2, p3)/m.pi*180

#auteur matduf
def calcAngleRad(p1, p2, p3):
    return m.acos(((p2.x - p1.x) * (p3.x - p2.x) +
                  (p2.y - p1.y) * (p3.y - p2.y) +
                  (p2.z - p1.z) * (p3.z - p2.z))
           / (p1.distance(p2)*p2.distance(p3)))

def calcAngleRadXY(p1, p2, p3):
    return m.acos(((p2.x - p1.x) * (p3.x - p2.x) + (p2.y - p1.y) * (p3.y - p2.y))
                 / (distanceXY(p1,p2)*distanceXY(p2,p3)))

def distanceXY(p1, p2):
    # 3D shortest distance between two points.
    dx = pow(p1.x - p2.x, 2)
    dy = pow(p1.y - p2.y, 2)
    return m.sqrt(dx + dy)

class SampleTest:
    def __init__(self, pset, tolerance, angle, toleranceZ):
        self.search = CandidateSearch(pset)
        self.tolerance = tolerance
        self.angle = angle
        self.toleranceZ = toleranceZ
        self.trajectories = []

    @property
    def score(self):
        return len(self.trajectories)

    def validate_candidate(self, candidate):
        # Determine the order of the points. Simplest solution is to select
        # the sequence which creates the shortest path when connecting the
        # dots.
        #sequence = min(permutations(candidate.points),
        #               key=lambda p: sum([p[i].distance(p[i+1])
        #                                  for i in range(4)]))
        sequence = candidate.points
        distMoyen = self.distanceMoyenne(sequence)
        zMoyen = self.moyenneEnZ(sequence)
        valide = 1
        i = 0

        maxDist = 2 if distanceXY(sequence[2], sequence[3]) > distanceXY(sequence[1], sequence[2]) else 1

        while valide and i < 5:
            # vérification de la cohérence sur Z
            valide = abs(zMoyen - sequence[i].z) <= self.toleranceZ
            # vérification des distances sur le plan X,Y
            if valide and i < 4:
                if i != maxDist:
                    valide = abs((distMoyen - distanceXY(sequence[i], sequence[i+1]))/distMoyen) <= self.tolerance
                else:
                    valide = abs((distMoyen - distanceXY(sequence[i], sequence[i+1])/2)/distMoyen) <= self.tolerance
            # vérification des angles sur X, Y
            if valide and i < 3:
                valide = calcAngleDeg(sequence[i], sequence[i+1], sequence[i+2]) <= self.angle

            i += 1

        if valide:
            candidate.points = sequence
            return candidate

        # Compute the slopes and the angles.
        #slopes = [(sequence[i+1].x - sequence[i].x,
        #           sequence[i+1].y - sequence[i].y,
        #           sequence[i+1].z - sequence[i].z) for i in range(4)]
        #angles = [angle(slopes[i], slopes[i+1]) for i in range(3)]

        #distances = []
        #for i in range(4):
        #    new_distance = sequence[i].distance(sequence[i+1])
        #    distances.append(new_distance / 2.0 if i == 2 else new_distance)

        #distance_max = candidate.radius * (1 + self.tolerance)
        #valid_angles = all(a <= self.angle for a in angles)
        #valid_distances = all(d <= distance_max for d in distances)

        #if valid_angles and valid_distances:
        #    candidate.points = sequence
        #    return candidate

        return None

    def distanceMoyenne(self,sequence):
        moyenne = 0
        for i in range(4):
            moyenne+=distanceXY(sequence[i], sequence[i+1])
        return moyenne/5

    def moyenneEnZ(self,sequence):
        moyenne = 0
        for i in range(5):
            moyenne+=sequence[i].z
        return moyenne/5

    def perform(self):
        for candidate in self.search.iterate():
            validation = self.validate_candidate(candidate)
            if validation is not None:
                print(validation)
                #self.search.report_positive(candidate)
                self.trajectories.append(validation)

