import pygame
import random
import sys
import csv
from pygame.locals import *

# Dimensiones de la pantalla de juego.
SCREEN_WIDTH=600
SCREEN_HEIGHT=900
ENTITY_SIZE=50

#-----------------------------------FUNCIONES AUXILIARES-----------------------------------

# Función auxiliar para cargar imágenes (con transparencia si se quiere)
def load_image(filename, transparent=False):
    image = pygame.image.load(filename)
    image = image.convert()
    if transparent:
        color = image.get_at((0,0))
        image.set_colorkey(color, RLEACCEL)
    return image

# Genera una posicion aleatoria (l_random, t_random), (l_min, l_max) cota de la x (t_min, t_max) cota de la y.
def random_rect_coord_generate(l_min, l_max, t_min, t_max):
    l_random=random.randrange(l_min, l_max)
    t_random=random.randrange(t_min, t_max)
    return [l_random, t_random]

#-----------------------------------CLASES QUE CONTROLAN EL JUEGO-----------------------------------

# Encargada de gestionar el ranking (crearlo, actulizarlo, y guardarlo), de parar el juego y la música.
class GameOver:
    # Creamos el 'gameover' cargando el ranking anterior a la partida.
    def __init__(self,surface, player, font):
        self.font=font
        self.GAMEOVER=False
        with open('./data/marks.csv') as csv_file:    # En el archivo marks.csv guardamos el ranking en formato csv.
            entry=csv.reader(csv_file)
            self.entry=list(entry)
        self.players=[]
        self.players.append(self.font.render("GAMEOVER", 0, (255,0,0))) # Añadimos la cabecera.
    # Paramos el juego, la música y actualizamos el ranking.
    def kill(self,player, mark):
        self.GAMEOVER=True
        player.kill()
        pygame.mixer.music.stop()
        self.calculateRank(player.username, mark)   # Actualizamos el ranking.
        out_csv = open('./data/marks.csv', 'w', newline='')
        out = csv.writer(out_csv)
        out.writerows(self.entry)   # Y lo escribimos.
        del out
        out_csv.close()
    # Recalculamos el ranking dependiendo de la puntuación (mark) que haya obtenido el jugador y creamos los renders de texto  necesarios para mostrarlo.
    def calculateRank(self, username, mark):
        for x in range(5):
            if int(mark) > int(self.entry[x][1]):
                self.entry.pop(x)
                self.entry.insert(x, [username, mark])
                break
        for x in range(5):
            self.players.append(self.font.render(self.entry[x][0]+"     "+str(self.entry[x][1]), 0, (255,0,0)))
    # Refrescamos el ranking en cada frame.
    def update(self, surface):
        if self.GAMEOVER:
            for x in range(6):
                surface.blit(self.players[x], (SCREEN_WIDTH/3,SCREEN_HEIGHT/3+x*30))

# Detecta si 'player' colisiona con alguno de los colliders en pantalla.
def collision_detect(player, colliders, mark, heart):
    for ent in colliders.list:
        if player.rect.colliderect(ent.rect):
            ent.touched=True    # Lo marcamos como tocado para no volver a refrescarlo.
            if ent.enemy:   # Si es un enemigo, quitamos vida.
                heart.kill()
            else:
                mark.up()   # Si no, aumentamos la puntuación.
            return True
    return False

# Clase que hereda la estructura de Sprite para representar los objetos que se mueven por pantalla.
class Entity(pygame.sprite.Sprite):
    def __init__(self, image, rect, enemy, touched):
        self.image=pygame.transform.scale(image, (50,50))
        self.rect=rect
        self.enemy=enemy    # Si es enemigo o no.
        self.touched=touched    # Si player ha colisionado con él o no.

