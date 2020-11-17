import pygame
import random
import os


def loadImage(name, scaleX=-1, scaleY=-1, colorKey=None):
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


def loadSpriteSheet(sheetName, cols, rows, scaleX=-1, scaleY=-1, colorKey=None):
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


def displayMessage(image, rect):
    screen.blit(image, rect)


def setCoordinat(rect, x, y):
    rect.centerx = x
    rect.top = y


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
        self.images, self.rect = loadSpriteSheet('run.png', 4, 1, sizeX, sizeY)
        self.imagesJump, self.rectJump = loadSpriteSheet('jump.png', 2, 1, sizeX, sizeY)
        self.imagesDamage, self.rectDamage = loadSpriteSheet('damage.png', 4, 1, sizeX, sizeY)
        self.imagesAttack, self.rectAttack = loadSpriteSheet('attack.png', 7, 1, sizeX, sizeY)
        self.rect.bottom = self.rectAttack.bottom = int(0.84 * height)
        self.rect.left = self.rectAttack.left = width / 18
        self.image = self.images[0]
        self.index = 0
        self.counter = 0
        self.score = 0
        self.isJumping = False
        self.isAttack = False
        self.isDamaged = False
        self.movement = [0, 0]
        self.jumpSpeed = 16

    def draw(self):
        if self.isAttack:
            screen.blit(self.image, self.rectAttack)
        else:
            screen.blit(self.image, self.rect)

    def checkbound(self):
        if self.rect.bottom > int(0.84 * height):
            self.rect.bottom = int(0.84 * height)
            self.isJumping = False

    def checkIndex(self):
        if self.index == 6:
            self.isAttack = False
            self.index = 0

    def update(self):
        if self.isJumping:
            self.movement[1] += gravity

        if self.isJumping and self.isDamaged is False:
            if self.movement[1] < 0:
                self.index = 0
            else:
                self.index = 1
        elif self.isAttack:
            if self.counter % 7 == 0:
                self.index = (self.index + 1) % 7
        elif self.isDamaged:
            if self.counter % 8 == 0:
                self.index = (self.index + 1) % 4
        else:
            if self.counter % 8 == 0:
                self.index = (self.index + 1) % 4

        if self.isJumping and self.isDamaged is False:
            self.image = self.imagesJump[self.index]
        elif self.isAttack:
            if self.index != -1:
                self.image = self.imagesAttack[self.index]
        elif self.isDamaged:
            self.image = self.imagesDamage[self.index]
        else:
            self.image = self.images[self.index]

        self.checkIndex()
        self.rect = self.rect.move(self.movement)
        self.checkbound()
        if self.counter % 5 == 4:
            self.score += 1
        self.counter += 1


class Barrier(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizeX=-1, sizeY=-1):
        super().__init__(self.containers)
        self.containers = None
        self.image, self.rect = loadImage('obs.png', sizeX, sizeY)
        self.rect.bottom = int(0.84 * height)
        self.rect.left = width + self.rect.width
        self.speed = speed
        self.movement = [-1 * self.speed, 0]

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self, speed):
        self.speed = speed
        self.movement[0] = -1 * self.speed
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizeX=-1, sizeY=-1):
        super().__init__(self.containers)
        self.containers = None
        self.images, self.rect = loadSpriteSheet('coin.png', 5, 2, sizeX, sizeY)
        self.rect.centery = random.randrange(height * 0.42, height * 0.64)
        self.rect.left = width + self.rect.width
        self.image = self.images[0]
        self.speed = speed
        self.movement = [-1 * self.speed, 0]
        self.index = 0
        self.counter = 0

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self, speed):
        if self.speed != 0:
            self.speed = speed
        self.movement[0] = -1 * self.speed
        if self.counter % 10 == 0:
            self.index = (self.index + 1) % 10
        self.image = self.images[self.index]
        self.rect = self.rect.move(self.movement)
        self.counter += 1
        if self.rect.right < 0:
            self.kill()


