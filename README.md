# Jeu de Course 2D (Projet Python - IPS)

    Jeu de course arcade 2D développé en Python avec la bibliothèque **Pygame**, respectant une architecture stricte **Modèle-Vue-Contrôleur (MVC)**.

## Installation

    Assurez vous d'avoir installé **Python** (version 3.10 ou supérieure recommandée)
    pip3 install -r requirements.txt

## Lancer le jeu

    python3 main.py

## Utilisation des outils d'IA

    (à compléter au cours du projet)

## Répartition du travail et planning

    Membre 1 : Modèle & Moteur Physique
    Physique de la voiture : Gestion de l'accélération (avant/arrière) et de la rotation de l'angle de braquage.   
    Système de dérapage (Drift) : Calcul automatique du dérapage lorsque l'orientation de la voiture diffère de son vecteur vitesse.   
    Influence des terrains : Intégration des variables de friction et de traction pour la Route, l'Herbe, la Terre, la Glace et les blocs "vide".   
    Sécurité anti-sortie de piste : Téléportation automatique au dernier point de passage sain et annulation de la vitesse (vitesse nulle) en cas de sortie de grille ou de passage sur le vide. 

    Membre 2 : Contrôleur & Logique de Course
    Entrées Joueurs : Configuration de la lecture du clavier pour 2 joueurs en simultané (Joueur 1 : ZQSD/WASD, Joueur 2 : Flèches directionnelles).   
    Logique du circuit : Vérification de la position des voitures sur la grille pour valider les Checkpoints.   
    Boucle de course : Comptage des tours au franchissement de la ligne d'arrivée (soumis à la validation de tous les checkpoints).   
    Blocs spéciaux : Déclenchement des blocs de Boost et gestion des blocs de départ.

    Membre 3 : Vue, Menus & Level Design   
    Level Design : Conception des circuits sous forme de matrices (tableaux 2D) intégrant les différents types de terrain et checkpoints.   
    Interface en jeu (HUD) : Rendu graphique du circuit, affichage des voitures avec rotation correcte et suivi des tours pour chaque joueur.   
    Navigation et Menus : Implémentation du menu principal (choix du circuit, lancement) et de l'écran de fin de course (affichage du vainqueur).      