# Gestiona el movimiento, la colisión y el re-spawn de los objetos que se mueven por pantalla.
class Colliders(object):
    def __init__(self, enemy_image, points_image, enemy_num, points_num, SPEED):
        self.SPEED=SPEED    # Velocidad a la que se mueven los objetos.
        self.list=[]    # Aquí se almacenan todos los objetos móviles de la pantalla (excepto player)
        for x in range(enemy_num):  # Creamos los enemigos.
            tupla=random_rect_coord_generate(2, SCREEN_WIDTH, -400, -20)
            tupla.append(ENTITY_SIZE)
            tupla.append(ENTITY_SIZE)
            self.list.append(Entity(enemy_image, pygame.Rect(tupla), True, False))
        for x in range(points_num): # Creamos los no-enemigos.
            tupla=random_rect_coord_generate(2, SCREEN_WIDTH, -400, -20)
            tupla.append(ENTITY_SIZE)
            tupla.append(ENTITY_SIZE)
            self.list.append(Entity(points_image, pygame.Rect(tupla), False, False))
    # Cuando un objeto móvil llega al final de la pantalla lo re-spawnea.
    def re_add(self):
        for x in range(len(self.list)):
            if self.list[x].rect.top > SCREEN_HEIGHT:
                tupla=random_rect_coord_generate(2, SCREEN_WIDTH, -400, -20)
                tupla.append(ENTITY_SIZE)
                tupla.append(ENTITY_SIZE)
                self.list[x].rect=pygame.Rect(tupla)
                self.list[x].touched=False  # Lo marcamos como no-tocado para que pueda aparecer en pantalla.
    def move(self):
        for ent in self.list:
            ent.rect.move_ip(0, self.SPEED)
    # Sólo dibujamos en pantalla aquellos que no hayan colisionado con player.
    def draw(self, surface):
        for ent in self.list:
            if not ent.touched:
                surface.blit(ent.image, ent.rect)

# Se encarga de crear al jugador, gestionar su movimiento, y de reproducir un sonido cuando se mueve.
class Player(pygame.sprite.Sprite):
    def __init__(self, username, image, explosion_image, SPEED):
        self.username=username
        self.SPEED=SPEED
        self.image=image.subsurface(270,120,400,550)
        self.explosion_image=explosion_image.subsurface(70,115,90,60)
        self.image=pygame.transform.scale(self.image, (50,50))
        self.rect=self.image.get_rect()
        self.rect.top=SCREEN_HEIGHT-200 # Situamos a player más o menos en la parte de abajo de la pantalla.
        self.rect.left=SCREEN_WIDTH/2 - 50
        self.explosion_image=pygame.transform.scale(self.explosion_image, (50,50))  # Imagen de cuando muere.
    def move(self, vx, vy):
        self.rect.move_ip(vx,vy)
    def kill(self):
        self.image = self.explosion_image
    def movement_play(self):
        self.movement_sound.play()
    def update(self, surface):
        surface.blit(self.image, self.rect)

# Se encarga de refrescar los corazones en pantalla y bajar la vida.
class HeartController(pygame.sprite.Sprite):
    def __init__(self, image):
        # self.damage_sound=damage_sound
        self.image=pygame.transform.scale(image,(25,25))
        self.hearts=[]
        self.rects=[]
        self.ticks=0
        self.hurt=False
        self.CURRENT_LIFE=3     # Número total de corazones de 'player'.
        self.GAMEOVER=False
        for x in range(self.CURRENT_LIFE):
            self.hearts.append(self.image)
            self.rects.append([130+x*25, 0, 25, 25])
    def kill(self):
        if not self.hurt:
            self.hurt=True  # Leer update()
            self.ticks=pygame.time.get_ticks()
            if self.CURRENT_LIFE > 0:
                self.CURRENT_LIFE= self.CURRENT_LIFE - 1
            if self.CURRENT_LIFE == 0:
                self.GAMEOVER = True

    def update(self, surface):
        if self.hurt:   # Mecanismo de control para evitar contar una colision más de 1 vez.
            if pygame.time.get_ticks() - self.ticks > 500:
                self.hurt=False
        for x in range(self.CURRENT_LIFE):
            surface.blit(self.hearts[x], self.rects[x])

# Se encarga de la puntuación. Cada segundo que pasa, es un punto más, si player colisiona con un objeto no-enemigo, suma 50 puntos.
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
            if pygame.time.get_ticks() - self.ticks > 500:  # Mismo mecanismo de control que en HeartController.
                self.touch=False
        if gameover:
            k=str(self.mark)
        else:
            k=int(pygame.time.get_ticks()/1000)
            k=str(k+self.points)
            self.mark=k
        surface.blit(self.font.render("Mark: "+k, 0, (255,0,0)), (425,0)) # Renderizamos en cada frame el texto de la puntuación.