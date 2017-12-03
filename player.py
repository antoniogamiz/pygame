import pygame
from pygame.locals import *

class Monigotillo(pygame.sprite.Sprite):

    def __init__(self, window, coordinates, image):
        pygame.sprite.Sprite.__init__(self)
        self.window = window
        self.ImgCompleta = image
        a=0
        self.arrayAnim=[]
        while a < 6:
            self.arrayAnim.append(self.ImgCompleta.subsurface((a*32,100,32,64)))
            a= a + 1
        self.anim= 0

        self.actualizado = pygame.time.get_ticks()
        self.image = self.arrayAnim[self.anim]
        self.rect = self.image.get_rect()
        self.rect.center = coordinates

    def update_movement(self, coord):
        self.rect = self.rect.move(coord) 

    def update(self, ventana):
        # self.update_movement()
        if self.actualizado + 100 < pygame.time.get_ticks():
            self.anim= self.anim + 1
            if self.anim > 5:
                self.anim= 0
            self.image = self.arrayAnim[self.anim]
            self.actualizado= pygame.time.get_ticks()
            
        ventana.blit(self.image, self.rect)