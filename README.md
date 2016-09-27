# trajectoire-de-bulle
Projet visant à déterminer les trajectoires de bulles à partir d'un fichier de données

Rappel du problème : Différentes position sont obtenus par un faisceau laser qui rebondit sur des particules, nous donnant alors leur positions en x, y et z dans un repère donnée. En ayant à notre disposition l'ensemble des différentes positions et leur coordonnées sous la forme d'un fichier, nous devons détecter la trajectoires prise par une particules. Ces particules sont prises dans un tourbillon (c'est son comportement que nous cherchons à étudier), leurs trajectoires seront donc courbes.

## Approche Analytique
---

L'approche analutique consiste à vérifier que les quintuplets répondent à des conditions spécifiques pour estimer que ce sont de possible trajectoire. Pour ca, on vérifie :

  -Que les distances entre les points correspondent à une distance moyenne + ou - un seuil de tolérance.
  -Que l'angle entre les points ne dépasse pas une valeur donnée.