class Ground:
    def __init__(self, speed):
        self.speed = speed
        self.image, self.rect = loadImage('ground.png', width, int(height * 0.18))
        self.image1, self.rect1 = loadImage('ground.png', width, int(height * 0.18))
        self.rect.bottom = height
        self.rect1.bottom = height
        self.rect1.left = self.rect.right - self.speed

    def draw(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.image1, self.rect1)

    def update(self, speed):
        self.speed = speed
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
        self.images, self.rect = loadSpriteSheet('clouds.png', 2, 2, 100, 40)
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
        self.images, self.rect = loadSpriteSheet('health.png', 4, 2, sizeX, sizeY)
        self.emptyImage, self.rect1 = loadImage('emptyHealth.png', sizeX, sizeY)
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
        self.digits, self.digitRect = loadSpriteSheet('digits.png', 10, 1, int(width / 75), int(11 * 6 / 5))
        self.image = pygame.Surface((int(width / 15), int(11 * 6 / 5)))
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


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizeX=-1, sizeY=-1):
        super().__init__(self.containers)
        self.containers = None
        self.images, self.rect = loadSpriteSheet('enemy.png', 6, 1, sizeX, sizeY)
        self.deathImage, self.deathRect = loadImage('enemyDeath.png', sizeX, sizeY)
        self.rect.bottom = self.deathRect.bottom = int(0.84 * height)
        self.rect.left = width + self.rect.width
        self.image = self.images[0]
        self.death = False
        self.speed = int(speed)
        self.movement = [-1 * self.speed, 0]
        self.index = 0
        self.counter = 0
        self.deathCounter = 0
        self.flag = False

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self, speed):
        self.speed = speed
        self.movement[0] = -1 * self.speed
        if self.death and self.flag is False:
            self.deathCounter = self.counter
            deathMusic.play()
            self.flag = True

        if self.death is False and self.counter % 12 == 0:
            self.index = (self.index + 1) % 6
            self.image = self.images[self.index]
        elif self.death:
            self.deathRect.left = self.rect.left
            self.rect = self.deathRect
            self.image = self.deathImage

        self.rect = self.rect.move(self.movement)
        self.counter = (self.counter + 1)
        if self.rect.right < 0 or (self.death and self.counter - self.deathCounter > 9):
            self.kill()


pygame.init()
clock = pygame.time.Clock()
scrSize = width, height = 900, 300
fps = 60
gravity = 1
backgroundCol = 0, 207, 255
screen = pygame.display.set_mode(scrSize)
pygame.display.set_caption("Running Viking")
menuMusic = pygame.mixer.Sound('sounds/menu.wav')
gameMusic = pygame.mixer.Sound('sounds/game.wav')
coinMusic = pygame.mixer.Sound('sounds/coin.wav')
attackMusic = pygame.mixer.Sound('sounds/attack.wav')
hMusic = pygame.mixer.Sound('sounds/100.mp3')
tMusic = pygame.mixer.Sound('sounds/1000.mp3')
deathMusic = pygame.mixer.Sound('sounds/death.mp3')
damageMusic = pygame.mixer.Sound('sounds/damage.mp3')
jumpMusic = pygame.mixer.Sound('sounds/jump.mp3')
global gameQuit


