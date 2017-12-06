
import pygame
import random
import sys
import csv
import controller as ctrl
from pygame.locals import *

# Dimensiones de la pantalla de juego.
SCREEN_WIDTH=600
SCREEN_HEIGHT=900


# Tamaño de la fuente.
FONT_SIZE = 40

# Volumen de los sonidos.
SOUND_VOLUME=0.0

# Dificutlad
ENEMIES=15
POINTS=5

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
    explosion=ctrl.load_image(".\\images\\explosion.png", True)
    ship=ctrl.load_image(".\\images\\ship.png", True)
    if len(sys.argv) != 2:
        print("Número de parámetros incorrecto. Help: python main.py <username>")
        return 1
    else:
        player=ctrl.Player(sys.argv[1],ship, explosion, movement_sound, 1)

    # Creación de los corazones de la vida.
    heart_image=ctrl.load_image(".\\images\\hearts.png", True)
    hearts=ctrl.HeartController(heart_image)

    # Creación del fondo.
    bg=ctrl.load_image(".\\images\\background.jpg").convert_alpha()
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH,SCREEN_HEIGHT))

    # Creación de los colliders del juego.
    meteorite=ctrl.load_image(".\\images\\meteorite.png", True)
    points=ctrl.load_image(".\\images\\points.jpg", True)
    coll=ctrl.Colliders(meteorite, points, ENEMIES, POINTS)
    main_clock = pygame.time.Clock()


    # Creamos la fuente de texto del juego.
    default_font = pygame.font.Font(None, FONT_SIZE)

    # Creamos la puntuación.
    mark = ctrl.MarkController(default_font)
    exit= False
    
    # Creamos el gameover
    gameover = ctrl.GameOver(screen, player, default_font)
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
            if ctrl.collision_detect(player, coll, mark, hearts):
                if hearts.GAMEOVER:
                    gameover.kill(player, mark.mark)


        main_clock.tick(1500)
        screen.blit(bg, (0,0))

        # Redibujamos los colliders.
        coll.draw(screen)

        player.update(screen)
        hearts.update(screen)
        mark.update(screen, hearts.GAMEOVER)                            
        gameover.update(screen)
        
        # Regeneramos los colliders.
        coll.re_add()

        # Hacemos blit del texto que muestra el tiempo de juego.
        screen.blit(time, (0,0))       

        pygame.display.update()



    pygame.quit()




main()