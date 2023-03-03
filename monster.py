import pygame
import os
from pygame.math import Vector2 as vector
from entity import Entity

class Monster:
    def get_player_distance_direction(self):
        distance=(vector(self.player.hitbox.center)-vector(self.hitbox.center)).magnitude()
        direction=None
        if distance!=0:
            direction=(vector(self.player.hitbox.center)-vector(self.hitbox.center)).normalize()
        else:
            direction=vector()
        return distance,direction
    
    def chase(self):
        distance,direction=self.get_player_distance_direction()
        if self.attack_radius<distance<self.walk_radius:
            self.direction=direction
            self.status=self.status.split('_')[0]
        else:
            self.direction=vector()
    
    def face(self):
        distance,direction=self.get_player_distance_direction()
        if distance<self.notice_radius:
            if -.5<direction.y<.5:
                if direction.x<0:
                    self.status='left_idle'
                else:
                    self.status='right_idle'