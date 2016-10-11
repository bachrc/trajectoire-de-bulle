import neurolab as nl


class NeuralNetwork:
    vrais = [1]
    faux = [0]
    nbNeuroneEntree = 15

    def __init__(self, matrice_input: list = None, matrice_output: list = None):
        """
        Ce constructeur entrainera le réseau en plus de le créer. Ne l'utilisez
        que si vous êtes sur que vous ne possèdez pas déjà un réseau dans un
        fichier.
        :param matrice_input: Matrice dont chaque ligne est une trajectoire à
        tester.
        :param matrice_output: Vecteur dont chaque valeur est une sortie
        attendue.
        """

        if matrice_input is None and matrice_output is None:
            self.network = nl.load('network.net')
        elif matrice_input is not None and matrice_output is not None:
            self.init_reseau(matrice_input, matrice_output)
        else:
            raise ValueError("Les matrices d'entrée et de sortie doivent être "
                             "soit renseignées, soit absentes toutes les deux.")

    def init_reseau(self, matrice_input: list, matrice_output: list):
        """
        Méthode initiant le réseau de neurone à partir d'une pool de base. Il
        faut passer une matrice ou chaque ligne est une trajectoire a tester. Le
        vecteur output doit contenir les sorties attendus pour chaque ligne. A
        chaque ligne de la matrice doit correspondre une valeur de sorties.

        Le réseau est sauvegardé dans le fichier network.net.

        :param matrice_input: Matrice dont chaque ligne est une trajectoire à
        tester.
        :param matrice_output: Vecteur dont chaque valeur est une sortie
        attendue.
        """
        max_input = max([max(l) for l in matrice_input])
        min_input = min([min(l) for l in matrice_input])

        mat_neurone_entree = [[min_input, max_input]]
        mat_neurone_entree *= NeuralNetwork.nbNeuroneEntree

        nb_neurone_cachee = len(mat_neurone_entree)
        nb_neurone_sortie = 1

        net = nl.net.newff(mat_neurone_entree, [nb_neurone_cachee,
                                                nb_neurone_sortie])
        net.train(matrice_input, matrice_output, epochs=100000, goal=0.0001)
        net.save('network.net')

        self.network = net

    def use_reseau(self, test_vector: list):
        """
        :param test_vector: Un ensemble de points qui peut être une
        trajectoire. On cherche à tester si c'est bien le cas.
        :return: La valeur de retour du réseau.
        """
        return self.network.sim([test_vector])
