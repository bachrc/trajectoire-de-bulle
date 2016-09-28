import neurolab as nl


class NeuralNetwork():

    def __init__(self):
        """
        N'utiliser ce constructeur que si vous êtes sur qu'il existe un fichier
        contenant le réseau
        """
        self.network = nl.load('network.net')

    def __init__(self, matrice_input: list, vector_output: list):
        """
        Ce constructeur entrainera le réseau en plus de le crée. Ne l'utilisez que si vous êtes sur
        que vosu ne possèdez pas déjà un réseau dans un fichier.
        :param matrice_input: Matrice dont chaque ligne est une trajectoire à tester
        :param vector_output: Vecteur dont chaque valeur est une sortie attendus
        """
        self.init_reseau(matrice_input, vector_output)

    def init_reseau(self, matrice_input: list, vector_output: list):
        """
        Méthode initiant le réseau de neurone à partir d'un
        pool de base. Il faut passer une matrice ou chaque ligne est
        une trajectoire a tester. Le vecteur output doit contenir les
        sorties attendus pour chaque ligne. A chaque ligne de la matrice doit
        correspondre une valeur de sorties.

        Le réseau est sauvegardé dans le fichier network.net
        :param matrice_input: Matrice dont chaque ligne est une trajectoire à tester
        :param vector_output: Vecteur dont chaque valeur est une sortie attendus
        pour le réseau pour la ligne correspondante
        :return: Rien
        """
        max_input=max([max(l) for l in matrice_input])
        min_input=min([min(l) for l in matrice_input])

        net = nl.net.newff([[min_input, max_input]*15], [100, 2])
        net.train(matrice_input, vector_output)
        net.save('network.net')

        self.network = net

    def use_reseau(self, vector_groupeToTest: list):
        """
        :param vector_groupeToTest: Un ensemble de point qui peut être une
        trajectoire. On cherche à tester si c'est bien le cas.
        :return: La valeur de retour du réseau
        """
        return self.network.sim(vector_groupeToTest)
