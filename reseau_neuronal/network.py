from preprocessing.candidates      import CandidateSearch
from preprocessing.datamodel       import LearningSet, PointSet
from reseau_neuronal.reseau_neural import NeuralNetwork

import math
import random


class Network:
    def __init__(self, train_sets: list = None, search_set: PointSet = None):
        self.search  = search_set

        if train_sets is None:
            self.network = NeuralNetwork()
        else:
            #On tranforme la liste de LearningSet en matrice unique
            matrice_input_vrais = []
            for train_set in train_sets:
                for candidat in train_set.iterate():
                    row = [coordonnee for point in candidat.points
                           for coordonnee in (point.x, point.y, point.z)]
                    matrice_input_vrais.append(row)

            max_input = max([max(l) for l in matrice_input_vrais])
            min_input = min([min(l) for l in matrice_input_vrais])

            #On crée la matrice des sorties attendus en mettant toute les réponses a Vrais
            matrice_output_vrais = [NeuralNetwork.vrais] * len(matrice_input_vrais)

            #On ajoute un ensemble de candidat que l'on estime faux
            #matrice_input_faux = [[random.gauss(min_input, max_input) for _ in range(NeuralNetwork.nbNeuroneEntree)] for _ in range(len(matrice_input_vrais))]
            #TODO lire le fichier false.net dans trajectories (JPK doit gérer ça demain matin normalement, on le tape sinon)


            #On crée une autre matrice de réponse attendus en mettant les réponse à faux
            matrice_output_faux = [NeuralNetwork.faux] * len(matrice_input_faux)

            #On crée la matrice complète
            matrice_input  = matrice_input_vrais + matrice_input_faux
            matrice_output = matrice_output_vrais + matrice_output_faux

            #On mélange de la même façon les deux matrices
            seed = random.random()
            random.shuffle(matrice_input, lambda: seed)
            random.shuffle(matrice_output, lambda: seed)

            #with open("datasets/trajectories/false.net","w") as out:
             #   for ligne in matrice_input_faux:
              #      ligne_wo = [ligne[i:i + 3] for i in range(0, len(ligne), 3)]
               #     for wo in ligne_wo:
                #        out.write(" ".join(str(w) for w in wo) + "\n")



            #On créer enfin le réseau
            #self.network = NeuralNetwork(matrice_input, matrice_output)


    def perform_all_verification(self, search_set: PointSet = None):
        if search_set is not None:
            self.search = search_set

        if self.search is None:
            raise ValueError('Aucun ensemble sur lequel rechercher')
        else:
            search = CandidateSearch(self.search)
            for candidat in search.iterate():
                print(candidat)
                vector = [coordonnee for point in candidat.points
                            for coordonnee in (point.x, point.y, point.z)]
                output = self.network.use_reseau(vector)
                reponse = [math.ceil(out) for out in output[0]]

                if reponse == NeuralNetwork.vrais:
                    print("Vrais")
                    search.report_positive(candidat)
                elif reponse == NeuralNetwork.faux:
                    print("Faux")
                else:
                    print("Bug")

    def verifier_reseau(self, search_set: PointSet = None):
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

    def generate_false(self, search_set: PointSet, candidats_vrais: LearningSet):
        search = CandidateSearch(self.search)
        candidats = set([candidat for candidat in search.iterate()])
        candidats_vrais = set([candidat for candidat in  candidats_vrais.iterate()])
        candidats_false = candidats - candidats_vrais

        return candidats_false