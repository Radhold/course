import pygame
import random
import os


def load_image(name, scaleX=-1, scaleY=-1, colorKey=None):
    path = os.path.join('sprites', name)
    image = pygame.image.load(path)
    image = image.convert()
    if colorKey is not None:
        if colorKey == -1:
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
                if colorKey == -1:
                    colorKey = image.get_at((0, 0))
                image.set_colorkey(colorKey)
            else:
                image = image.convert_alpha()
            if scaleX != -1 or scaleY != -1:
                image = pygame.transform.scale(image, (scaleX, scaleY))
            sprites.append(image)

    sprite_rect = sprites[0].get_rect()

    return sprites, sprite_rect


class Player:
    def __init__(self, sizeX=-1, sizeY=-1):
        # self.images =
        self.rect = pygame.Rect((0, 0, 30, 30))
        self.rect.bottom = int(0.98 * height)
        self.rect.left = width / 15
        # self.image = self.images[0]
        self.index = 0
        self.counter = 0
        self.score = 0
        self.isJumping = False
        self.isDead = False
        self.isAttack = False
        self.movement = [0, 0]
        self.jumpSpeed = 15

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

    def checkbound(self):
        if self.rect.bottom > int(0.98 * height):
            self.rect.bottom = int(0.98 * height)
            self.isJumping = False

    def update(self):
        if self.isJumping:
            self.movement[1] = self.movement[1] + gravity

        if self.isJumping:
            pass
        elif self.isAttack:
            pass
        elif self.isDead:
            pass
        else:
            pass

        self.rect = self.rect.move(self.movement)
        self.checkbound()
        if not self.isDead and self.counter % 5 == 4:
            self.score += 1
        self.counter = (self.counter + 1)


class Barrier(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizeX=-1, sizeY=-1):
        super().__init__(self.containers)
        self.containers = None
        self.image, self.rect = load_image('obs.png', sizeX, sizeY)
        self.rect.bottom = int(0.98 * height)
        self.rect.left = width + self.rect.width
        self.movement = [-1 * speed, 0]

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()


pygame.init()
clock = pygame.time.Clock()
scrSize = width, height = 600, 200
fps = 60
gravity = 1
background_col = 0, 207, 255
screen = pygame.display.set_mode(scrSize)
pygame.display.set_caption("Run, Vasya, run")


def gameplay():
    gamespeed = 5
    player = Player()
    barrier = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()
    Barrier.containers = barrier
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player.rect.bottom == int(0.98 * height):
                        player.isJumping = True
                        player.movement[1] = -1 * player.jumpSpeed

        for b in barrier:
            b.movement[0] = -1 * gamespeed
            if pygame.sprite.collide_rect(player, b):
                player.isDead = True

        if len(barrier) < 2:
            print(len(barrier))
            if len(barrier) == 0:
                last_obstacle.empty()
                last_obstacle.add(Barrier(gamespeed, 20, 40))
            else:
                for i in last_obstacle:
                    if i.rect.right < width * 0.7 and random.randrange(0, 50) == 10:
                        last_obstacle.empty()
                        last_obstacle.add(Barrier(gamespeed, 20, 40))

        player.update()
        barrier.update()
        screen.fill(background_col)
        barrier.draw(screen)
        player.draw()
        pygame.display.update()
        clock.tick(fps)

        if player.isDead:
            running = False
    pygame.quit()


gameplay()
