import os
import pygame
from pygame.math import Vector2 as vector

class Entity(pygame.sprite.Sprite):
    def __init__(self,position,group,collision_sprite,path):
        super().__init__(group)
        self.import_assets(path)
        self.image=pygame.Surface((50,50))
        self.rect=self.image.get_rect(center=position)

        # movements
        self.position=vector(self.rect.center)
        self.direction=vector()
        self.speed=330

        # collisions
        self.hitbox=self.rect.inflate(-self.rect.width/2,-self.rect.height*.4)
        self.collision_sprite=collision_sprite

        # attacks
        self.attacking=False
    
    def move(self,dt):
        if self.direction.magnitude()!=0:
            self.direction=self.direction.normalize()

        # horizontal movement
        self.position.x+=self.direction.x*self.speed*dt
        self.hitbox.centerx=round(self.position.x)
        self.rect.center=self.hitbox.center
        self.collision('horizontal')

        # vertical movement
        self.position.y+=self.direction.y*self.speed*dt
        self.hitbox.centery=round(self.position.y)
        self.rect.center=self.hitbox.center
        self.collision('vertical')