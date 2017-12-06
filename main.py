
import pygame
import random
import sys
import csv
import controller as ctrl
from pygame.locals import *

# Dimensiones de la pantalla de juego.
SCREEN_WIDTH=600
SCREEN_HEIGHT=900

# Tiempo límite.
LIMIT_TIME=60

# Tamaño de la fuente.
FONT_SIZE = 40

# Volumen de los sonidos.
SOUND_VOLUME=0.1

# Dificutlad
ENEMIES=15
POINTS=5

def main():

    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
    pygame.display.set_caption("Naves Espaciales")

    # Cargamos la música de fondo.
    pygame.mixer.music.load(".\\music\\background_music.mp3")
    
    # Reproducimos la música de fondo.
    pygame.mixer.music.play(1) # La duración máxima de la partida es 1 minuto, así que con 1 loop es suficiente.
    pygame.mixer.music.set_volume(SOUND_VOLUME)

    # Variables auxiliares para el control del movimiento.
    vx,vy = 0,0
    # LEFT, RIGHT, UP, DOWN
    key_pressed = [False, False, False, False]

    # Creamos a 'player' (Se le pasa como argumento al archivo un nombre de usuario, si no se le pasa, finaliza la ejecución)
    explosion=ctrl.load_image(".\\images\\explosion.png", True)
    ship=ctrl.load_image(".\\images\\ship.png", True)
    if len(sys.argv) != 2:
        print("Número de parámetros incorrecto. Help: python main.py <username>")
        return 1
    else:
        player=ctrl.Player(sys.argv[1],ship, explosion, 1)

    # Creamos la barra de vida.
    heart_image=ctrl.load_image(".\\images\\hearts.png", True)
    hearts=ctrl.HeartController(heart_image)

    # Creamos el fondo.
    bg=ctrl.load_image(".\\images\\background.jpg").convert_alpha()
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH,SCREEN_HEIGHT))

    # Creamos los objetos móviles del juego (enemigos y no-enemigos).
    meteorite=ctrl.load_image(".\\images\\meteorite.png", True)
    points=ctrl.load_image(".\\images\\points.jpg", True)
    coll=ctrl.Colliders(meteorite, points, ENEMIES, POINTS)

    # Iniciamos el reloj.
    main_clock = pygame.time.Clock()


    # Creamos una fuente de texto para el juego.
    default_font = pygame.font.Font(None, FONT_SIZE)

    # Creamos la puntuación.
    mark = ctrl.MarkController(default_font)

    exit= False
    
    # Creamos el gameover
    gameover = ctrl.GameOver(screen, player, default_font)

    while not exit:
        for event in pygame.event.get():
            # Cierre del juego.
            if event.type == pygame.QUIT:
                exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
        if not hearts.GAMEOVER:
            # Actualizamos el tiempo de juego mientras el jugador no haya perdido.
            time_=int(pygame.time.get_ticks()/1000)
            time = default_font.render("Time: "+str(LIMIT_TIME-time_), 0, (255,0,0))
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
            # Movemos a player y a los objetos móviles.
            player.move(vx,vy)
            coll.move()
            # Comprobámos las colisiones.
            if ctrl.collision_detect(player, coll, mark, hearts):
                if hearts.GAMEOVER:
                    gameover.kill(player, mark.mark)
            # Tiempo límite.
            if time_ > LIMIT_TIME:
                gameover.kill(player, mark.mark)

        main_clock.tick(1500)

        # Fijamos el fondo.
        screen.blit(bg, (0,0))

        # Redibujamos los colliders.
        coll.draw(screen)

        # Actualizamos los objetos en pantalla.
        player.update(screen)
        hearts.update(screen)
        mark.update(screen, hearts.GAMEOVER)                            
        gameover.update(screen)
        
        # Regeneramos los objetos móviles.
        coll.re_add()

        # Hacemos blit del texto que muestra el tiempo de juego.
        screen.blit(time, (0,0))       

        pygame.display.update()



    pygame.quit()




main()