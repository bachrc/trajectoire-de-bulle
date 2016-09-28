import pylab as p
import mpl_toolkits.mplot3d.axes3d as p3


class GUI:

    def __init__(self, bubbles, trajectories):
        """
        Méthode instanciant un affichage pour tous les points et trajectoires passés en paramètre.

        :param bubbles: Liste de toutes les coordonnées de bulles sous forme de tuples (x, y, z).
        :param trajectories: Liste des tuples contenant les 5 tuples de coordonnées des points à atteindre.
        """
        self.bubbles = bubbles
        self.trajectories = trajectories

        self.fig = p.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

    def display(self):
        """
        Méthode affichant les points restés en mémoire.

        """

        for bubble in self.bubbles:
            self.ax.scatter([bubble[0]], [bubble[1]], [bubble[2]], c='b', marker='o', picker=5)

        self.fig.canvas.mpl_connect('pick_event', self.onpick)

        p.show()

    def onpick(self, event):
        ind = event.ind[0]
        x, y, z = event.artist._offsets3d

        trajectories = [coordinates for coordinates in self.trajectories if (x[ind], y[ind], z[ind]) in coordinates]

        if len(trajectories) > 0:
            for i in range(4):
                self.ax.plot([trajectories[0][i][0], trajectories[0][i+1][0]], [trajectories[0][i][1], trajectories[0][i+1][1]], zs=[trajectories[0][i][2], trajectories[0][i+1][2]])

        p.draw()

        print(x[ind], y[ind], z[ind])


if __name__ == '__main__':
    """
    fig = p.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter([1], [0], [0], c='r', marker='^', picker=5)
    ax.scatter([0], [1], [0], c='g', marker='^', picker=5)
    ax.scatter([0], [0], [1], c='b', marker='^', picker=5)

    ax.plot([1, 0], [0, 1], zs=[0, 0])

    def onpick(event):
        ind = event.ind[0]
        x, y, z = event.artist._offsets3d
        print(x[ind], y[ind], z[ind])

    fig.canvas.mpl_connect('pick_event', onpick)

    p.show()
    """

    bubbles = [(0, 0, 1), (1, 0, 0), (0, 2, 1), (1, 3, 0), (2, 0, 1), (3, 2, 1), (1, 2, 3), (0, 0, 0)]
    trajectories = [((0, 0, 1), (0, 2, 1), (2, 0, 1), (1, 2, 3), (3, 2, 1)),
                    ((1, 3, 0), (2, 0, 1), (3, 2, 1), (1, 2, 3), (0, 0, 0))]

    gui = GUI(bubbles, trajectories)

    gui.display()
