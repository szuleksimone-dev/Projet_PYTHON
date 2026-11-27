
# Kart-Engine v2.3

import unittest

from constants import (
    CAR_ACCELERATION,
    CAR_BRAKE,
    CAR_MAX_REVERSE_SPEED,
    CAR_TURN_SPEED
)
from model.car import Car


class TestCarControls(unittest.TestCase):
    """
    Vérifie les commandes principales de la voiture.

    Chaque test contrôle une action sans lancer
    une course complète.
    """

    def setUp(self):
        """
        Crée une nouvelle voiture avant chaque test.

        Ainsi, les tests sont indépendants :
        la vitesse ou l'angle d'un test ne modifie
        pas les résultats des autres tests.
        """
        self.car = Car(7, 1)

    def test_acceleration(self):
        """Vérifie que la voiture accélère."""
        self.car.accelerate()

        # La vitesse doit augmenter.
        self.assertAlmostEqual(
            self.car.speed, CAR_ACCELERATION
        )

    def test_reverse(self):
        """
        Vérifie que la voiture ralentit puis recule.
        Vérifie aussi la limite de vitesse en marche arrière.
        """
        self.car.speed = 2 * CAR_ACCELERATION

        # La commande réduit d'abord la vitesse.
        self.car.reverse()
        self.assertAlmostEqual(
            self.car.speed, CAR_ACCELERATION
        )

        # En maintenant la commande, la voiture recule.
        self.car.reverse()
        self.car.reverse()
        self.assertLess(self.car.speed, 0)

        # La vitesse arrière ne doit pas dépasser la limite.
        for _ in range(100):
            self.car.reverse()

        self.assertAlmostEqual(
            self.car.speed, -CAR_MAX_REVERSE_SPEED
        )

    def test_brake(self):
        """
        Vérifie que le frein arrête la voiture
        en marche avant et en marche arrière.
        """
        # Test du freinage en marche avant.
        self.car.speed = 2 * CAR_BRAKE
        self.car.brake()
        self.car.brake()

        self.assertAlmostEqual(self.car.speed, 0)

        # Test du freinage en marche arrière.
        self.car.speed = -2 * CAR_BRAKE
        self.car.brake()
        self.car.brake()

        self.assertAlmostEqual(self.car.speed, 0)

    def test_steering(self):
        """
        Vérifie que les commandes gauche et droite
        modifient correctement l'angle de la voiture.
        """
        self.car.steer_left()

        self.assertAlmostEqual(
            self.car.angle, -CAR_TURN_SPEED
        )

        self.car.steer_right()

        # Les deux rotations opposées s'annulent.
        self.assertAlmostEqual(self.car.angle, 0)
