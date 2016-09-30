import neurolab as nl


class NeuralNetwork:

    vrais = [1, 0]
    faux  = [0, 1]
    nbNeuroneEntree = 15

    def __init__(self, matrice_input: list = None, matrice_output: list = None):
        """
        Ce constructeur entrainera le réseau en plus de le crée. Ne l'utilisez que si vous êtes sur
        que vosu ne possèdez pas déjà un réseau dans un fichier.
        :param matrice_input: Matrice dont chaque ligne est une trajectoire à tester
        :param matrice_output: Vecteur dont chaque valeur est une sortie attendus
        """

        if matrice_input == None and matrice_output == None:
            self.network = nl.load('network.net')

        elif matrice_input != None and matrice_output != None:
            self.init_reseau(matrice_input, matrice_output)

        else:
            raise ValueError('Il est impossible qu\'une matrice soit null et l\'autre non')

    def init_reseau(self, matrice_input: list, matrice_output: list):
        """
        Méthode initiant le réseau de neurone à partir d'un
        pool de base. Il faut passer une matrice ou chaque ligne est
        une trajectoire a tester. Le vecteur output doit contenir les
        sorties attendus pour chaque ligne. A chaque ligne de la matrice doit
        correspondre une valeur de sorties.

        Le réseau est sauvegardé dans le fichier network.net
        :param matrice_input: Matrice dont chaque ligne est une trajectoire à tester
        :param matrice_output: Vecteur dont chaque valeur est une sortie attendus
        pour le réseau pour la ligne correspondante
        :return: Rien
        """
        max_input=max([max(l) for l in matrice_input])
        min_input=min([min(l) for l in matrice_input])

        mat_neurone_entree = [[min_input, max_input]]*15
        nb_neurone_cachee  = 10
        nb_neurone_sortie  = 2

        net = nl.net.newff(mat_neurone_entree, [nb_neurone_cachee, nb_neurone_sortie])
        net.train(matrice_input, matrice_output, epochs=3600)
        net.save('network.net')

        self.network = net

    def use_reseau(self, vector_groupeToTest: list):
        """
        :param vector_groupeToTest: Un ensemble de point qui peut être une
        trajectoire. On cherche à tester si c'est bien le cas.
        :return: La valeur de retour du réseau
        """
        return self.network.sim([vector_groupeToTest])