from reseau_neuronal.network import Network
from reseau_neuronal.reseau_neural import NeuralNetwork
from preprocessing.datamodel import LearningSet,PointSet
from glob import glob

import math
import random

class TestNetwork:
    def __init__(self, need_to_train):

        if need_to_train:
            tab_learning_set = []
            datafiles = glob('./datasets/points/norma_*.txt')
            for filename in datafiles:
               print(filename)
               basename = filename[filename.rindex('/') + 1:-4]
               tra_file = "./datasets/trajectories/%s_tra.txt" % basename

               pset = PointSet(filename)
               lset = LearningSet(pset=pset, trajectory_file=tra_file)
               tab_learning_set.append(lset)

            net = Network(tab_learning_set)
        else:
            net = Network()

        print("valid")
        net.verifier_reseau(PointSet("./datasets/points/valid_sample.txt"))
        print("invalid")
        net.verifier_reseau(PointSet("./datasets/points/pas_valid_sample.txt"))


TestNetwork(input("1/ Lire le fichier \n2/ Re-créer le réseau") == "1")
