import pygame
import pygame.freetype as freetype
import numpy as np

from pygame import Color
from pygame.locals import *

from game import Game, GameObject

class Body(GameObject):
    TRACE_PRECISION=2**2 # Minimal distance of two trace points squared
    def __init__(self, game, name, mass, position, speed, radius, color, trace=True):
        super().__init__(game)
        self.name = name
        self.mass = mass
        self.position = position
        self.radius = radius
        self.color = color
        self.accel = np.array([0,0], dtype=np.int32)
        self.speed = speed
        self.trace = trace
        transpos = self.transform(self.position)
        self.points = [ (transpos[0], transpos[1]) ]

    def transform(self, pos):
        pos = np.array([self.position[0], self.position[1], 1])
        return np.squeeze(np.asarray(self.game.get_camera().dot(pos))).astype(int)

    def paint(self, time, surface):
        self.speed = self.speed + self.accel * time
        self.position = self.position + self.speed * time
        pos = self.transform(self.position)
        if self.trace:
            if (pos[0] - self.points[-1][0]) ** 2 + (pos[1] - self.points[-1][1]) ** 2 > Body.TRACE_PRECISION:
                self.points.append((pos[0], pos[1]))
                if len(self.points) > 1000:
                    self.points.pop(0)
            if len(self.points) > 1:
                pygame.draw.aalines(surface, (self.color[0]/2,self.color[1]/2,self.color[2]/2), False, self.points)
        pygame.draw.circle(surface, self.color, (pos[0], pos[1]), self.radius)


