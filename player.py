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

    def get_status(self):
        if self.direction.magnitude()==0:
            self.status=self.status.split('_')[0]+'_idle'
        if self.attacking:
            self.status=self.status.split('_')[0]+'_attack'

    def input(self):
        keys=pygame.key.get_pressed()

        if not self.attacking:
            # vertical movement
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y=-1
                self.status='up'
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y=1
                self.status='down'
            else:
                self.direction.y=0

            # horizontal movement
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x=1
                self.status='right'
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x=-1
                self.status='left'
            else:
                self.direction.x=0
            
            # attacking
            if keys[pygame.K_SPACE]:
                if self.status.split('_')[0]=='left':
                    self.bullet_direction=vector(-1,0)
                elif self.status.split('_')[0]=='right':
                    self.bullet_direction=vector(1,0)
                elif self.status.split('_')[0]=='up':
                    self.bullet_direction=vector(0,-1)
                elif self.status.split('_')[0]=='down':
                    self.bullet_direction=vector(0,1)
    
    def update(self,dt):
        self.input()
        self.get_status()
        self.invincibility_timer()
        self.animate(dt)
        self.blink()
        self.move(dt)
        self.check_death()