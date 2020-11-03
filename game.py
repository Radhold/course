import pygame
import random
import os


def load_image(name, scaleX=-1, scaleY=-1, colorKey=None,):
    path = os.path.join('sprites', name)
    image = pygame.image.load(path)
    image = image.convert()
    if colorKey is not None:
        if colorKey is -1:
            colorKey = image.get_at((0, 0))
        image.set_colorkey(colorKey)
    if scaleX != -1 or scaleY != -1:
        image = pygame.transform.scale(image, (scaleX, scaleY))
    return (image, image.get_rect())



pygame.init()
scrSize = width, height = 600, 200
FPS = 60
gravity = 1
background_col = 0, 207, 255
screen = pygame.display.set_mode(scrSize)

pygame.display.set_caption("Run, Vasya, run")
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()
