import tkinter as tk
import os
import traceback
from gui.plot import GUI
from preprocessing.datamodel import PointSet
from preprocessing.candidates import CandidateSearch
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
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
        self.trajectories = []
        self.bad_trajectories = []
        self.point_set = None
        self.file = None

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

        self.process_auto = Button(self.master, text="Recherche automatique", command=self.process_file)
        self.process_auto.grid(row=3, sticky=W + E)

        self.process_manual = Button(self.master, text="Recherche manuelle",
                                     command=self.process_file_m)
        self.process_manual.grid(row=3, column=1, sticky=W + E)

    def update_results_widgets(self):
        """
        S'appuie sur le GUI afin d'afficher les informations des bulles, ainsi que divers contrôles.
        """

        ttk.Separator(self.master).grid(row=4, columnspan=2, sticky=E + W)
        Label(self.master, text="{} bulles chargées\n{} trajectoires trouvées"
              .format(len(self.gui.bubbles) + len(self.gui.special_bubbles), len(self.gui.trajectories)), pady=5)\
            .grid(row=5, columnspan=2, sticky=W)
        Button(self.master, text="Afficher les trajectoires", command=self.gui.display_traj)\
            .grid(row=6, column=0, sticky=W+E)
        Button(self.master, text="Cacher les trajectoires", command=self.gui.hide_traj)\
            .grid(row=6, column=1, sticky=W+E)
        Button(self.master, text="Exporter les trajectoires", command=self.export)\
            .grid(row=7, columnspan=2, sticky=W+E)

    def load_file(self):
        """
        Charge un fichier de données afin de démarrer le plot
        """

        fname = askopenfilename(filetypes=(("Fichiers de résultats", "*.txt"),
                                           ("All files", "*.*")))
        if fname:
            self.file = fname
        return

    def process_file_m(self):
        self.process_file(manual_mode=True)

    def process_file(self, find_trajectories=True, manual_mode=False):
        try:
            if self.file is None:
                raise ValueError("Aucun fichier chargé.")

            self.pointSet = PointSet(self.file)
            bubbles = [temp.raw() for temp in self.pointSet.points]
            self.loaded_file.config(text="Fichier chargé : {}".format(os.path.basename(str(self.file))))

            self.gui.set_bubbles(bubbles)

            if find_trajectories:
                # TODO: Soumettre les données du fichier à la reconnaissance des trajectoires
                print("Trajectoires à définir..")
                # self.gui.set_trajectories(trajectories)

            # TODO: Afficher les deux listes de données précédentes dans le matplot3d

            self.update_results_widgets()

            showinfo("Ouverture de fichier", "Fichier chargé avec succès !")

            self.gui.display()

            if manual_mode:
                self.manual_mode()

        except ValueError as ve:
            showerror("Ouverture de fichier", ve)
        except Exception as e:
            print(e)
            showerror("Ouverture de fichier", "Erreur lors de l'ouverture du fichier.")
            traceback.print_exc()
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

    def export(self):
        def save_file(to_save):
            f = asksaveasfile(mode='w', defaultextension=".txt")
            if f is None:  # En cas d'annulation
                return

            save = []
            for candidate in to_save:
                save.append(' '.join([point.p_id for point in candidate.points]))

            text2save = '\n'.join(save)
            f.write(text2save)
            f.close()

        try:
            if self.trajectories:
                showinfo("Exportation", "Choisissez où sauvegarder")
                save_file(self.trajectories)
            if self.bad_trajectories:
                showinfo("Exportation", "Choisissez où sauvegarder")
                save_file(self.bad_trajectories)
        except:
            showerror("Exportation", "Erreur lors de l'écriture du fichier.")

    def manual_mode(self):
        # On réinitialise les trajectoires connues
        del self.trajectories[:]
        del self.bad_trajectories[:]

        cs = CandidateSearch(pset=self.pointSet)

        for trajectory in cs.iterate():
            self.gui.hide_traj()
            self.gui.unspecialize_bubbles()
            self.gui.add_trajectories(trajectory.raw())
            print(self.gui.trajectories)
            self.gui.display_traj()

            if messagebox.askyesno("Analyse des trajectoires", "Est-ce une trajectoire valide ?", icon=messagebox.QUESTION):
                self.trajectories.append(trajectory)
            else:
                self.bad_trajectories.append(trajectory)

        showinfo("Analyse des trajectoires", "Analyse terminée !")


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

