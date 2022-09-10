import os
import pygame
import sys
import json

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
        self.all_sprites=pygame.sprite.Group()
   
    def run(self):
        while self.gamerun:
            dt=self.clock.tick(60)/1000

            # check game events
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.gamerun=False
            
            # update sprites
            self.all_sprites.update(dt)

            # draw sprites
            self.display_surface.fill('black')
            self.all_sprites.draw()

            # update display
            pygame.display.update()
        pygame.quit()

if __name__=='__main__':
    game=Game()
    game.run()