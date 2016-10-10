from preprocessing.candidates import Candidate

from collections import deque
from math import sqrt


class Point:
    """
    A simple point class (x, y, z). Each point also has a unique numerical ID.
    """

    def __init__(self, p_id, x, y, z):
        self.p_id = p_id
        self.x, self.y, self.z = x, y, z

    def __hash__(self):
        return self.p_id

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self):
        return "(%f, %f, %f)" % (self.x, self.y, self.z)

    def raw(self):
        """
        Bypasses the class representation and returns a coordinate tuple.
        :return: An (x, y, z) tuple.
        """
        return tuple((self.x, self.y, self.z))

    def distance(self, point):
        """
        Returns the distance between self and point.
        :param point: The remote point.
        :return: The distance, as a real number.
        """
        dx = pow(self.x - point.x, 2)
        dy = pow(self.y - point.y, 2)
        dz = pow(self.z - point.z, 2)
        return sqrt(dx + dy + dz)

    def distance_to_line(self, p1, p2):
        """
        Point-to-line distance using a projection of the target point onto the
        line. Useful when trying to keep points around an axis.
        :param p1: A point on the remote line.
        :param p2: Another point on the remote line.
        :return: The projected distance to the (p1, p2) line.
        """
        l2 = pow(p1.x - p2.x, 2) + pow(p1.y - p2.y, 2) + pow(p1.z - p2.z, 2)
        l2 = sqrt(l2)

        if l2 == 0:
            # Already got the projection, we're done.
            return self.distance(p1)

        # Compute the adjustment needed to make a projection from p1 and p2.
        t = (self.x - p1.x) * (p2.x - p1.x)
        t += (self.y - p1.y) * (p2.y - p1.y)
        t += (self.z - p1.z) * (p2.z - p1.z)
        t = max(0, min(1, t / l2))

        projection = Point(0, p1.x + t * (p2.x - p1.x),
                           p1.y + t * (p2.y - p1.y),
                           p1.z + t * (p2.z - p1.z))
        return self.distance(projection)


class PointSet:
    """
    A set of Point instances, parsed from a data file.
    """

    def __init__(self, filename=None):
        """
        Initialises a point set.
        :param filename: The coordinates data file. A Point's ID will be its
        position (line number) in the file. Makes lookups easier from
        LearningSet.
        """
        self.points = deque()
        self.ids = {}
        next_id = 1

        if filename is not None:
            with open(filename) as resource:
                for line in resource:
                    x, y, z = [float(s) for s in line.strip().split()[:3]]
                    point = Point(next_id, x, y, z)
                    self.ids[next_id] = point
                    self.points.append(point)
                    next_id += 1

    def copy(self):
        """
        Returns a shallow copy of the PointSet.
        :return: A PointSet instance.
        """
        pcopy = PointSet()
        for point in self.points:
            pcopy.ids[point.p_id] = point
            pcopy.points.append(point)
        return pcopy

    def size(self):
        """
        Returns the number of points in the set.
        :return: The set's size (integer).
        """
        return len(self.points)

    def push_back(self, point):
        """
        Adds a point to the set. This is used by CandidateSearch to bring points
        back into a copy's set.
        :param point: The new point, coming back into the set.
        """
        if point.p_id not in self.ids:
            self.ids[point.p_id] = point
            self.points.append(point)

    def remove(self, point):
        """
        Removes a point from the set.
        :param point: The point to be removed.
        """
        if point.p_id not in self.ids:
            return

        del self.ids[point.p_id]
        self.points.remove(point)

    def get_by_id(self, point_id):
        """
        Retrieves a Point instance based on its ID. Used by LearningSet to match
        Point IDs in trajectory files to PointSet points.
        :param point_id: A point ID.
        :return: The Point instance.
        """
        try:
            return self.ids[point_id]
        except KeyError:
            return None

    def pop_iterate(self):
        """
        Pops a Point from the PointSet. Used by CandidateSearch.
        :return: The first Point in the set. Don't make assumptions about the
        order.
        """
        while len(self.points) > 0:
            point = self.points.popleft()
            del self.ids[point.p_id]
            yield point

    def nearest(self, ref):
        """
        Returns the Point nearest to a given reference Point.
        :param ref: The reference Point.
        :return: The nearest Point.
        """
        try:
            return min((p for p in self.points if p != ref),
                       key=lambda p: p.distance(ref))
        except ValueError:
            return None

    def neighbours(self, ref, radius):
        """
        Returns a Point instance in the given radius of a reference Point.
        :param ref: The reference Point.
        :param radius: The search radius.
        :return: A Point instance in the reference's neighbour. Use this method
        as a generator to get all of them.
        """
        for point in (p for p in self.points if p != ref):
            if abs(point.x - ref.x) <= radius and \
               abs(point.y - ref.y) <= radius and \
               abs(point.z - ref.z) <= radius:
                yield point


class LearningSet:
    """
    Parses a trajectory files and matches the point IDs to Point instances in a
    given PointSet.
    """

    def __init__(self, pset, trajectory_file):
        """
        Initialises the LearningSet.
        :param pset: The associated PointSet.
        :param trajectory_file: The trajectory file name.
        """
        self.pset = pset
        self.trajectory_file = trajectory_file

    def iterate(self, raw_smooth=False):
        """
        Generates positive candidates.
        :param raw_smooth: Set to True if you want the Candidate's raw() forms.
        :return: A positive candidate from the file. Use as a generator.
        """
        with open(self.trajectory_file) as resource:
            for line in resource:
                point_ids = [int(i) for i in line.strip().split()]
                trajectory = [self.pset.get_by_id(i) for i in point_ids]

                if any(p is None for p in trajectory):
                    # Bogus trajectory: some points are still unreferenced.
                    continue

                # Candidate instances come with a radius value. Since this
                # candidate doesn't actually come from a search, we'll compute
                # a theoretical search radius by averaging the distances. We'll
                # allow a factor of 2 to account for the 3-4 distance (doubled).
                dists = [trajectory[i].distance(trajectory[i+1])
                         for i in range(4)]
                d_max = max(dists)
                dists = [d_max / 2.0 if d == d_max else d for d in dists]

                candidate = Candidate(trajectory, max(dists))
                candidate.to_standard_order()

                yield candidate.raw(True) if raw_smooth else candidate
