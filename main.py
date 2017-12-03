# Importamos la librería
import pygame
import player
import sys

# Importamos constantes locales de pygame
from pygame.locals import *

# Iniciamos Pygame
pygame.init()

# Creamos una surface (la ventana de juego), asignándole un alto y un ancho
Ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

clock = pygame.time.Clock()

# Le ponemos un título a la ventana
pygame.display.set_caption("xEnderCrystalx")

info = pygame.display.Info()

Imagen = pygame.image.load(".\images\monigotillo.png")
transparente = Imagen.get_at((0, 0))
Imagen.set_colorkey(transparente)

MiMonigotillo = player.Monigotillo(Ventana, (300, 200), Imagen)
# Cargamos las imágenes
bg = pygame.image.load(".\images\\background.png")
bg = pygame.transform.scale(bg, (info.current_w, info.current_h))


# Bucle infinito para mantener el programa en ejecución
while True:


    Ventana.blit(bg, (0, 0))
    MiMonigotillo.update(Ventana)
    coord_x=0
    coord_y=0
    coord = (coord_x, coord_y)


    for evento in pygame.event.get():
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                sys.exit()
            if evento.key == pygame.K_RIGHT:
                coord_x=5
            elif evento.key == pygame.K_DOWN:
                coord_y=5
            elif evento.key == pygame.K_LEFT:
                coord_x=-5
            elif evento.key == pygame.K_UP:
                coord_y=-5
            coord=(coord_x, coord_y)
        if evento.type == pygame.KEYUP:
                coord = (0,0)
    MiMonigotillo.update_movement(coord)
    pygame.display.flip()
    clock.tick(30)

