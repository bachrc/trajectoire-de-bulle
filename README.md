# trajectoire-de-bulle
Projet visant à déterminer les trajectoires de bulles à partir d'un fichier de données

Rappel du problème : Différentes position sont obtenus par un faisceau laser qui rebondit sur des particules, nous donnant alors leur positions en x, y et z dans un repère donnée. En ayant à notre disposition l'ensemble des différentes positions et leur coordonnées sous la forme d'un fichier, nous devons détecter la trajectoires prise par une particules. Ces particules sont prises dans un tourbillon (c'est son comportement que nous cherchons à étudier), leurs trajectoires seront donc courbes.

EDIT 27/09/16 : Nous avons décidé de dévelloper deux approches d'identification : l'une par les réseau de neurone et l'autre plus analytique. Les deux approches ont pour but d'analyser un ensemble de point et de vérifier si celui-ci correspond à une trajectoire. C'est par l'exploration optimisé que l'on obtient les différents ensemble de point.
