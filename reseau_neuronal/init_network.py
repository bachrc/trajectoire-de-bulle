from reseau_neuronal.network import Network
from preprocessing.datamodel import LearningSet, PointSet
from glob import glob


class InitNetwork:

    def __init__(self, need_to_train, file):
        """
        Permet d'initialiser un réseau et de l'entrainer sur tout nos fichier
        de données. Il est également possible de lire le fichier décrivant le
        réseau à utiliser.
        :param need_to_train: True si l'on veut recrée le réseau à partir des
        fichier de données
        """

        self.file = file

        if need_to_train:
            # Chaque tableau contiendra les LearningSet qui
            # serviront à entrainer le réseau
            tab_learning_set_true = []
            tab_learning_set_false = []

            # Lecture des fichiers
            datafiles = glob(file+'/points/norma_*.txt')

            for filename in datafiles:
                print(filename)
                basename = filename[filename.rindex('/') + 1:-4]
                tra_file_true = (file+"/trajectories/%s_tra.txt") \
                                % basename
                tra_file_false = (file+"/trajectories/%s_tra_false.txt") \
                                 % basename

                # On créer l'ensemble des points à partir
                # du fichier puis on initialise les LearningSet
                pset = PointSet(filename)
                lset_true = LearningSet(pset=pset,
                                        trajectory_file=tra_file_true)
                lset_false = LearningSet(pset=pset,
                                         trajectory_file=tra_file_false)
                tab_learning_set_true.append(lset_true)
                tab_learning_set_false.append(lset_false)

            # On initialise le réseau avec les deux learning_set
            self.net = Network(tab_learning_set_true, tab_learning_set_false)
        else:
            # On initalise le réseau avec le fichier network.net
            self.net = Network()

    def getResult(self):
        return self.net.perform_all_verification(PointSet(self.file))
