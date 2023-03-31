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
            else:
                if direction.y<0:
                    self.status='up_idle'
                else:
                    self.status='down_idle'
    
class Coffin(Entity,Monster):
    def __init__(self, position, group, collision_sprite, path,player):
        super().__init__(position, group, collision_sprite, path)
        # player interaction
        self.player=player
        self.notice_radius=550
        self.walk_radius=500
        self.attack_radius=150
        self.health=3

        # overwrites
        self.speed=200
        
        # sounds
        self.shovel_hit=pygame.mixer.Sound(os.path.join('sound','shovel-hit.wav'))
    
    def attack(self):
        distance=self.get_player_distance_direction()[0]
        if distance<self.attack_radius and not self.attacking:
            self.attacking=True
            self.shovel_hit.play()
            self.frameidx=0
        if self.attacking:
            self.status=self.status.split('_')[0]+'_attack'

    def animate(self,dt):
        self.frameidx+=18*dt
        distance=self.get_player_distance_direction()[0]
        if int(self.frameidx)==4 and self.attacking:
            if distance<self.attack_radius:
                self.player.damage()
        if self.frameidx>=len(self.animations[self.status]):
            self.frameidx=0
            if self.attacking:
                self.attacking=False
        self.image=self.animations[self.status][int(self.frameidx)]
        self.mask=pygame.mask.from_surface(self.image)
    
    def update(self,dt):
        self.face()
        self.chase()
        self.attack()
        self.animate(dt)

class Cactus(Entity,Monster):
    def __init__(self, position, group, collision_sprite, path,player,create_bullet):
        super().__init__(position, group, collision_sprite, path)
        # player interaction
        self.player=player
        self.notice_radius=550
        self.walk_radius=500
        self.attack_radius=350
        self.health=1
    
    def attack(self):
        distance=self.get_player_distance_direction()[0]
        if distance<self.attack_radius and not self.attacking:
            self.attacking=True
            self.frameidx=0
            self.bullet_shot=False
        if self.attacking:
            self.status=self.status.split('_')[0]+'_attack'
    
    def animate(self,dt):
        if int(self.frameidx)==6 and self.attacking and not self.bullet_shot:
            distance,direction=self.get_player_distance_direction()
            self.create_bullet(self.rect.center+direction*150,direction,1000)
            self.bullet_sound.play()
            self.bullet_shot=True
        if self.frameidx>=len(self.animations[self.status]):
            self.frameidx=0
            if self.attacking:
                self.attacking=False
        self.image=self.animations[self.status][int(self.frameidx)]
        self.mask=pygame.mask.from_surface(self.image)
    
    def update(self,dt):
        self.face()
        self.chase()
        self.attack()
        self.animate(dt)
        self.blink()
        self.invincibility_timer()
        self.check_death()
        self.move(dt)