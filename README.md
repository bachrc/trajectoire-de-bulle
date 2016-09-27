# trajectoire-de-bulle
Projet visant à déterminer les trajectoires de bulles à partir d'un fichier de données (nom provisoire)

## Utilisation du dépot Git
Chaque branche du dépot définit les sections de travail du projet :

- Une branche `gui` pour travailler l'interface graphique
- Une branche `approche-neuronale` où l'on se concentre sur les packages où l'on travaille l'IA
etc.

Il vous suffit de sélectionner la branche dans laquelle vous voulez faire vos changements,
et si ça n'appartient à aucun des domaines couverts par les branches existantes, vous créez une branche à partir
de `master`, sans accent, en lower case, et avec des tirets en guise d'espaces.

Rappel du problème : Différentes position sont obtenus par un faisceau laser qui rebondit sur des particules, nous donnant alors leur positions en x, y et z dans un repère donnée. En ayant à notre disposition l'ensemble des différentes positions et leur coordonnées sous la forme d'un fichier, nous devons détecter la trajectoires prise par une particules. Ces particules sont prises dans un tourbillon (c'est son comportement que nous cherchons à étudier), leurs trajectoires seront donc courbes.

EDIT 27/09/16 : Nous avons décidé de dévelloper deux approches d'identification : l'une par les réseau de neurone et l'autre plus analytique. Les deux approches ont pour but d'analyser un ensemble de point et de vérifier si celui-ci correspond à une trajectoire. C'est par l'exploration optimisé que l'on obtient les différents ensemble de point.