def menu():
    menuMusic.play(-1)
    global gameQuit
    helpCase = False
    gameStart = False
    gameQuit = False
    menuImage, menuRect = loadImage('menu.png', int(width / 12), int(height / 18))
    logoImage, logoRect = loadImage('logo.png', int(width / 2), int(height / 4.5))
    helpImage, helpRect = loadImage('help.png', int(width / 6), int(height / 9))
    helpTextImage, helpTextRect = loadImage('helpText.png', -1, -1)
    startImage, startRect = loadImage('start.png', int(width / 6), int(height / 9))
    exitImage, exitRect = loadImage('exitt.png', int(width / 6), int(height / 9))
    setCoordinat(helpTextRect, width / 2, height - 200)
    setCoordinat(logoRect, width / 2, height * 0.1)
    setCoordinat(helpRect, width / 1.5 - 40, height * 0.5)
    setCoordinat(startRect, width / 2.5 - 20, height * 0.5)
    setCoordinat(exitRect, width / 2, height * 0.75)
    setCoordinat(menuRect, 50, int(height / 10))
    screen.fill(backgroundCol)
    displayMessage(logoImage, logoRect)
    displayMessage(startImage, startRect)
    displayMessage(exitImage, exitRect)
    displayMessage(helpImage, helpRect)
    pygame.display.update()
    while not gameQuit:
        while not gameStart and not gameQuit:
            if pygame.display.get_surface() is None:
                gameQuit = True
                gameStart = True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameStart = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                            gameStart = True
                        elif event.key == pygame.K_ESCAPE and helpCase is False:
                            gameQuit = True
                            gameStart = True
                        elif event.key == pygame.K_ESCAPE and helpCase:
                            helpCase = False
                            screen.fill(backgroundCol)
                            displayMessage(logoImage, logoRect)
                            displayMessage(startImage, startRect)
                            displayMessage(exitImage, exitRect)
                            displayMessage(helpImage, helpRect)
                            pygame.display.update()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if startRect.collidepoint(pos):
                            gameStart = True
                        elif exitRect.collidepoint(pos):
                            gameQuit = True
                            gameStart = True
                        elif helpRect.collidepoint(pos):
                            helpCase = True
                            screen.fill(backgroundCol)
                            displayMessage(helpImage, (width / 2 - 70, height * 0.1, int(width / 6), int(height / 9)))
                            displayMessage(helpTextImage, helpTextRect)
                            displayMessage(menuImage, menuRect)
                            pygame.display.update()
                        elif menuRect.collidepoint(pos) and helpCase:
                            helpCase = False
                            screen.fill(backgroundCol)
                            displayMessage(logoImage, logoRect)
                            displayMessage(startImage, startRect)
                            displayMessage(exitImage, exitRect)
                            displayMessage(helpImage, helpRect)
                            pygame.display.update()
        if not gameQuit:
            menuMusic.stop()
            gameplay()
    pygame.quit()


