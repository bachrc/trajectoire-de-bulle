## Parsing des fichiers et candidats ##

Ce module prend en charge le preprocessing du modèle, soit :

1. L'extraction des données contenues dans les fichiers (`datamodel`)
2. L'identification de candidats potentiels (`candidates`).

### Parsing ###

Le module `datamodel` fournit la représentation d'un point, et d'un ensemble de
points, ce dernier étant initialisé avec un fichier.

**Note:** les fonctionnalités permettant de récupérer les fichiers de
trajectoires ne sont pas encore présentes.

`PointSet` fournit également deux méthodes `nearest` et `neighbours` prenant
toutes les deux un point de référence. La recherche du plus proche retourne un
point. La recherche des voisins prend un rayon de recherche et retourne un
ensemble de voisins.

### Recherche de candidats ###

La classe `CandidateSearch` prend en charge la recherche de candidats. La
méthode `iterate` est un générateur (itérateur) qui, à chaque appel, fourni un
candidat potentiel (voir son utilisation dans `enumerative.testing`).

**Important !** Une fois qu'un candidat a été testé, il est important de
signaler tout résultat positif a la classe en appelant `report_positive` ! Peu
importe si le résultat vient de la méthode énumérative dans `testing` ou du
réseau de neurones !
