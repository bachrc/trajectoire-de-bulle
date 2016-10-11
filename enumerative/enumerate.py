from preprocessing.datamodel import PointSet
from enumerative.testing import SampleTest

from glob import glob

if __name__ == '__main__':
    datafiles = glob('../datasets/points/norma_*.txt')

    # If you want to run a test on a small (5 points) sample, use this. The
    # points in that file DO FORM a trajectory.
    # datafiles = ["../datasets/points/valid_sample.txt"]

    for filename in datafiles:
        tests = {}
        points = PointSet(filename)

        for tolerance in range(5, 25, 5):
            for angle in reversed(range(10, 50, 5)):
                test = SampleTest(points, tolerance / 100.0, angle)
                test.perform()

                if tolerance not in tests:
                    tests[tolerance] = {}

                tests[tolerance][angle] = test

        best_keys = max([(t, a) for t in tests for a in tests[t]],
                        key=lambda p: tests[p[0]][p[1]].score)
        best = tests[best_keys[0]][best_keys[1]]

        print("%d points, %d trajectories, best tolerance is %d%%, "
              "best angle is %d°." % (points.size(), best.score,
                                      best.tolerance * 100.0, best.angle))
