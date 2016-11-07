from tkinter.filedialog import askdirectory
from reseau_neuronal.init_network import InitNetwork

if __name__ == '__main__':
    choice = input("What do you want to do ? \n1) Choose directory to analyse \n2) Train network\n")
    print("Peek a directory")
    fname = askdirectory(mustexist=True, title="Choose a directory with trajectory and points files")
    InitNetwork(choice, fname)
