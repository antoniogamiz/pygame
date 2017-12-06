
import pygame
import random
import sys
import csv
from pygame.locals import *

# Dimensiones de la pantalla de juego.
SCREEN_WIDTH=600
SCREEN_HEIGHT=900

# COLORES
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)

# Tamaño de la fuente.
FONT_SIZE = 40

# Volumen de los sonidos.
SOUND_VOLUME=0.0

# Dificutlad
ENEMIES=15
POINTS=5


def mark_table(surface, entry):
    

#Función que gestiona el gameover.
def gameover(surface, player):
    player.kill()
    pygame.mixer.music.stop()
    with open('.\\data\\marks.csv') as csv_file:
        entry=csv.reader(csv_file)
        entry=list(entry)
    mark_table(surface, entry)

# Función auxiliar para cargar imágenes (con transparencia si se quiere)
def load_image(filename, transparent=False):
    image = pygame.image.load(filename)
    image = image.convert()
    if transparent:
        color = image.get_at((0,0))
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
def collision_detect(player, colliders, mark, heart):
    for ent in colliders.list:
        if player.rect.colliderect(ent.rect):
            ent.touched=True
            if ent.enemy:
                heart.kill()
            else:
                mark.up()
            return True
    return False

class Entity(pygame.sprite.Sprite):
    def __init__(self, image, rect, enemy, touched):
        self.image=pygame.transform.scale(image, (50,50))
        self.rect=rect
        self.enemy=enemy
        self.touched=touched

class Colliders(object):
    def __init__(self, enemy_image, points_image, enemy_num, points_num):
        self.SPEED=1
        self.list=[]
        for x in range(enemy_num):
            self.list.append(Entity(enemy_image, pygame.Rect(random_rect_coord_generate(2, SCREEN_WIDTH, -400, -20, 49, 50, 49, 50)), True, False))
        for x in range(points_num):
            self.list.append(Entity(points_image, pygame.Rect(random_rect_coord_generate(2, SCREEN_WIDTH, -400, -20, 49, 50, 49, 50)), False, False))
    def re_add(self):
        for x in range(len(self.list)):
            if self.list[x].rect.top > SCREEN_HEIGHT:
                self.list[x].rect=pygame.Rect(random_rect_coord_generate(2, SCREEN_WIDTH, -400, -20,49, 50, 49, 50))
                self.list[x].touched=False
    def move(self):
        for ent in self.list:
            ent.rect.move_ip(0, self.SPEED)
    def draw(self, surface):
        for ent in self.list:
            if not ent.touched:
                surface.blit(ent.image, ent.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self, image, explosion_image, movement_sound, SPEED):
        self.SPEED=SPEED
        self.movement_sound=movement_sound
        self.image=image.subsurface(270,120,400,550)
        self.explosion_image=explosion_image.subsurface(70,115,90,60)
        self.image=pygame.transform.scale(self.image, (50,50))
        self.rect=self.image.get_rect()
        self.rect.top=SCREEN_HEIGHT-200
        self.rect.left=SCREEN_WIDTH/2 - 50
        self.explosion_image=pygame.transform.scale(self.explosion_image, (50,50))
    def move(self, vx, vy):
        self.rect.move_ip(vx,vy)
    def kill(self):
        self.image = self.explosion_image
    def movement_play(self):
        self.movement_sound.play()
    def update(self, surface):
        surface.blit(self.image, self.rect)


class HeartController(pygame.sprite.Sprite):
    def __init__(self, image):
        # self.damage_sound=damage_sound
        self.image=pygame.transform.scale(image,(25,25))
        self.hearts=[]
        self.rects=[]
        self.ticks=0
        self.hurt=False
        self.CURRENT_LIFE=3
        self.GAMEOVER=False
        for x in range(self.CURRENT_LIFE):
            self.hearts.append(self.image)
            self.rects.append([130+x*25, 0, 25, 25])
    def kill(self):
        if not self.hurt:
            self.hurt=True
            self.ticks=pygame.time.get_ticks()
            if self.CURRENT_LIFE > 0:
                self.CURRENT_LIFE= self.CURRENT_LIFE - 1
            if self.CURRENT_LIFE == 0:
                self.GAMEOVER = True

    def update(self, surface):
        if self.hurt:
            if pygame.time.get_ticks() - self.ticks > 500:
                self.hurt=False
        for x in range(self.CURRENT_LIFE):
            surface.blit(self.hearts[x], self.rects[x])

