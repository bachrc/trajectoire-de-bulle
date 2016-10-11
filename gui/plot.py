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
        """

        self.bubbles.extend(self.special_bubbles)
        del self.special_bubbles[:]

    def add_trajectories(self, trajectory, refresh=False):
        """
        Ajoute les trajectoires à la liste des trajectoires normales

        :param trajectory: Liste de trajectoires à ajouter
        :param refresh: Booléen spécifiant s'il faut actualiser le panel
        """

        self.trajectories.extend(trajectory)
        if refresh:
            p.draw()

    def add_bubbles(self, bubble, refresh=False):
        """
        Ajoute les bulles à la liste des trajectoires normales

        :param bubble: Liste de bulles à ajouter
        :param refresh: Booléen spécifiant s'il faut actualiser le panel
        """

        self.bubbles.extend(bubble)
        if refresh:
            p.draw()

    def set_bubbles(self, new_bubbles):
        """
        Setter des bulles

        :param new_bubbles: Les bulles remplaçantes
        """

        self.bubbles = new_bubbles

    def set_trajectories(self, new_trajectories):
        """
        Setter des trajectoires

        :param new_trajectories: Les trajectoires remplaçantes
        """

        self.trajectories = new_trajectories

    def update_scatters(self):
        """
        Met à jour les affichages de points, en fonction des points en mémoires.
        Il y a ici deux affichages :
        - Un affichage bleu pour les points normaux
        - Un affichage route pour les points spéciaux à faire ressortir
        """

        self.normal_scatter.remove()
        self.special_scatter.remove()

        self.normal_scatter = self.ax.scatter([bubbleTemp[0] for bubbleTemp in self.bubbles],
                                              [bubbleTemp[1] for bubbleTemp in self.bubbles],
                                              [bubbleTemp[2] for bubbleTemp in self.bubbles],
                                              c='b', marker='o', picker=5)

        self.special_scatter = self.ax.scatter([bubbleTemp[0] for bubbleTemp in self.special_bubbles],
                                               [bubbleTemp[1] for bubbleTemp in self.special_bubbles],
                                               [bubbleTemp[2] for bubbleTemp in self.special_bubbles],
                                               c='r', marker='o', picker=5)

    def hide_traj(self):
        """
        Méthode supprimant toutes les trajectoires à l'écran
        """

        del self.ax.lines[:]
        p.draw()

    def display_traj(self):
        """
        Affiche dans une couleur différente chaque trajectoire en mémoire dans le plot.
        """

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
        # FIXME: Empêcher la fermeture du plot
        # self.fig.canvas.mpl_connect('close_event', lambda: False)

        p.show()

    def close_all(self):
        """
        Méthode fermant toutes les instances de plot en cours.
        """

        p.close('all')

    def onpick(self, event):
        """
        Méthode appelée lors de la sélection d'une bulle, trace la (les ?) trajectoires comprenant la
        bulle sélectionnée.
        """

        ind = event.ind[0]
        x, y, z = event.artist._offsets3d

        trajectories = [coordinates for coordinates in self.trajectories if (x[ind], y[ind], z[ind]) in coordinates]

        del self.ax.lines[:]

        if len(trajectories) > 0:
            for i in range(4):
                self.ax.plot([trajectories[0][i][0], trajectories[0][i+1][0]],
                             [trajectories[0][i][1], trajectories[0][i+1][1]],
                             zs=[trajectories[0][i][2], trajectories[0][i+1][2]])

        p.setp(self.ax.lines, color='b')
        p.draw()
