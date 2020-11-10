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


def extractdigits(number, length):
    if number > -1:
        digits = []
        while number / 10 != 0:
            digits.append(number % 10)
            number = int(number / 10)

        digits.append(number % 10)
        for i in range(len(digits), length):
            digits.append(0)
        digits.reverse()
        return digits


def displayMessage(image, x, y):
    rect = image.get_rect()
    rect.centerx = x
    rect.top = y
    screen.blit(image, rect)


def healthDamage(hNow, hCount):
    healthCopy = pygame.sprite.Group()
    for i in range(hNow):
        healthCopy.add(Health(30, 30, width / 18 + i * width / 18))
    for j in range(hCount - hNow):
        healthCopy.add(Health(30, 30, (len(healthCopy) + 1) * (width / 18), True))
    group = healthCopy
    return group


class Player(pygame.sprite.Sprite):
    def __init__(self, sizeX=-1, sizeY=-1):
        super().__init__()
        self.images, self.rect = load_sprite_sheet('run.png', 4, 1, sizeX, sizeY)
        self.imagesJump, self.rectJump = load_sprite_sheet('jump.png', 2, 1, sizeX, sizeY)
        self.imagesDamage, self.rectDamage = load_sprite_sheet('damage.png', 4, 1, sizeX, sizeY)
        self.rect.bottom = int(0.84 * height)
        self.rect.left = width / 18
        self.image = self.images[0]
        self.index = 0
        self.counter = 0
        self.score = 0
        self.isJumping = False
        self.isDead = False
        self.isAttack = False
        self.isDamaged = False
        self.movement = [0, 0]
        self.jumpSpeed = 15

    def draw(self):
        screen.blit(self.image, self.rect)

    def checkbound(self):
        if self.rect.bottom > int(0.84 * height):
            self.rect.bottom = int(0.84 * height)
            self.isJumping = False

    def update(self):
        if self.isJumping:
            self.movement[1] += gravity

        if self.isJumping and self.isDamaged is not True:
            if self.movement[1] < 0:
                self.index = 0
            else:
                self.index = 1
        elif self.isAttack:
            pass
        elif self.isDead:
            pass
        elif self.isDamaged:
            if self.counter % 8 == 0:
                self.index = (self.index + 1) % 4
        else:
            if self.counter % 8 == 0:
                self.index = (self.index + 1) % 4

        if self.isJumping and self.isDamaged is not True:
            self.image = self.imagesJump[self.index]
        elif self.isAttack:
            pass
        elif self.isDead:
            pass
        elif self.isDamaged:
            self.image = self.imagesDamage[self.index]
        else:
            self.image = self.images[self.index]

        self.rect = self.rect.move(self.movement)
        self.checkbound()
        if not self.isDead and self.counter % 7 == 6:
            self.score += 1
        self.counter = (self.counter + 1)


class Barrier(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizeX=-1, sizeY=-1):
        super().__init__(self.containers)
        self.containers = None
        self.image, self.rect = load_image('obs.png', sizeX, sizeY)
        self.rect.bottom = int(0.84 * height)
        self.rect.left = width + self.rect.width
        self.movement = [-1 * speed, 0]
        self.speed = speed

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.movement[0] = -1 * self.speed
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizeX=-1, sizeY=-1):
        super().__init__(self.containers)
        self.containers = None
        self.images, self.rect = load_sprite_sheet('coin.png', 5, 2, sizeX, sizeY)
        self.rect.centery = random.randrange(height * 0.42, height * 0.64)
        self.rect.left = width + self.rect.width
        self.image = self.images[0]
        self.movement = [-1 * speed, 0]
        self.index = 0
        self.counter = 0
        self.speed = speed

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        if self.counter % 10 == 0:
            self.index = (self.index + 1) % 10
        self.image = self.images[self.index]
        self.movement[0] = -1 * self.speed
        self.rect = self.rect.move(self.movement)
        self.counter += 1
        if self.rect.right < 0:
            self.kill()


