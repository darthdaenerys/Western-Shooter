import os
import pygame
from pygame.math import Vector2 as vector

class Entity(pygame.sprite.Sprite):
    def __init__(self,position,group,collision_sprite,path):
        super().__init__(group)
        self.import_assets(path)
        self.frameidx=0
        self.status='down_idle'
        self.image=self.animations[self.status][self.frameidx]
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
    
    def import_assets(self,path):
        self.animations={}
        for _ in os.walk(path):
            for folder in _[1]:
                self.animations[folder]=[]
                folder_path=os.path.join(path,folder)
                for file in os.listdir(folder_path):
                    file_path=os.path.join(folder_path,file)
                    surface=pygame.image.load(file_path).convert_alpha()
                    self.animations[folder].append(surface)

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