import pygame
import random
from pygame.locals import *

def main():
    l=[]
    for x in range(25):
        w=random.randrange(15,20)
        h=random.randrange(15,20)
        x=random.randrange(400)
        y=random.randrange(400)
        l.append(pygame.Rect(x,y,w,h))
    pygame.init()
    screen = pygame.display.set_mode([400,400])
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

        for recs in l:
            pygame.draw.rect(screen, GREEN, recs)

        pygame.display.update()



    pygame.quit()




main()