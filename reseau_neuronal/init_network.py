from reseau_neuronal.network import Network
from preprocessing.datamodel import LearningSet, PointSet
from glob import glob


class InitNetwork:
    def __init__(self, need_to_train):
        """
        Permet d'initialiser un réseau et de l'entrainer sur tout nos fichier
        de données. Il est également possible de lire le fichier décrivant le
        réseau à utiliser.
        :param need_to_train: True si l'on veut recrée le réseau à partir des
        fichier de données
        """
        if need_to_train:
            # Chaque tableau contiendra les LearningSet qui
            # serviront à entrainer le réseau
            tab_learning_set_true = []
            tab_learning_set_false = []

            # Lecture des fichiers
            datafiles = glob('./datasets/points/norma_*.txt')

            for filename in datafiles:
                print(filename)
                basename = filename[filename.rindex('/') + 1:-4]
                tra_file_true = "./datasets/trajectories/%s_tra.txt" \
                                % basename
                tra_file_false = "./datasets/trajectories/%s_tra_false.txt" \
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
            net = Network(tab_learning_set_true, tab_learning_set_false)
        else:
            # On initalise le réseau avec le fichier network.net
            net = Network()

        # On teste le réseau
        print("valid")
        net.verifier_reseau(PointSet("./datasets/points/valid_sample.txt"))
        print("invalid")
        net.verifier_reseau(PointSet("./datasets/points/pas_valid_sample.txt"))


InitNetwork(input("1/ Lire le fichier \n2/ Re-créer le réseau\n") != "1")
