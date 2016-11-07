from preprocessing.candidates import CandidateSearch
from preprocessing.datamodel import PointSet
from reseau_neuronal.reseau_neural import NeuralNetwork

import math
import random


class Network:
    """
    Classe permettant de faire le lien entre les différents conteneur de données
    et leur utilisation par le réseau de neurones. Cette classes n'est pas
    nécessaire au fonctionnement du réseau mais elle simplifie beaucoup son
    utilisation
    """
    def __init__(self, train_sets_true: list = None,
                 train_sets_false: list = None):
        """
        Créer un réseau en l'entrainant avec les deux ensemble de LearningSet
        passé en paramètre. Le permier doit décrire les cas positif et le second
        les cas négatif. Il est conseillé que la taille de ces deux ensembles
        soit du même ordre

        :param train_sets_true: Ensemble de LearningSet auquel le réseau doit
        répondre par NeuraLNetwork.vrais
        :param train_sets_false: Ensemble de LearningSet auquel le réseau doit
        répondre par NeuralNetwork.faux
        """

        if train_sets_true is None and train_sets_false is None:
            self.network = NeuralNetwork()
        else:
            # On tranforme la liste de LearningSet en matrice unique
            matrice_input_vrais = [row for train_set in train_sets_true for row
                                   in train_set.iterate(True)]
            matrice_input_faux = [row for train_set in train_sets_false for row
                                  in train_set.iterate(True)]

            # On crée la matrice des sorties attendus
            # en mettant toute les réponses a Vrais
            matrice_output_vrais = [NeuralNetwork.vrais]
            matrice_output_vrais *= len(matrice_input_vrais)

            # On crée une autre matrice de réponse
            # attendus en mettant les réponse à faux
            matrice_output_faux = [NeuralNetwork.faux]
            matrice_output_faux *= len(matrice_input_faux)

            # On crée la matrice complète
            matrice_input = matrice_input_vrais + matrice_input_faux
            matrice_output = matrice_output_vrais + matrice_output_faux

            # On mélange de la même façon les deux matrices
            seed = random.random()
            random.shuffle(matrice_input, lambda: seed)
            random.shuffle(matrice_output, lambda: seed)

            # On créer enfin le réseau
            self.network = NeuralNetwork(matrice_input, matrice_output)

    def perform_all_verification(self, search_set: PointSet):
        """
        Permet de demander la vérifiaction par le réseau d'un ensemble de point
        et de leur candidat associé

        :param search_set: Un PointSet dans lequel on cherchera les candidat
        possible à passer au réseau de neurones
        :return: L'ensemble des candidats retenus
        """

        if search_set is None:
            raise ValueError('Aucun ensemble sur lequel rechercher')
        else:
            search = CandidateSearch(search_set)
            good_candidats = []
            for candidat in search.iterate():
                vector = [coordonnee for point in candidat.points
                          for coordonnee in (point.x, point.y, point.z)]
                output = self.network.use_reseau(vector)
                reponse = [math.ceil(out) for out in output[0]]

                if reponse == NeuralNetwork.vrais:
                    print("Vrais")
                    search.report_positive(candidat)
                    good_candidats.append(candidat)
                elif reponse == NeuralNetwork.faux:
                    print("Faux")
                else:
                    print("Bug")

            return good_candidats

    def verifier_reseau(self, search_set: PointSet = None):
        """
        Permet de tester si le réseau fonctionne bien en lui passant
        un pointSet dans lequel il piochera des candidats. Il faut que l'on
        sache ce que le réseau est censé répondre pour chacun de ces candidats

        :param search_set: L'ensemble dans lequel on vas rechercher
        """
        pts = list(search_set.points)
        fakes = [pts[i:i + 5] for i in
                 range(0, len(search_set.points), 5)]
        flat = [[c for p in fake for c in p.raw()] for fake in
                fakes]

        for candidat in flat:
            output = self.network.use_reseau(candidat)
            reponse = [math.ceil(out) for out in output[0]]

            print("candidat : ", candidat)

            if reponse == NeuralNetwork.vrais:
                print("Vrais")
            elif reponse == NeuralNetwork.faux:
                print("Faux")
            else:
                print("Bug")
