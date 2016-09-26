# trajectoire-de-bulle
Projet visant à déterminer les trajectoires de bulles à partir d'un fichier de données

Rappel du problème : Différentes position sont obtenus par un faisceau laser qui rebondit sur des particules, nous donnant alors leur positions en x, y et z dans un repère donnée.
En ayant à notre disposition l'ensemble des différentes positions et leur coordonnées sous la forme d'un fichier, nous devons détecter la trajectoires prise par une particules. Ces particules sont prises dans un tourbillon (c'est son comportement que nous cherchons à étudier), leurs trajectoires seront donc courbes.

On essaye ici une approche par Réseau de neurones de ce problème. L'idée principal étant qu'une trajectoire dessiné par une suite de points n'est rien d'autre qu'un pattern. Il est donc possible d'enseigner ce pattern à un réseau de neurones de manière à lui faire reconnaitres les différentes trajectoires.

Deux visions sont possibles : 
 - Un réseau qui prend en paramètre un ensemble de point que l'on soupsconne d'être une trajctoire. Celui répond alors par oui ou non.
 - Un réseau qui lies ensemble des points qui correspondent à une trajctoire. C'est alors l'étude des points ainsi relié qui nous donne la liste des trajectoires. Ceci peut être envisagé par un réseau de type courant : des paramètres d'entrée et des paramètres de sortie, ou par une mémoire auto-associative.
 
 Dans le premier cas, les paramètres d'entrée sont l'ensembles des coordonées des points dans un ordre précis. Les paramètres de sorties seront alors chacun considéré comme une trajctoire, et l'on obtient alors une trajectoire en étudiant quel neurones sont relié a chacun des neurones de sorties. Ainsi, chaque neurones de sorties aura n neurones d'entrée lié, et ceux-ci formeront alors une trajectoire.
 
 Dans le second cas, les paramètres d'entrée et de sortie ne forme qu'un unique ensemble et on cherche à relié les points entre-eux pour définir ainsi des ensembles qui seront nos trajectoires.
 
 Il est important de rappeler les différents avantages et inconvénients inhérent au Réseau de neurones. Il s'agit d'une technique possédant une grande fiabilité et une assez bonne plasticité d'execution. De plus, les réseau de neurones ne demande qu'un temps d'execution minimal à l'execution. Les mauvais points sont principalement le manque de compréhension interne : Un réseau de neurones fonctionne mais on ne saurait expliquer clairement (autrement qu'avec des mathématiques) comment. A cela s'ajoute qu'un réseau de neurones ne fonctionne que pour les cas auxquelles il est destiné, de par son design il est difficile de le faire évoluer, c'est la rançon de sa fiabilité. Enfin, il est nécessaire d'entraîner un réseau de neurones, cela correspond à la rançon de son efficacité puisque cet entrainement est êxtremement long en comparaison de son temps d'execution future.