class Ground:
    def __init__(self, speed):
        self.speed = speed
        self.image, self.rect = load_image('ground.png', width, int(height * 0.18))
        self.image1, self.rect1 = load_image('ground.png', width, int(height * 0.18))
        self.rect.bottom = height
        self.rect1.bottom = height
        self.rect1.left = self.rect.right - self.speed

    def draw(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.image1, self.rect1)

    def update(self):
        self.rect.left -= self.speed
        self.rect1.left -= self.speed

        if self.rect.right < 0:
            self.rect.left = self.rect1.right - self.speed

        if self.rect1.right < 0:
            self.rect1.left = self.rect.right - self.speed


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(self.containers)
        self.containers = None
        self.images, self.rect = load_sprite_sheet('clouds.png', 2, 2, 100, 40)
        self.image = self.images[random.randrange(0, 4)]
        self.speed = 1
        self.rect.left = width
        self.rect.top = random.randrange(height / 4, height / 2)
        self.movement = [-1 * self.speed, 0]

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()


class Health(pygame.sprite.Sprite):
    def __init__(self, sizeX=-1, sizeY=-1, left=-1, dead=False):
        super().__init__(self.containers)
        self.containers = None
        self.images, self.rect = load_sprite_sheet('health.png', 4, 2, sizeX, sizeY)
        self.emptyImage, self.rect1 = load_image('emptyHealth.png', sizeX, sizeY)
        self.rect.top = int(0.09 * height)
        self.rect.left = left
        self.image = self.images[0]
        self.index = 0
        self.counter = 0
        self.dead = dead

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        if self.dead:
            self.image = self.emptyImage
        else:
            if self.counter % 8 == 0:
                self.index = (self.index + 1) % 8
            self.image = self.images[self.index]
            self.counter += 1


class Scoreboard:
    def __init__(self, x=-1, y=-1, length=5):
        self.digits, self.digitRect = load_sprite_sheet('digits.png', 10, 1, 11, int(11 * 6 / 5))
        self.image = pygame.Surface((55, int(11 * 6 / 5)))
        self.rect = self.image.get_rect()
        self.length = length
        if x == -1:
            self.rect.left = width * 0.89
        elif x == 0:
            self.rect.centerx = width / 2
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = height * 0.1
        else:
            self.rect.top = y

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self, score):
        scoreDigits = extractdigits(score, self.length)
        self.image.fill(backgroundCol)
        for s in scoreDigits:
            self.image.blit(self.digits[s], self.digitRect)
            self.digitRect.left += self.digitRect.width
        self.digitRect.left = 0


pygame.init()
clock = pygame.time.Clock()
scrSize = width, height = 600, 200
fps = 60
gravity = 1
backgroundCol = 0, 207, 255
highScore = 0
screen = pygame.display.set_mode(scrSize)
pygame.display.set_caption("Running Viking")


