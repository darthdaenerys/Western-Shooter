import pygame
from pygame.math import Vector2 as vector

class Monster:
    def get_player_distance_direction(self):
        distance=(vector(self.player.hitbox.center)-vector(self.hitbox.center)).magnitude()
        direction=None
        if distance!=0:
            direction=(vector(self.player.hitbox.center)-vector(self.hitbox.center)).normalize()
        else:
            direction=vector()
        return distance,direction