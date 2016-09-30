from reseau_neuronal.network import Network
from reseau_neuronal.reseau_neural import NeuralNetwork
from preprocessing.datamodel import LearningSet,PointSet
from glob import glob



class TestNetwork:
    def __init__(self):

        #tab_learning_set = []
        #datafiles = glob('./datasets/points/norma_*.txt')
        #for filename in datafiles:
        #   print(filename)
        #   basename = filename[filename.rindex('/') + 1:-4]
        #   tra_file = "./datasets/trajectories/%s_tra.txt" % basename

        #   pset = PointSet(filename)
        #   lset = LearningSet(pset=pset, trajectory_file=tra_file)
        #   tab_learning_set.append(lset)

        #net = Network(tab_learning_set)
        net = Network()
        print("valid")
        output_mean_valid   = net.perform_all_verification(PointSet("./datasets/points/valid_sample.txt"))
        print("invalid")
        output_mean_invalid = net.perform_all_verification(PointSet("./datasets/points/pas_valid_sample.txt"))

test = TestNetwork()