
import pygame
import random
from pygame.locals import *

def load_image(filename, transparent=False):
    image = pygame.image.load(filename)
    image = image.convert()
    if transparent:
        color = image.get_at((0,0))
        image.set_colorkey(color, RLEACCEL)
    return image


class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.top=450
        self.rect.left=300
        self.image=pygame.transform.scale(self.image, (100,100))
    def move(self, vx, vy):
        self.rect.move_ip(vx,vy)
    def update(self, surface):
        surface.blit(self.image, self.rect)




def main():
    pygame.init()
    screen = pygame.display.set_mode([600,900])
    pygame.display.set_caption("Acnologia")

    vx,vy = 0,0
    speed = 1

    # LEFT, RIGHT, UP, DOWN
    key_pressed = [False, False, False, False]

    ship=load_image(".\\images\\ship.png")
    player=Player(ship)

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                vx=-speed
            if event.key == pygame.K_RIGHT:
                vx=speed
            if event.key == pygame.K_UP:
                vy=-speed
            if event.key == pygame.K_DOWN:
                vy=speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                if key_pressed[0]: vx=speed
                else: vx=0
            if event.key == pygame.K_RIGHT:
                if key_pressed[1]: vx=-speed
                else: vx=0
            if event.key == pygame.K_UP:
                if key_pressed[2]: vy=speed
                else: vy=0
            if event.key == pygame.K_DOWN:
                if key_pressed[3]: vy=-speed
                else: vy=0

        main_clock.tick(3000)
        player.move(vx,vy)
        screen.fill(BLACK)
        player.update(screen)
        
        pygame.display.update()

        #player.update(screen)


    pygame.quit()




main()