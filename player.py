import pygame
import os
from pygame.math import Vector2 as vector
from entity import Entity

class Player(Entity):
    def __init__(self,position,group,collision_sprite,path,create_bullet):
        super().__init__(position,group,collision_sprite,path)
        self.create_bullet=create_bullet
        self.bullet_shot=False
        self.bullet_direction=vector()
    
    def animate(self,dt):
        self.frameidx+=7*dt
        if int(self.frameidx)==2 and self.attacking and not self.bullet_shot:
            self.create_bullet(self.rect.center+self.bullet_direction*80,self.bullet_direction,5000)
            self.bullet_shot=True
            self.bullet_sound.play()
        
    def update(self,dt):
        self.input()
        self.get_status()
        self.invincibility_timer()
        self.animate(dt)
        self.blink()
        self.move(dt)
        self.check_death()