def gameplay():
    gameMusic.play(-1)
    with open('highScore') as f:
        highScore = int(f.read())
    global gameQuit
    gameQuit = False
    gameSpeed = 4
    counter = 0
    gameOver = False
    healthCount = 3
    healthCountNow = healthCount
    gameWaiting = False
    objDamaged = None
    deathEnemy = False
    tempCounter = 0
    coinsCount = 0
    scb = Scoreboard()
    highScb = Scoreboard(width * 0.80)
    coinsScb = Scoreboard(0, height * 0.12, 2)
    player = Player()
    ground = Ground(gameSpeed)

    barrier = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    health = pygame.sprite.Group()
    lastObstacle = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    Barrier.containers = barrier
    Coin.containers = coins
    Cloud.containers = clouds
    Health.containers = health
    Enemy.containers = enemies

    tempCoin = Coin(0, 30, 30)
    tempCoin.rect.centerx = width / 2 - 50
    tempCoin.rect.top = height * 0.09

    hiImage, hiRect = loadImage('HI.png', int(width / 51), int(11 * 6 / 5))
    continueImage, continueRect = loadImage('continue.png', int(width / 3), int(height / 9))
    replayImage, replayRect = loadImage('replay.png', int(width / 20), int(height / 8))
    acceptImage, acceptRect = loadImage('accept.png', int(width / 20), int(height / 8))
    exitImage, exitRect = loadImage('exit.png', int(width / 20), int(height / 8))
    pauseImage, pauseRect = loadImage('pause.png', int(width / 3), int(height / 9))
    menuImage, menuRect = loadImage('menu.png', int(width / 12), int(height / 7))
    setCoordinat(hiRect, width * 0.785, height * 0.1)
    setCoordinat(continueRect, width / 2, height * 0.3)
    setCoordinat(acceptRect, width / 2 - 50, height * 0.5)
    setCoordinat(exitRect, width / 2 + 20, height * 0.5)
    setCoordinat(replayRect, width / 2 - 30, height * 0.55)
    setCoordinat(menuRect, width / 2 - 30, height * 0.35)
    setCoordinat(pauseRect, width / 2, height * 0.3)
    pygame.time.delay(300)

    while not gameQuit:
        while not gameOver and not gameQuit:
            if pygame.display.get_surface() is None:
                gameQuit = True
                gameOver = True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameOver = True
                        gameQuit = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameOver = True
                            gameQuit = True
                            gameMusic.stop()
                            menu()
                        if event.key == pygame.K_SPACE:
                            if player.rect.bottom == int(0.84 * height):
                                jumpMusic.play()
                                player.isJumping = True
                                if player.isAttack:
                                    player.isAttack = False
                                player.movement[1] = -1 * player.jumpSpeed
                        if event.key == pygame.K_f:
                            if player.isJumping is False and player.isDamaged is False and player.isAttack is False:
                                attackMusic.play()
                                player.isAttack = True
                                player.index = -1
                        if event.key == pygame.K_p:
                            pause = True
                            while pause and gameOver is False:
                                for ev in pygame.event.get():
                                    if ev.type == pygame.QUIT:
                                        gameOver = True
                                        gameQuit = True
                                    if ev.type == pygame.KEYDOWN:
                                        if ev.key == pygame.K_p:
                                            pause = False
                                        if ev.key == pygame.K_ESCAPE:
                                            pause = False
                                            gameOver = True
                                            gameQuit = True
                                            gameMusic.stop()
                                            menu()
                                displayMessage(pauseImage, pauseRect)
                                pygame.display.update()
                                pygame.time.delay(100)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if player.isJumping is False and player.isDamaged is False and player.isAttack is False:
                            attackMusic.play()
                            player.isAttack = True
                            player.index = -1

            for b in barrier:
                if pygame.sprite.collide_mask(player, b) and player.isDamaged is False:
                    if player.isAttack:
                        player.isAttack = False
                    damageMusic.play()
                    player.isDamaged = True
                    objDamaged = b
                    healthCountNow -= 1
                    player.index = -1
                    health = healthDamage(healthCountNow, healthCount)

            for c in coins:
                if pygame.sprite.collide_mask(player, c) and c is not tempCoin:
                    coinsCount += 1
                    coinMusic.play()
                    c.kill()

            for e in enemies:
                if pygame.sprite.collide_mask(player, e) and player.isDamaged is False \
                        and player.isAttack is False and deathEnemy is False and player.isJumping is False:
                    damageMusic.play()
                    player.isDamaged = True
                    objDamaged = e
                    healthCountNow -= 1
                    player.index = -1
                    health = healthDamage(healthCountNow, healthCount)
                if pygame.sprite.collide_mask(player, e) and (player.isAttack or
                                                              player.isJumping and (player.rect.bottom < e.rect.top)):
                    if e.death is False:
                        coinsCount += 1

                    deathEnemy = True
                    e.death = True
                    tempCounter = counter

            if player.isDamaged is True:
                if objDamaged.rect.right < player.rect.left:
                    player.isDamaged = False

            if len(health) < 3:
                for i in range(healthCount):
                    health.add(Health(30, 30, (width / 18 + i * width / 18)))

            if len(barrier) < 2:
                if len(barrier) == 0:
                    lastObstacle.empty()
                    lastObstacle.add(Barrier(gameSpeed, 36, 38))
                else:
                    for i in lastObstacle:
                        if i.rect.right < width * 0.7 and random.randrange(0, 100) == 10:
                            lastObstacle.empty()
                            lastObstacle.add(Barrier(gameSpeed, 36, 38))

            if len(enemies) < 2:
                for i in lastObstacle:
                    if i.rect.right < width * 0.7 and random.randrange(0, 100) == 10:
                        lastObstacle.empty()
                        lastObstacle.add(Enemy(gameSpeed + 1))

            if random.randrange(0, 100) == 10 and counter > 50:
                for i in lastObstacle:
                    if i.rect.right < width * 0.7:
                        lastObstacle.empty()
                        lastObstacle.add(Coin(gameSpeed, 30, 30))

            if len(clouds) < 10 and random.randrange(0, 600) == 351:
                Cloud()

            health.update()
            clouds.update()
            player.update()
            ground.update(gameSpeed)
            barrier.update(gameSpeed)
            coins.update(gameSpeed)
            enemies.update(gameSpeed + 1)
            scb.update(player.score)
            coinsScb.update(coinsCount)
            highScb.update(highScore)
            if pygame.display.get_surface() is not None:
                screen.fill(backgroundCol)
                tempCoin.draw()
                health.draw(screen)
                clouds.draw(screen)
                player.draw()
                ground.draw()
                coins.draw(screen)
                barrier.draw(screen)
                enemies.draw(screen)
                scb.draw()
                coinsScb.draw()
                if highScore != 0:
                    displayMessage(hiImage, hiRect)
                    highScb.draw()
                pygame.display.update()
                clock.tick(fps)

            if counter - tempCounter > 10:
                deathEnemy = False

            if counter % 700 == 699:
                gameSpeed += 1

            counter += 1
            if player.score % 100 == 0 and player.score % 1000 != 0 and player.counter % 5 == 4:
                hMusic.play()
            if player.score % 1000 == 0 and player.counter % 5 == 4:
                tMusic.play()
            if healthCountNow == 0:
                gameOver = True
                if coinsCount >= 3:
                    gameWaiting = True
                else:
                    if player.score > highScore:
                        highScore = player.score
                        with open('highScore', 'w') as f:
                            f.write(str(highScore))
        if gameQuit:
            break

        while gameWaiting:
            if pygame.display.get_surface() is None:
                gameQuit = True
                gameOver = False
                gameWaiting = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = False
                        gameWaiting = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameOver = True
                            gameQuit = False
                            gameWaiting = False
                            gameMusic.stop()
                            menu()
                        if event.key == pygame.K_SPACE:
                            gameWaiting = False
                            gameOver = False
                            coinsCount -= 3
                            healthCountNow += 1
                            health = healthDamage(healthCountNow, healthCount)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if acceptRect.collidepoint(pos):
                            gameWaiting = False
                            gameOver = False
                            coinsCount -= 3
                            healthCountNow += 1
                            health = healthDamage(healthCountNow, healthCount)
                        elif exitRect.collidepoint(pos):
                            if player.score > highScore:
                                highScore = player.score
                                with open('highScore', 'w') as f:
                                    f.write(str(highScore))
                            gameOver = True
                            gameWaiting = False
                            gameMusic.stop()
                            menu()
                if pygame.display.get_surface() is not None:
                    if gameWaiting is True:
                        displayMessage(continueImage, continueRect)
                        displayMessage(acceptImage, acceptRect)
                        displayMessage(exitImage, exitRect)
                        pygame.display.update()
                        clock.tick(fps)

        while gameOver and not gameQuit:
            if pygame.display.get_surface() is None:
                gameQuit = True
                gameOver = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameQuit = True
                            gameOver = False
                            gameMusic.stop()
                            menu()
                        if event.key == pygame.K_SPACE:
                            gameQuit = False
                            gameOver = False
                            gameMusic.stop()
                            gameplay()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if replayRect.collidepoint(pos):
                            gameQuit = False
                            gameOver = False
                            gameMusic.stop()
                            gameplay()
                        if menuRect.collidepoint(pos):
                            gameQuit = False
                            gameOver = False
                            gameMusic.stop()
                            menu()
            if pygame.display.get_surface() is not None:
                displayMessage(replayImage, replayRect)
                displayMessage(menuImage, menuRect)
                pygame.display.update()
            clock.tick(fps)
            if gameQuit:
                break

    pygame.quit()


menu()
