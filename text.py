import pygame
import random
from pygame.locals import *


class Player(pygame.sprite.Sprite):
    def __init(self, image):
        self.image=image
        self.rect=self.imagen.get_rect()
        self.rect.top, self.rect.left=(100,200)
    def mover(self, vx, vy):
        pass
    def update(self, surface):
        surface.blit.(self.image, self.rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode([600,400])
    pygame.display.set_caption("Acnologia")

    #COLORES
    WHITE=(255,255,255)
    BLACK=(0,0,0)
    RED=(255,0,0)
    GREEN=(0,255,0)

    main_clock = pygame.time.Clock()

    exit= False
    
    while not exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True

        main_clock.tick(3000)

        screen.fill(BLACK)

        pygame.display.update()



    pygame.quit()




main()