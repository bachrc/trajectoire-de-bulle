import pylab as p
import mpl_toolkits.mplot3d.axes3d as p3
from random import randint


class GUI:

    def __init__(self, bubbles=[], trajectories=[], special_bubbles=[]):
        """
        Méthode instanciant un affichage pour tous les points et trajectoires passés en paramètre.

        :param bubbles: Liste de toutes les coordonnées de bulles sous forme de tuples (x, y, z).
        :param trajectories: Liste des tuples contenant les 5 tuples de coordonnées des points à atteindre.
        """
        self.bubbles = bubbles
        self.special_bubbles = special_bubbles
        self.trajectories = trajectories

        self.fig = p.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

        self.normal_scatter = self.ax.scatter([], [], [], c='b', marker='o', picker=5)
        self.special_scatter = self.ax.scatter([], [], [], c='r', marker='o', picker=5)

    def add_special_bubbles(self, new_special_bubbles):
        """
        Enlève les bulles du scatter normal pour les mettre dans le scatter spécial.

        :param bubbles: Coordonnées des bulles à ajouter/déplacer.
        """

        # Suppression des doublons
        new_special_bubbles = [temp for temp in new_special_bubbles if temp not in self.special_bubbles]

        # Suppression des bulles normales, pour les rendre spéciales.
        self.bubbles = [temp for temp in self.bubbles if temp not in new_special_bubbles]

        self.special_bubbles.extend(new_special_bubbles)

    def unspecialize_bubbles(self):
        """
        Rend normales toutes les bulles spéciales.
        :return:
        """

        self.bubbles.extend(self.special_bubbles)
        del self.special_bubbles[:]

    def add_trajectories(self, trajectory, refresh=False):
        self.trajectories.extend(trajectory)
        if refresh:
            p.draw()

    def add_bubbles(self, bubble, refresh=False):
        self.bubbles.extend(bubble)
        if refresh:
            p.draw()

    def set_bubbles(self, new_bubbles):
        self.bubbles = new_bubbles

    def set_trajectories(self, new_trajectories):
        self.trajectories = new_trajectories

    def update_scatters(self):
        self.normal_scatter.remove()
        self.special_scatter.remove()

        self.normal_scatter = self.ax.scatter([bubbleTemp[0] for bubbleTemp in self.bubbles],
                                              [bubbleTemp[1] for bubbleTemp in self.bubbles],
                                              [bubbleTemp[2] for bubbleTemp in self.bubbles],
                                              c='b', marker='o', picker=5)

        print(self.special_bubbles)

        self.special_scatter = self.ax.scatter([bubbleTemp[0] for bubbleTemp in self.special_bubbles],
                                               [bubbleTemp[1] for bubbleTemp in self.special_bubbles],
                                               [bubbleTemp[2] for bubbleTemp in self.special_bubbles],
                                               c='r', marker='o', picker=5)

    def hide_traj(self):
        del self.ax.lines[:]
        p.draw()

    def display_traj(self):
        del self.ax.lines[:]
        for temp in self.trajectories:
            lines = []
            for i in range(4):
                lines.append(self.ax.plot([temp[i][0], temp[i+1][0]],
                                          [temp[i][1], temp[i+1][1]],
                                          zs=[temp[i][2], temp[i+1][2]]))

            color = '%06X' % randint(0, 0xFFFFFF)
            p.setp(lines, color="#" + color)

        p.draw()

    def display(self):
        """
        Méthode affichant les points restés en mémoire.

        """
        self.update_scatters()
        self.fig.canvas.mpl_connect('pick_event', self.onpick)

        p.show()

    def close_all(self):
        """
        Méthode fermant toutes les instances de plot en cours.
        """
        p.close('all')

    def onpick(self, event):
        ind = event.ind[0]
        x, y, z = event.artist._offsets3d

        trajectories = [coordinates for coordinates in self.trajectories if (x[ind], y[ind], z[ind]) in coordinates]

        del self.ax.lines[:]

        if len(trajectories) > 0:
            for i in range(4):
                self.ax.plot([trajectories[0][i][0], trajectories[0][i+1][0]],
                             [trajectories[0][i][1], trajectories[0][i+1][1]],
                             zs=[trajectories[0][i][2], trajectories[0][i+1][2]])

        # print(self.ax.lines)
        p.setp(self.ax.lines, color='b')
        p.draw()

        # print(x[ind], y[ind], z[ind])


if __name__ == '__main__':

    bubbles = [(0, 0, 1), (1, 0, 0), (0, 2, 1), (1, 3, 0), (2, 0, 1), (3, 2, 1), (1, 2, 3), (0, 0, 0)]
    trajectories = [((0, 0, 1), (0, 2, 1), (2, 0, 1), (1, 2, 3), (3, 2, 1)),
                    ((1, 3, 0), (2, 0, 1), (3, 2, 1), (1, 2, 3), (0, 0, 0))]

    gui = GUI(bubbles, trajectories)
    gui.add_special_bubbles([(0, 2, 1), (1, 3, 0)])
    gui.display()
