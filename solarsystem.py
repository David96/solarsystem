import pygame
import pygame.freetype as freetype
import numpy as np

from pygame import Color
from pygame.locals import *

from game import Game, GameObject
from body import Body

class SolarSystem(GameObject):
    G = 6.67408e-11
    TRACE_ENABLED = False
    def __init__(self, game):
        super().__init__(game)
        self.planets = []
        self.reset()

    def reset(self):
        print("resetting bodies")
        for planet in self.planets:
            self.game.del_game_object(planet)
        self.planets.clear()
        self.planets = [ Body(self.game, "Sun", 1.9891e30, np.array([0,0]), np.array([0,0]), 5, (255,0,0), False),
                Body(self.game, "Mercury", 0.330e24, np.array([0,-57.9e9]), np.array([47.4e3,0]), 3, (255,255,0), self.TRACE_ENABLED),
                Body(self.game, "Venus", 4.87e24, np.array([0,-108.2e9]), np.array([35e3,0]), 3, (0,255,255), self.TRACE_ENABLED),
                Body(self.game, "Earth", 5.97219e24, np.array([0,-149.6e9]), np.array([29.78e3,0]), 3, (0,0,255), self.TRACE_ENABLED),
                Body(self.game, "Mars", 0.642e24, np.array([0, -227.9e9]), np.array([24.1e3,0]), 3, (150,0,0), self.TRACE_ENABLED),
                Body(self.game, "Jupiter", 1.89813e27, np.array([0, -778.5e9]), np.array([13.06e3,0]), 3, (0,255,0), self.TRACE_ENABLED),
                Body(self.game, "Saturn", 568e24, np.array([0,-1433.5e9]), np.array([9.7e3,0]), 3, (0,150,150), self.TRACE_ENABLED),
                Body(self.game, "Uranus", 86.8e24, np.array([0, -2872.5e9]), np.array([6.8e3, 0]), 3, (150, 150, 0), self.TRACE_ENABLED),
                Body(self.game, "Neptune", 102e24, np.array([0,-4495.1e9]), np.array([5.4e3,0]), 3, (150,150,150), self.TRACE_ENABLED), ]


    def update(self, time):
        for i in range(0, len(self.planets)):
            a = self.planets[i]
            a.accel = np.array([0,0])
            for j in range(0, len(self.planets)):
                if i != j:
                    b = self.planets[j]
                    r = b.position - a.position
                    a.accel = a.accel + r / (np.linalg.norm(r) ** 3) * SolarSystem.G * b.mass


