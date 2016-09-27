## Approche de base ##

### Principe ###

Cette branche prend en charge l'évaluation de la méthode de base : explorer le
repère à la recherche de trajectoires en se basant sur une valeur de tolérance
et d'angle. Au cours du programme ces variables prennent différentes valeurs, et
chaque couple est évalué en fonction du nombre de trajectoires valides qu'il
permet d'extraire.

- **whirlwinds.py** se charge de ces variations, et lance un test sur chaque
couple possible. C'est ici que les résultats sont synthétisés pour chaque
fichier de données.

- **parser.py** s'occupe de représenter l'ensemble de points, et de l'extraire
d'un fichier. La structure PointSet est un point critique, car ses méthodes de
recherche de voisins sont souvent utilisées.

- **testing.py** représente un test, pour deux valeurs (tolérance, angle)
donnéees. Son objectif est de détecter les possibles trajectoires en ciblant des
ensembles de 5 points, puis de les évaluer en utilisant les valeurs de tolérance
et d'angle associées au test.

### TODO list ###

A l'heure actuelle les structures de données utilisées ne permettent pas
d'exécuter ce procédé avec une complexité temporelle raisonnable. Une meilleure
implémentation est nécessaire pour accélérer les recherches de voisins.
