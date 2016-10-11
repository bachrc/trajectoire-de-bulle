import tkinter as tk
import os
from gui.plot import GUI
from preprocessing.datamodel import PointSet
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo


class Application(tk.Frame):
    def __init__(self, master=None):
        """
        Constructeur du GUI.

        :param master: Le container parent.
        """

        super().__init__(master)
        self.gui = GUI()
        self.create_widgets()

    def create_widgets(self):
        """
        Crée les éléments du GUI primaire.
        """

        Label(self.master, text="Trajectoires de bulles", font=("fixedsys", 17))\
            .grid(row=0, sticky=W+N+E, columnspan=2, padx=15, pady=15)

        ttk.Separator(self.master).grid(row=1, columnspan=2, sticky=E+W)

        self.load = Button(self.master, text="Parcourir", command=self.load_file)
        self.load.grid(row=2, column=0, sticky=W+E)

        self.loaded_file = Label(self.master, text="Aucun fichier chargé.")
        self.loaded_file.grid(row=2, column=1)

    def update_results_widgets(self):
        """
        S'appuie sur le GUI afin d'afficher les informations des bulles, ainsi que divers contrôles.
        """

        ttk.Separator(self.master).grid(row=3, columnspan=2, sticky=E + W)
        Label(self.master, text="{} bulles chargées\n{} trajectoires trouvées"
              .format(len(self.gui.bubbles) + len(self.gui.special_bubbles), len(self.gui.trajectories)), pady=5)\
            .grid(row=4, columnspan=2, sticky=W)
        Button(self.master, text="Afficher les trajectoires", command=self.gui.display_traj)\
            .grid(row=5, column=0, sticky=W+E)
        Button(self.master, text="Cacher les trajectoires", command=self.gui.hide_traj)\
            .grid(row=5, column=1, sticky=W+E)

    def load_file(self):
        """
        Charge un fichier de données afin de démarrer le plot
        """
        fname = askopenfilename(filetypes=(("Fichiers de résultats", "*.txt"),
                                           ("All files", "*.*")))
        if fname:
            try:
                print("Fichier ouvert : " + fname)
                bubbles = [temp.raw() for temp in PointSet(fname).points]
                # TODO: Soumettre les données du fichier à la reconnaissance des trajectoires
                # TODO: Afficher les deux listes de données précédentes dans le matplot3d
                self.loaded_file.config(text="Fichier chargé : {}".format(os.path.basename(str(fname))))

                self.gui.set_bubbles(bubbles)
                # self.gui.set_trajectories(trajectories)
                self.update_results_widgets()

                showinfo("Ouverture de fichier", "Fichier chargé avec succès !")

                self.gui.display()
            except Exception as e:  # <- naked except is a bad idea
                print(e)
                showerror("Ouverture de fichier", "Erreur lors de l'ouverture du fichier {}".format(fname))
            return

    def load_test_values(self):
        """
        Chargement de quelques données de test pour affichage.
        """

        bubbles = [(0, 0, 1), (1, 0, 0), (0, 2, 1), (1, 3, 0), (2, 0, 1), (3, 2, 1), (1, 2, 3), (0, 0, 0)]
        trajectories = [((0, 0, 1), (0, 2, 1), (2, 0, 1), (1, 2, 3), (3, 2, 1)),
                        ((1, 3, 0), (2, 0, 1), (3, 2, 1), (1, 2, 3), (0, 0, 0))]

        self.gui.set_bubbles(bubbles)
        self.gui.set_trajectories(trajectories)
        self.update_results_widgets()
        self.gui.display()


def launch_gui():
    """
    Méthode lançant l'application.
    """

    root = tk.Tk()
    root.wm_title("Trajectoires de bulles")
    app = Application(master=root)

    def on_close():
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter l'application ?"):
            app.gui.close_all()
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    app.mainloop()

