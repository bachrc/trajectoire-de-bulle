from elements import TrajectoryTree
from random import choice


class SampleTest:
    def __init__(self, points, tolerance, angle):
        self.eligible = points.shallow_copy()
        self.tolerance = tolerance
        self.angle = angle
        self.trajectories = []

    def perform(self):
        while len(self.eligible) != 0:
            root = choice(self.eligible)
            builder = TrajectoryTree(root)
            trajectory = builder.build_trajectory()

            if trajectory is not None:
                self.trajectories.append(trajectory)
                for point in trajectory:
                    self.eligible.remove(point)
            else:
                self.eligible.remove(root)

    @property
    def score(self):
        return len(self.trajectories)
