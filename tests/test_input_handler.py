
# Kart-Engine v2.3

import unittest
from collections import defaultdict
from unittest.mock import patch

import pygame

from controller.input_handler import InputHandler


class TestInputHandler(unittest.TestCase):
    """
    Vérifie les commandes clavier des deux joueurs.

    Les tests simulent les touches appuyées sans
    avoir besoin d'ouvrir la fenêtre du jeu.
    """

    def setUp(self):
        """Crée un gestionnaire de commandes pour chaque test."""
        self.handler = InputHandler()

    def lire_commandes(self, *touches):
        """
        Simule les touches maintenues enfoncées.

        Les autres touches sont considérées comme relâchées.
        """
        clavier = defaultdict(bool)

        for touche in touches:
            clavier[touche] = True

        # On remplace temporairement la lecture du clavier.
        with patch(
            "controller.input_handler.pygame.key.get_pressed",
            return_value=clavier
        ):
            return self.handler.get_inputs()

    def test_aucune_touche(self):
        """Sans touche appuyée, aucune action n'est active."""
        commandes = self.lire_commandes()

        for joueur in ("player1", "player2"):
            self.assertFalse(any(commandes[joueur].values()))

    def test_commandes_joueur1(self):
        """Vérifie les touches du premier joueur."""
        commandes = self.lire_commandes(
            pygame.K_z, pygame.K_q, pygame.K_SPACE
        )

        joueur1 = commandes["player1"]

        self.assertTrue(joueur1["accelerate"])
        self.assertTrue(joueur1["steer_left"])
        self.assertTrue(joueur1["use_item"])
        self.assertFalse(joueur1["reverse"])

        # Le joueur 2 ne doit pas réagir.
        self.assertFalse(any(commandes["player2"].values()))

    def test_commandes_joueur2(self):
        """Vérifie les touches du deuxième joueur."""
        commandes = self.lire_commandes(
            pygame.K_UP, pygame.K_RIGHT, pygame.K_RETURN
        )

        joueur2 = commandes["player2"]

        self.assertTrue(joueur2["accelerate"])
        self.assertTrue(joueur2["steer_right"])
        self.assertTrue(joueur2["use_item"])
        self.assertFalse(joueur2["reverse"])

        # Le joueur 1 ne doit pas réagir.
        self.assertFalse(any(commandes["player1"].values()))

    def test_commandes_simultanees(self):
        """
        Vérifie que les deux joueurs peuvent utiliser
        leurs commandes en même temps.
        """
        commandes = self.lire_commandes(
            pygame.K_w, pygame.K_DOWN
        )

        self.assertTrue(commandes["player1"]["accelerate"])
        self.assertTrue(commandes["player2"]["reverse"])

    def test_touches_alternatives(self):
        """
        Vérifie les touches alternatives du joueur 1
        et les commandes de recul et de direction.
        """
        commandes = self.lire_commandes(
            pygame.K_a, pygame.K_s, pygame.K_d
        )

        joueur1 = commandes["player1"]

        self.assertTrue(joueur1["steer_left"])
        self.assertTrue(joueur1["reverse"])
        self.assertTrue(joueur1["steer_right"])
