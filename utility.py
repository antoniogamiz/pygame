import pygame

def load_image(filename, transparent=False):
    image = pygame.image.load(filename)
    image = image.convert()
    if transparent:
        color = image.get_at((0,0))
        image.set_colorkey(color, RLEACCEL)
    return image

class square:
    def __init__(self, x, y, side, colour, bg_c):
        self.x=x
        self.y=y
        self.side=side
        self.colour=colour
        self.bg_c=bg_c
        self.rect = pygame.Rect(self.x, self.y, self.side, self.side)

    def __draw(self, screen, colour):
        pygame.draw.rect(screen, colour, self.rect, 0)

    def draw(self, screen):
        self.__draw(screen, self.colour)

    def delete(self, screen):
        self.__draw(screen, self.bg_c)

    def colisiona_con(self, cuadrado2):
        return self.rect.colliderect(cuadrado2.rect)

    def move(self, x, y):
        self.rect.move_ip(x, y)

    def move_p(self, screen, x, y):
        self.delete(screen)
        rect_init = self.rect.copy()
        self.move(x, y)
        rect_final = self.rect.copy()
        self.draw(screen)
        pygame.display.update(rect_final.union(rect_init))