#!/usr/bin/env python
from game import Game
from solarsystem import SolarSystem

if __name__ == "__main__":
    game = Game()
    SolarSystem(game)
    game.run()
