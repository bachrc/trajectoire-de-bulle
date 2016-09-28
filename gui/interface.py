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

        self.lines = []

    def add_trajectory(self, trajectory, refresh=False):
        self.trajectories.append(trajectory)
        if refresh:
            p.draw()

    def add_bubbles(self, bubble, refresh=False):
        self.bubbles.append(bubble)
        if refresh:
            p.draw()

    def set_bubbles(self, new_bubbles):
        self.bubbles = new_bubbles

    def set_trajectories(self, new_trajectories):
        self.trajectories = new_trajectories

    def display(self):
        """
        Méthode affichant les points restés en mémoire.

        """

        for bubble in self.bubbles:
            self.ax.scatter([bubble[0]], [bubble[1]], [bubble[2]], c='#0099cc', marker='o', picker=5)

        self.fig.canvas.mpl_connect('pick_event', self.onpick)

        p.show()

    def onpick(self, event):
        ind = event.ind[0]
        x, y, z = event.artist._offsets3d

        trajectories = [coordinates for coordinates in self.trajectories if (x[ind], y[ind], z[ind]) in coordinates]

        del self.ax.lines[:]

        if len(trajectories) > 0:
            for i in range(4):
                self.lines.append(self.ax.plot([trajectories[0][i][0], trajectories[0][i+1][0]],
                                               [trajectories[0][i][1], trajectories[0][i+1][1]],
                                               zs=[trajectories[0][i][2], trajectories[0][i+1][2]]))

        print(self.ax.lines)
        p.draw()

        print(x[ind], y[ind], z[ind])


if __name__ == '__main__':

    bubbles = [(0, 0, 1), (1, 0, 0), (0, 2, 1), (1, 3, 0), (2, 0, 1), (3, 2, 1), (1, 2, 3), (0, 0, 0)]
    trajectories = [((0, 0, 1), (0, 2, 1), (2, 0, 1), (1, 2, 3), (3, 2, 1)),
                    ((1, 3, 0), (2, 0, 1), (3, 2, 1), (1, 2, 3), (0, 0, 0))]

    gui = GUI(bubbles, trajectories)

    gui.display()
