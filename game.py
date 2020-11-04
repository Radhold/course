import pygame
import random
import os


def load_image(name, scaleX=-1, scaleY=-1, colorKey=None, ):
    path = os.path.join('sprites', name)
    image = pygame.image.load(path)
    image = image.convert()
    if colorKey is not None:
        if colorKey is -1:
            colorKey = image.get_at((0, 0))
        image.set_colorkey(colorKey)
    else:
        image = image.convert_alpha()
    if scaleX != -1 or scaleY != -1:
        image = pygame.transform.scale(image, (scaleX, scaleY))
    return image, image.get_rect()


def load_sprite_sheet(sheetName, cols, rows, scaleX=-1, scaleY=-1, colorKey=None):
    fullname = os.path.join('sprites', sheetName)
    sheet = pygame.image.load(fullname)
    sheet = sheet.convert()
    sheet_rect = sheet.get_rect()
    sprites = []
    sizeX = sheet_rect.width / cols
    sizeY = sheet_rect.height / rows

    for i in range(0, rows):
        for j in range(0, cols):
            rect = pygame.Rect((j * sizeX, i * sizeY, sizeX, sizeY))
            image = pygame.Surface(rect.size)
            image = image.convert()
            image.blit(sheet, (0, 0), rect)
            if colorKey is not None:
                if colorKey is -1:
                    colorKey = image.get_at((0, 0))
                image.set_colorkey(colorKey)
            else:
                image = image.convert_alpha()
            if scaleX != -1 or scaleY != -1:
                image = pygame.transform.scale(image, (scaleX, scaleY))
            sprites.append(image)

    sprite_rect = sprites[0].get_rect()

    return sprites, sprite_rect


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
