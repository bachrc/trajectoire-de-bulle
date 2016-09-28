## Approche de base (énumérative) ##

### Principe ###

Le package `enumerative` se centre autour du fichier `testing.py`. Ce fichier
définit la classe `SampleTest` qui prend en paramètres l'angle et la tolérance
de distance à mettre en oeuvre dans l'instance.

L'attribut `trajectories` liste toutes les trajectoires valides qui ont été
identifiées à partir de candidats. Le score du test est le nombre de
trajectoires ainsi trouvées.

`validate_candidate` prend en paramètre un candidat, et le retourne si ce
dernier décrit une trajectoire valide. Elle renvoie `None` dans le cas
contraire. Dans l'idéal, cette méthode doit également classer les points dans
l'ordre et modifier le candidat avant de le retourner.

`perform` est le point d'entrée. Il itère sur les candidats fournis et lance la
validation sur chacun. La gestion des candidats est gérée par
`preprocessing.candidates` (voir le README de `preprocessing`).

Le module `enumerate.py` est un programme de test pour `testing`.
