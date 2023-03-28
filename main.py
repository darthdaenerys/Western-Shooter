import os
import pygame
from sprite import Sprite,Bullet
import sys
from pygame.math import Vector2 as vector
import json
from player import Player
from pytmx.util_pygame import load_pygame
from monster import Coffin,Cactus

class AllSprites(pygame.sprite.Group):
    def __init__(self,settings):
        super().__init__()
        self.offset=vector()
        self.display_surface=pygame.display.get_surface()
        self.background=pygame.image.load(os.path.join('graphics','other','map.png')).convert()
        self.settings=settings
    
    def custom_draw(self,player):
        self.offset.x=player.rect.centerx-self.settings['window_width']/2
        self.offset.y=player.rect.centery-self.settings['window_height']/2
        self.display_surface.blit(self.background,-self.offset)
        for sprite in sorted(self.sprites(),key=lambda sprite:sprite.rect.centery):
            self.display_surface.blit(sprite.image,sprite.rect.topleft-self.offset)

class Game:
    def __init__(self):
        pygame.init()
        f=open('settings.json')
        self.settings=json.load(f)
        del f
        self.display_surface=pygame.display.set_mode((self.settings['window_width'],self.settings['window_height']))
        pygame.display.set_caption('Western Shooter')
        self.clock=pygame.time.Clock()
        self.gamerun=True
        self.bullet_surface=pygame.image.load(os.path.join('graphics','other','particle.png')).convert_alpha()
        self.all_sprites=AllSprites(self.settings)
        self.collision_sprite=pygame.sprite.Group()
        self.bullet_sprite=pygame.sprite.Group()
        self.monster_sprite=pygame.sprite.Group()
        self.music=pygame.mixer.Sound(os.path.join('sound','music.mp3'))
        self.setup()
    
    def create_bullet(self,position,direction,bullet_speed):
        Bullet(position, self.bullet_surface, direction,[self.all_sprites,self.bullet_sprite],bullet_speed)
    
    def bullet_collision(self):
        # bullet obstacle collision
        for obstacle in self.collision_sprite.sprites():
            pygame.sprite.spritecollide(obstacle,self.bullet_sprite,True)

        # bullet monster collision
        for bullet in self.bullet_sprite.sprites():
            sprites=pygame.sprite.spritecollide(bullet,self.monster_sprite,False,pygame.sprite.collide_mask)
            if sprites:
                bullet.kill()
                for sprite in sprites:
                    sprite.damage()

        # player bullet collision
        if pygame.sprite.spritecollide(self.player,self.bullet_sprite,True,pygame.sprite.collide_mask):
            self.player.damage()

    def setup(self):
        tmx_map=load_pygame(os.path.join('data','map.tmx'))
        # tiles
        for x,y,surface in tmx_map.get_layer_by_name('fence').tiles():
            Sprite((x*64,y*64), surface,[self.all_sprites,self.collision_sprite])
        
        # objects
        for obj in tmx_map.get_layer_by_name('object'):
            Sprite((obj.x,obj.y), obj.image,[self.all_sprites,self.collision_sprite])
        
        # entities
        for obj in tmx_map.get_layer_by_name('entities'):
            if obj.name=='Player':
                self.player=Player((obj.x,obj.y),[self.all_sprites,self.monster_sprite],self.collision_sprite,self.settings['paths']['player'],self.create_bullet)
            elif obj.name=='Coffin':
                self.coffin=Coffin((obj.x,obj.y), [self.all_sprites,self.monster_sprite],self.collision_sprite,self.settings['paths']['coffin'],self.player)
            elif obj.name=='Cactus':
                self.Cactus=Cactus((obj.x,obj.y),[self.all_sprites,self.monster_sprite],self.collision_sprite,self.settings['paths']['cactus'],self.player,self.create_bullet)
    
    def run(self):
        self.music.play(loops=-1)
        while self.gamerun:
            dt=self.clock.tick(60)/1000

            # check game events
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.gamerun=False
            
            # update sprites
            self.all_sprites.update(dt)
            self.bullet_collision()

            # draw sprites
            self.display_surface.fill('black')
            self.all_sprites.custom_draw(self.player)

            # update display
            pygame.display.update()
        pygame.quit()

if __name__=='__main__':
    game=Game()
    game.run()