def gameplay():
    gameSpeed = 5
    counter = 0
    gameOver = False
    healthCount = 3
    healthCountNow = healthCount
    gameQuit = False
    gameWaiting = False
    objDamaged = None
    coinsCount = 5
    scb = Scoreboard()
    highScb = Scoreboard(width * 0.78)
    coinsScb = Scoreboard(0, height * 0.13, 2)
    player = Player()
    ground = Ground(gameSpeed)

    barrier = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    health = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()

    Barrier.containers = barrier
    Coin.containers = coins
    Cloud.containers = clouds
    Health.containers = health

    tempCoin = Coin(0, 30, 30)
    tempCoin.rect.centerx = width / 2 - 50
    tempCoin.rect.top = height * 0.09

    continueImage, continueRect = load_image('continue.png', 183, 13)
    replayImage, replayRect = load_image('replay.png', 35, 31)
    acceptImage, acceptRect = load_image('accept.png', 35, 31)
    exitImage, exitRect = load_image('exit.png', 35, 31)
    while not gameQuit:
        while not gameOver:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if player.rect.bottom == int(0.84 * height):
                            player.isJumping = True
                            player.movement[1] = -1 * player.jumpSpeed

            for b in barrier:
                if pygame.sprite.collide_mask(player, b) and player.isDamaged is not True:
                    player.isDamaged = True
                    objDamaged = b
                    healthCountNow -= 1
                    health = healthDamage(healthCountNow, healthCount)

            if player.isDamaged is True:
                if objDamaged.rect.right < player.rect.left:
                    player.isDamaged = False

            for c in coins:
                if pygame.sprite.collide_mask(player, c) and c is not tempCoin:
                    coinsCount += 1
                    c.kill()

            if len(health) < 3:
                for i in range(healthCount):
                    health.add(Health(30, 30, (width / 18 + i * width / 18)))

            if len(barrier) < 2:
                if len(barrier) == 0:
                    last_obstacle.empty()
                    last_obstacle.add(Barrier(gameSpeed, 36, 38))
                else:
                    for i in last_obstacle:
                        if i.rect.right < width * 0.7 and random.randrange(0, 50) == 10:
                            last_obstacle.empty()
                            last_obstacle.add(Barrier(gameSpeed, 36, 38))

            if random.randrange(0, 10) == 5 and counter > 50:
                for i in last_obstacle:
                    if i.rect.right < width * 0.7:
                        last_obstacle.empty()
                        last_obstacle.add(Coin(gameSpeed, 30, 30))

            if len(clouds) < 5 and random.randrange(0, 600) == 10:
                Cloud()

            health.update()
            clouds.update()
            player.update()
            ground.update()
            barrier.update()
            coins.update()
            scb.update(player.score)
            coinsScb.update(coinsCount)
            highScb.update(highScore)
            screen.fill(backgroundCol)
            tempCoin.draw()
            health.draw(screen)
            clouds.draw(screen)
            player.draw()
            ground.draw()
            coins.draw(screen)
            barrier.draw(screen)
            scb.draw()
            if highScore != 0:
                highScb.draw()
            coinsScb.draw()
            pygame.display.update()
            clock.tick(fps)
            counter += 1

            if healthCountNow == 0:
                if coinsCount > 3:
                    gameWaiting = True
                    gameOver = True
                else:
                    print(9)
                    highScb.update(highScore)
                    player.isDead = True
            if player.isDead:
                gameQuit = True
                gameOver = True

        if gameQuit:
            break

        while gameWaiting:

            print(1)
            for event in pygame.event.get():
                print(0)
                if event.type == pygame.QUIT:
                    print(2)
                    gameQuit = True
                    gameOver = False
                    gameWaiting = False
                if event.type == pygame.KEYDOWN:
                    print(3)
                    if event.key == pygame.K_ESCAPE:
                        gameQuit = True
                        print(4)
                        gameOver = False
                        gameWaiting = False
                    if event.key == pygame.K_SPACE:
                        print(7)
                        gameWaiting = False
                        gameOver = False
                        coinsCount -= 3
                        healthCountNow += 1
                        health = healthDamage(healthCountNow, healthCount)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    print(6)
                    if acceptRect.collidepoint(pos):
                        print(7)
                        gameWaiting = False
                        gameOver = False
                        coinsCount -= 3
                        healthCountNow += 1
                        health = healthDamage(healthCountNow, healthCount)
                    elif exitRect.collidepoint(pos):
                        gameQuit = True
                        gameOver = False
                        gameWaiting = False
                        print(8)
            displayMessage(continueImage, width / 2, height * 0.4)
            displayMessage(acceptImage, width / 2 - 30, height * 0.6)
            displayMessage(exitImage, width / 2 + 30, height * 0.6)
            pygame.display.update()
            clock.tick(fps)

    pygame.quit()


gameplay()
