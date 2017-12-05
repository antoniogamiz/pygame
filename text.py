
import pygame
import random
from pygame.locals import *

# Dimensiones de la pantalla de juego.
SCREEN_WIDTH=600
SCREEN_HEIGHT=900

# COLORES
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)

# Función auxiliar para cargar imágenes (con transparencia si se quiere)
def load_image(filename, transparent=False):
    image = pygame.image.load(filename)
    image = image.convert()
    if transparent:
        color = image.get_at((0,0))
        color = (0,255,0)
        image.set_colorkey(color, RLEACCEL)
    return image

# Genera una posicion aleatoria (l_random, t_random) y un tamaño aleatorio (width, height)
# (l_min, l_max, t_min, t_max, w_min, w_max, h_min, h_max) son las cotas de los valores.
def random_rect_coord_generate(l_min, l_max, t_min, t_max, w_min, w_max, h_min, h_max):
    l_random=random.randrange(l_min, l_max)
    t_random=random.randrange(t_min, t_max)
    width = random.randrange(w_min, w_max)
    height = random.randrange(h_min, h_max)
    return [l_random, t_random, width, height]


# Detecta si 'player' colisiona con alguno de los colliders en pantalla.
def collision_detect(player, colliders):
    for coll in colliders.list:
        if player.rect.colliderect(coll):
            return True
    return False

class Colliders(object):
    def __init__(self, init_n):
        self.SPEED=1
        self.list=[]
        for x in range(init_n):
            # Creamos un rectángulo aleatorio.
            self.list.append(pygame.Rect(random_rect_coord_generate(2, SCREEN_WIDTH, -400, -20, 10, 30, 15, 35)))
    def re_add(self):
        for x in range(len(self.list)):
            if self.list[x].top > SCREEN_HEIGHT:
                self.list[x]=pygame.Rect(random_rect_coord_generate(2, SCREEN_WIDTH, -400, -20, 10, 30, 15, 35))
    def add_other(self):
        pass
    def move(self):
        for rec in self.list:
            rec.move_ip(0, self.SPEED)
    def draw(self, surface):
        for rec in self.list:
            pygame.draw.rect(surface, RED, rec)

class Player(pygame.sprite.Sprite):
    def __init__(self, image, explosion_image, movement_sound):
        self.movement_sound=movement_sound
        self.image=image
        self.explosion_image=explosion_image
        self.rect=self.image.get_rect()
        self.rect.top=SCREEN_HEIGHT-200
        self.rect.left=SCREEN_WIDTH/2 - 50
        self.image=pygame.transform.scale(self.image, (100,100))
        self.explosion_image=pygame.transform.scale(self.explosion_image, (200,200))
    def move(self, vx, vy):
        self.rect.move_ip(vx,vy)
    def kill(self):
        self.image = self.explosion_image
    def movement_play(self):
        self.movement_sound.play()
    def update(self, surface):
        surface.blit(self.image, self.rect)




def main():

    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
    pygame.display.set_caption("Acnologia")

    # Cargamos la música de fondo.
    pygame.mixer.music.load(".\\music\\background_music.mp3")
    movement_sound=pygame.mixer.Sound(".\\music\\movement_sound.wav")

    # Variables auxiliares para el control del movimiento.
    vx,vy = 0,0
    speed = 1
    # LEFT, RIGHT, UP, DOWN
    key_pressed = [False, False, False, False]

    # Creación del player.
    explosion=load_image(".\\images\\explosion.png", True)
    ship=load_image(".\\images\\ship.png", True)
    player=Player(ship, explosion, movement_sound)

    # Creación del fondo.
    bg=load_image(".\\images\\background.png").convert_alpha()
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH,SCREEN_HEIGHT))

    # Creación de los colliders del juego.
    coll=Colliders(5)
    main_clock = pygame.time.Clock()


    GAMEOVER = False
    exit= False
    
    # Reproducimos la música de fondo.
    pygame.mixer.music.play(2)
    pygame.mixer.music.set_volume(0.1)

    while not exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
        if not GAMEOVER:
            #Gestión del movimiento de 'player'.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    key_pressed[0] = True
                    vx=-speed
                    
                if event.key == pygame.K_RIGHT:
                    key_pressed[1] = True
                    vx=speed
                if event.key == pygame.K_UP:
                    key_pressed[2] = True
                    vy=-speed
                if event.key == pygame.K_DOWN:
                    key_pressed[3] = True
                    vy=speed
                player.movement_play()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    key_pressed[0] = False
                    if key_pressed[1]: vx=speed
                    else: vx=0
                if event.key == pygame.K_RIGHT:
                    key_pressed[1] = False
                    if key_pressed[0]: vx=-speed
                    else: vx=0
                if event.key == pygame.K_UP:
                    key_pressed[2] = False
                    if key_pressed[3]: vy=speed
                    else: vy=0
                if event.key == pygame.K_DOWN:
                    key_pressed[3] = False
                    if key_pressed[2]: vy=-speed
                    else: vy=0
            player.move(vx,vy)
            coll.move()
            if collision_detect(player, coll):
                GAMEOVER=True
                player.kill()
                pygame.mixer.music.stop()


        main_clock.tick(1500)
        screen.blit(bg, (0,0))

        # Redibujamos los colliders.
        coll.draw(screen)

        player.update(screen)
        
        # Regeneramos los colliders.
        coll.re_add()

        pygame.display.update()



    pygame.quit()




main()