from glob import glob
from preprocessing.datamodel import LearningSet, PointSet
from preprocessing.candidates import CandidateSearch

"""
Script permettant de générer les valeurs fausse à passer au réseau en se basant
sur les fichiers de points et les fichier de trajectoire connus.

La logique utiliser ici correspond à
[Toute les trajectoires] - [Trajectoire vrais] = [Trajectoire fausse]
Il est impératif que les trajectoires connus soient absolument sur pour que
l'on puisse utiliser cette méthode et qu'il ne reste que peux de trajctoires
inconnus dans les ensembles de points utiliser
"""

datafiles = glob('./datasets/points/norma_*.txt')
for filename in datafiles:

    print(filename)
    basename = filename[filename.rindex('/') + 1:-4]
    tra_file = "./datasets/trajectories/%s_tra.txt" % basename

    pset = PointSet(filename)
    lset = LearningSet(pset=pset, trajectory_file=tra_file)

    search = CandidateSearch(pset)

    candidats = set([candidat for candidat in search.iterate()])
    candidats_vrais = set([candidat for candidat in lset.iterate()])
    candidats_false = candidats - candidats_vrais

    with open(tra_file[:-4]+"_false.txt", "w") as out:
        for candidat in candidats_false:
            print(candidat)
            out.write(" ".join(str(p.p_id) for p in candidat.points) + "\n")
