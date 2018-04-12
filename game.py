import pygame
import pygame.freetype as freetype
import numpy as np

from pygame import Color
from pygame.locals import *

class GameObject:
    def __init__(self, game):
        self.game = game
        game.add_game_object(self)
    def paint(self, time, surface):
        pass
    def update(self, time):
        pass
    def reset(self):
        pass

class Game:
    VIEWPORT_HEIGHT=2 * 4499e9
    WINDOW_WIDTH=1500
    WINDOW_HEIGHT=1000
    ANIMATION_SPEED = 10 # Years per second
    SCALING_FACTOR = 1.2
    FIXED_TIMESTEP = 2
    FPS = 0

    def __init__(self):
        pygame.init()
        freetype.init()
        pygame.mouse.set_visible(1)

        self.clock = pygame.time.Clock()
        self.objects = []
        self.screen = pygame.display.set_mode( (self.WINDOW_WIDTH,self.WINDOW_HEIGHT) )
        self.font = freetype.SysFont("DeJaVu", size=10)
        self.update_camera()
        self.total_elapsed = 0

    def update_camera(self):
        self.proj_matrix = np.matrix(
                [[self.WINDOW_WIDTH/((self.WINDOW_WIDTH/self.WINDOW_HEIGHT)*self.VIEWPORT_HEIGHT), 0, self.WINDOW_WIDTH/2],
                [0, self.WINDOW_HEIGHT/self.VIEWPORT_HEIGHT, self.WINDOW_HEIGHT/2],
                [0, 0, 1]])

    def run(self):
        running = True
        self.clock.tick(self.FPS) # reset time spent during initialization
        while running:
            elapsed = self.clock.tick(self.FPS) # tick must be called for FPS to work
            if self.FIXED_TIMESTEP != 0:
                elapsed = self.FIXED_TIMESTEP
            elapsed = (elapsed / 1000) * 60 * 60 * 24 * 365.25 * self.ANIMATION_SPEED
            self.total_elapsed += elapsed
            self.screen.fill( (0,0,0) )

            for obj in self.objects:
                obj.update(elapsed)
                obj.paint(elapsed, self.screen)

            for event in pygame.event.get():
                running = self.handle_event(event)

            self.font.render_to(self.screen, (10,10), "FPS: %d" % self.clock.get_fps(), (255,255,255))
            self.font.render_to(self.screen, (10,22),
                    "Elapsed time: %fyr" % (self.total_elapsed / (60 * 60 * 24 * 365.25)), Color("white"))
            #for i in range(0, len(solarsystem.planets)):
            #    p = solarsystem.planets[i]
            #    font.render_to(screen, (10, 12*(i+3)), "%s: (x,y) = (%e,%e)" % (p.name, p.position[0], p.position[1]), (255,255,255))
            pygame.display.flip()
        freetype.quit()

    def reset(self):
        self.total_elapsed = 0
        for obj in self.objects:
            obj.reset()

    def add_game_object(self, obj):
        self.objects.append(obj)

    def del_game_object(self, obj):
        self.objects.remove(obj)

    def get_camera(self):
        return self.proj_matrix

    def handle_event(self, event):
        if event.type == pygame.KEYUP:
            self.handle_key_up(event.key, event.mod)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(event.pos, event.button)
        return event.type != pygame.QUIT

    def handle_key_up(self, key, mod):
        if key == ord("r"):
            self.reset()
        elif key == K_ESCAPE:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def handle_mouse_down(self, pos, button):
        if button == 4:
            self.VIEWPORT_HEIGHT /= self.SCALING_FACTOR
            self.update_camera()
        elif button == 5:
            self.VIEWPORT_HEIGHT *= self.SCALING_FACTOR
            self.update_camera()
