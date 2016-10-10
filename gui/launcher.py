import tkinter as tk
import os
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets(master)

    def create_widgets(self, master):
        Label(master, text="Trajectoires de bulles", font=("fixedsys", 17))\
            .grid(row=0, sticky=W+N+E, columnspan=2, padx=15, pady=15)

        self.load = Button(master, text="Parcourir", command=self.load_file)
        self.load.grid(row=1, column=0, sticky=W+E)

        self.loaded_file = Label(master, text="Aucun fichier chargé.")
        self.loaded_file.grid(row=1, column=1)

    def load_file(self):
        fname = askopenfilename(filetypes=(("Fichiers de résultats", "*.txt"),
                                           ("All files", "*.*")))
        if fname:
            try:
                print("Fichier ouvert : " + fname)
                # TODO: Charger les données du fichier
                # TODO: Soumettre les données du fichier à la reconnaissance des trajectoires
                # TODO: Afficher les deux listes de données précédentes dans le matplot3d
                self.loaded_file.config(text="Fichier chargé : {}".format(os.path.basename(str(fname))))
                showinfo("Ouverture de fichier", "Fichier chargé avec succès !")
            except Exception as e:  # <- naked except is a bad idea
                print(e)
                showerror("Ouverture de fichier", "Erreur lors de l'ouverture du fichier\n{} : {}".format(fname, e))
            return


def launch_gui():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
