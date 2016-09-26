# trajectoire-de-bulle
Projet visant à déterminer les trajectoires de bulles à partir d'un fichier de données

Rappel du problème : Différentes position sont obtenus par un faisceau laser qui rebondit sur des particules, nous donnant alors leur positions en x, y et z dans un repère donnée. En ayant à notre disposition l'ensemble des différentes positions et leur coordonnées sous la forme d'un fichier, nous devons détecter la trajectoires prise par une particules. Ces particules sont prises dans un tourbillon (c'est son comportement que nous cherchons à étudier), leurs trajectoires seront donc courbes.

## Approche itérative
---

L'approche itérative consiste à tester les points sucessevivement avec leurs "voisins" pour en dégager une séquence 
selon les données qui définnissent la séquence.

Les problèmes à résoudre sont :
* La détermination des points voisins d'un point donné pour débuter l'identification d'une séquence
* La modularité des boucles pour accepter différentes sortes de séquence
* Décider comment gérer "le début d'une séquence"
* Décider de la suppresion des points utilisé dans une séquence précédemment déterminée.

Aide :  
https://en.wikipedia.org/wiki/Nearest_neighbor_search  
https://en.wikipedia.org/wiki/Fixed-radius_near_neighbors
