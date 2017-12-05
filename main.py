import pygame
import random
from pygame.locals import *

def main():
    for x in range(15):
        w=random.randrange(15, 45)
        h=random.randrange(20,60)
        x=random.randrange(400)
        y=random.randrange(400)
    pygame.init()
    screen = pygame.display.set_mode([400,400])
    pygame.display.set_caption("Acnologia")

    #COLORES
    WHITE=(255,255,255)
    BLACK=(0,0,0)
    RED=(255,0,0)

    #RectÃ¡ngulo
    r1=pygame.Rect(50,50,45,45)
    r2=pygame.Rect(100,100,60,40)

    main_clock = pygame.time.Clock()

    exit= False
    
    while not exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True

        #Almacenamso la antigua posisicion.
        (xant,yant)=(r1.left,r1.top)
        #Desplazamos.
        (r1.left,r1.top)=pygame.mouse.get_pos()
        r1.left-=r1.width/2
        r1.top-=r1.height/2
        #Comprobamos si hay colisión.
        if r1.colliderect(r2):
            # (r1.left,r1.top)=(xant,yant)
            r2.inflate_ip(-1,-1)

            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     r1.move_ip(10,10)
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_LEFT:
            #         r1.move_ip(-10,0)
            #     if event.key == pygame.K_DOWN:
            #         r1.move_ip(0,10)
            #     if event.key == pygame.K_RIGHT:
            #         r1.move_ip(10,0)
            #     if event.key == pygame.K_UP:
            #         r1.move_ip(0,-10)
                    
        main_clock.tick(3000)
        screen.fill(WHITE)

        pygame.draw.rect(screen, BLACK, r1)
        pygame.draw.rect(screen, RED, r2)
        pygame.display.update()



    pygame.quit()




main()