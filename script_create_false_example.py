from reseau_neuronal.network import Network
from reseau_neuronal.reseau_neural import NeuralNetwork
from preprocessing.datamodel import LearningSet,PointSet
from glob import glob
from gui.interface import GUI

import math
import random
import pprint

tab_learning_set = []
datafiles = glob('./datasets/points/norma_*.txt')
for filename in datafiles:
   print(filename)
   basename = filename[filename.rindex('/') + 1:-4]
   tra_file = "./datasets/trajectories/%s_tra.txt" % basename

   pset = PointSet(filename)
   lset = LearningSet(pset=pset, trajectory_file=tra_file)
   tab_learning_set.append(lset)

#On tranforme la liste de LearningSet en matrice unique
matrice_input_vrais = []
for train_set in tab_learning_set:
    for candidat in train_set.iterate():
        row = [coordonnee for point in candidat.points
               for coordonnee in (point.x, point.y, point.z)]
        matrice_input_vrais.append(row)

max_input = max([max(l) for l in matrice_input_vrais])
min_input = min([min(l) for l in matrice_input_vrais])

#On ajoute un ensemble de candidat que l'on estime faux
matrice_input_faux = [[random.uniform(min_input, max_input) for _ in range(NeuralNetwork.nbNeuroneEntree)] for _ in range(len(matrice_input_vrais))]

matrice_input_faux = [x for row in matrice_input_faux for x in row]
set = set(matrice_input_faux)

pprint(set)
