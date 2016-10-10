import tkinter as tk
from tkinter import *


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        #self.pack()
        self.create_widgets(master)

    def create_widgets(self, master):
        Label(master, text="Trajectoires de bulles", font=("fixedsys", 17))\
            .grid(row=0, sticky=W+N+E, columnspan=2, padx=15, pady=15)
        self.load = Button(master, text="Parcourir", command=self.load_file)\
            .grid(row=1, column=0, sticky=W)
        self.loaded_file = Label(master, text="Aucun fichier chargé.")\
            .grid(row=1, column=1, sticky=W+E)

    def load_file(self):
        print("Bonjour")

    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Application(master=root)
app.mainloop()