class MarkController:
    def __init__(self, font):
        self.font=font
        self.mark=0
        self.points=0
        self.touch=False
    def up(self):
        if not self.touch:
            self.touch=True
            self.ticks=pygame.time.get_ticks()
            self.points=self.points+50
    def update(self,surface, gameover):
        if self.touch:
            if pygame.time.get_ticks() - self.ticks > 500:
                self.touch=False
        if gameover:
            k=str(self.mark)
        else:
            k=int(pygame.time.get_ticks()/1000)
            k=str(k+self.points)
            self.mark=k
        surface.blit(self.font.render("Mark: "+k, 0, (255,0,0)), (425,0)) 

def main():

    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
    pygame.display.set_caption("Acnologia")

    # Cargamos la música de fondo.
    pygame.mixer.music.load(".\\music\\background_music.mp3")
    movement_sound=pygame.mixer.Sound(".\\music\\movement_sound.wav")
    movement_sound.set_volume(SOUND_VOLUME)

    # Variables auxiliares para el control del movimiento.
    vx,vy = 0,0
    # LEFT, RIGHT, UP, DOWN
    key_pressed = [False, False, False, False]

    # Creación del player.
    explosion=load_image(".\\images\\explosion.png", True)
    ship=load_image(".\\images\\ship.png", True)
    player=Player(ship, explosion, movement_sound, 1)

    # Creación de los corazones de la vida.
    heart_image=load_image(".\\images\\hearts.png", True)
    hearts=HeartController(heart_image)

    # Creación del fondo.
    bg=load_image(".\\images\\background.jpg").convert_alpha()
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH,SCREEN_HEIGHT))

    # Creación de los colliders del juego.
    meteorite=load_image(".\\images\\meteorite.png", True)
    points=load_image(".\\images\\points.jpg", True)
    coll=Colliders(meteorite, points, ENEMIES, POINTS)
    main_clock = pygame.time.Clock()


    # Creamos la fuente de texto del juego.
    default_font = pygame.font.Font(None, FONT_SIZE)

    # Creamos la puntuación.
    mark = MarkController(default_font)
    exit= False
    
    # Reproducimos la música de fondo.
    pygame.mixer.music.play(2)
    pygame.mixer.music.set_volume(SOUND_VOLUME)



    while not exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
        if not hearts.GAMEOVER:
            # Actualizamos el tiempo de juego mientras el jugador no haya perdido.
            time = default_font.render("Time: "+str(int(pygame.time.get_ticks()/1000)), 0, (255,0,0))
            #Gestión del movimiento de 'player'.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    key_pressed[0] = True
                    vx=-player.SPEED
                if event.key == pygame.K_RIGHT:
                    key_pressed[1] = True
                    vx=player.SPEED
                if event.key == pygame.K_UP:
                    key_pressed[2] = True
                    vy=-player.SPEED
                if event.key == pygame.K_DOWN:
                    key_pressed[3] = True
                    vy=player.SPEED
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    key_pressed[0] = False
                    if key_pressed[1]: vx=player.SPEED
                    else: vx=0
                if event.key == pygame.K_RIGHT:
                    key_pressed[1] = False
                    if key_pressed[0]: vx=-player.SPEED
                    else: vx=0
                if event.key == pygame.K_UP:
                    key_pressed[2] = False
                    if key_pressed[3]: vy=player.SPEED
                    else: vy=0
                if event.key == pygame.K_DOWN:
                    key_pressed[3] = False
                    if key_pressed[2]: vy=-player.SPEED
                    else: vy=0
            player.move(vx,vy)
            coll.move()
            if collision_detect(player, coll, mark, hearts):
                if hearts.GAMEOVER:
                    gameover(screen, player)


        main_clock.tick(1500)
        screen.blit(bg, (0,0))

        # Redibujamos los colliders.
        coll.draw(screen)

        player.update(screen)
        hearts.update(screen)
        mark.update(screen, hearts.GAMEOVER)                            
        # Regeneramos los colliders.
        coll.re_add()

        # Hacemos blit del texto que muestra el tiempo de juego.
        screen.blit(time, (0,0))       

        pygame.display.update()



    pygame.quit()




main()