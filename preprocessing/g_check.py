from preprocessing.datamodel import PointSet
from preprocessing.candidates import CandidateSearch
from gui.plot import GUI

import random

pset = PointSet("../datasets/points/norma_N5_tau4_dt2_delai820_000001.txt")
search = CandidateSearch(pset)
gui = GUI([(p.x, p.y, p.z) for p in pset.points], [])

for candidate in search.iterate():
    gui.add_special_bubbles(((p.x, p.y, p.z) for p in candidate.points))

    # TODO: add an actual test...
    if bool(random.getrandbits(1)):
        search.report_positive(candidate)
        gui.add_trajectories([(p.x, p.y, p.z) for p in candidate.points], True)

gui.display()
