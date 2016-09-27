import pylab as p
import mpl_toolkits.mplot3d.axes3d as p3

fig=p.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter([1], [0], [0], c='r', marker='^', picker=5)
ax.scatter([0], [1], [0], c='g', marker='^', picker=5)
ax.scatter([0], [0], [1], c='b', marker='^', picker=5)

