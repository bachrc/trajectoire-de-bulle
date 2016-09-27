class Point:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z


class TrajectoryNode:
    SEARCH_RADIUS = 2

    def __init__(self, point):
        self.point = point
        self.near = []


class TrajectoryTree:
    def __init__(self, points, root):
        self.points = points
        self.root = TrajectoryNode(root)

    def build_trajectory(self):
        return None
