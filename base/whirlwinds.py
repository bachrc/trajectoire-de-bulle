from testing import SampleTest
from parser import PointSet
from glob import glob

if __name__ == '__main__':
    for filename in glob('data/points/norma_*.txt'):
        tests = {}
        points = PointSet(filename)

        for tolerance in range(5, 25, 5):
            for angle in reversed(range(10, 50, 5)):
                test = SampleTest(points, tolerance, angle)
                test.perform()

                if tolerance not in tests:
                    tests[tolerance] = {}

                tests[tolerance][angle] = test

        best_keys = max([(t, a) for t in tests for a in tests[t]],
                        key=lambda p: tests[p[0]][p[1]].score)
        best = tests[best_keys[0]][best_keys[1]]

        print("%d points, best tolerance is %d%%, best angle is %d°." % (
            points.size, best.tolerance, best.angle))
