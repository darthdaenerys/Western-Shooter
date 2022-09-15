import pygame
import os
from pygame.math import Vector2 as vector
class Player(Entity):
    def __init__(self,position,group,collision_sprite,path,create_bullet):
        super().__init__(position,group,collision_sprite,path)
        self.create_bullet=create_bullet
        self.bullet_shot=False
        self.bullet_direction=vector()

    