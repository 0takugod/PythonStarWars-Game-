import sys
import pygame

pygame.init()

windowWidth = 1100
windowHeight = 728
FPS = 20
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
throwFireRate = 25


# setting variables for the fire image and its rectangular area
imgfb2 = pygame.image.load('fireborder2.png')
imgfb2_rect = imgfb2.get_rect()
imgfb2_rect.left = 0
imgfb1 = pygame.image.load('fireborder.png')
imgfb1_rect = imgfb1.get_rect()
imgfb1_rect.left = 0


CLOCK = pygame.time.Clock()
font = pygame.font.SysFont('calibri', 20)
canvas = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Star Wars')
icon = pygame.image.load('StarWars.png')
pygame.display.set_icon(icon)


class Topscore:
    def __init__(self):
        self.high_score = 0

    def top_score(self, score):
        if score > self.high_score:
            self.high_score = score
        return self.high_score


topscore = Topscore()


# defining the game character Enemy
class Enemy:

    def __init__(self):

        self.velocityE = 10
        self.imgE = pygame.image.load('Enemy.png')
        self.imgE_rect = self.imgE.get_rect()
        self.imgE_rect.width -= 10
        self.imgE_rect.height -= 10
        self.imgE_rect.top = windowHeight/2
        self.imgE_rect.right = windowWidth - 40
        self.up = True
        self.down = False

    def update(self):

        canvas.blit(self.imgE, self.imgE_rect)

        if self.imgE_rect.top <= imgfb2_rect.bottom:
            self.up = False
            self.down = True

        elif self.imgE_rect.bottom >= imgfb1_rect.top:
            self.up = True
            self.down = False

        if self.up:
            self.imgE_rect.top -= self.velocityE               # the enemy moves up
        elif self.down:
            self.imgE_rect.top += self.velocityE               # the enemy moves down


# defining the game element Bullet
class Fire:

    def __init__(self):

        self.velocityFire = 20
        self.imgFire = pygame.image.load('Fire.png')
        self.imgFire_rect = self.imgFire.get_rect()
        self.imgFire_rect.right = ENEMY.imgE_rect.left
        self.imgFire_rect.top = ENEMY.imgE_rect.top + 22

    def update(self):

        canvas.blit(self.imgFire, self.imgFire_rect)

        # making the bullet move left after it is created
        if self.imgFire_rect.left > 0:
            self.imgFire_rect.left -= self.velocityFire


# defining the game character of the player
class Player:

    def __init__(self):

        self.velocity = 10
        self.imgP = pygame.image.load('Player.png')
        self.imgP_rect = self.imgP.get_rect()
        self.imgP_rect.left = 40
        self.imgP_rect.top = windowHeight/2 - 100

    def update(self):

        canvas.blit(self.imgP, self.imgP_rect)

        if self.imgP_rect.top <= imgfb2_rect.bottom:
            game_over()                                              # player touches fire above, game over

        if self.imgP_rect.bottom >= imgfb1_rect.top:
            game_over()                                              # player touches fire below, game over


# defining the function to terminate the program
def game_exit():
    pygame.quit()
    sys.exit()


# defining the function which is called when game is lost
def game_over():
    topscore.top_score(SCORE)

    canvas.fill(BLACK)

    imgGameOver = pygame.image.load('GameOver.png')
    imgGameOver_rect = imgGameOver.get_rect()
    canvas.blit(imgGameOver, imgGameOver_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                               # runs a function to quit program
                game_exit()

            if event.type == pygame.KEYDOWN:                            # checks if key is pressed
                if event.key == pygame.K_ESCAPE:
                    game_exit()
                else:
                    game_loop()

        pygame.display.update()


# defining the starting of game
def game_start():
    canvas.fill(BLACK)

    imgStart = pygame.image.load('StarWars.png')
    imgStart_rect = imgStart.get_rect()
    canvas.blit(imgStart, imgStart_rect)

    # to quit the game midway
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_exit()
                else:
                    game_loop()

        pygame.display.update()


# defining a function that keeps a track of the level
def check_level():

    global LEVEL

    if SCORE in range(0, 10):
        imgfb2_rect.bottom = 0
        imgfb1_rect.top = windowHeight - 0
        LEVEL = 1
    elif SCORE in range(10, 25):
        imgfb2_rect.bottom = 70
        imgfb1_rect.top = windowHeight - 70
        LEVEL = 2
    elif SCORE in range(25, 45):
        imgfb2_rect.bottom = 140
        imgfb1_rect.top = windowHeight - 140
        LEVEL = 3
    elif SCORE in range(45, 65):
        imgfb2_rect.bottom = 210
        imgfb1_rect.top = windowHeight - 210
        LEVEL = 4
    elif SCORE in range(65, 80):
        imgfb2_rect.bottom = 280
        imgfb1_rect.top = windowHeight - 280
        LEVEL = 5
    elif SCORE in range(80, 8000):
        imgfb2_rect.bottom = 350
        imgfb1_rect.top = windowHeight - 350
        LEVEL = 6


# defining the main gameplay function
def game_loop():

    global ENEMY
    ENEMY = Enemy()
    global PLAYER
    PLAYER = Player()
    global SCORE
    SCORE = 0
    global HIGHSCORE
    HIGHSCORE = topscore.top_score(SCORE)

    throwFireCounter = 0
    fire_list = []

    while True:

        imgGamePlay = pygame.image.load('bg.jpg')
        imgGamePlay_rect = imgGamePlay.get_rect()
        canvas.blit(imgGamePlay, imgGamePlay_rect)

        check_level()
        ENEMY.update()
        throwFireCounter += 1

        # controlling the interval after which again a fireball is thrown
        if throwFireCounter == throwFireRate:
            throwFireCounter = 0
            new_flame = Fire()
            fire_list.append(new_flame)

        for f in fire_list:

            if f.imgFire_rect.left <= 0:
                fire_list.remove(f)
                SCORE += 1

            f.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    game_exit()

                if event.key == pygame.K_UP:            # player moves up
                    PLAYER.imgP_rect.top -= 20
                elif event.key == pygame.K_DOWN:        # player moves down
                    PLAYER.imgP_rect.top += 20

        # setting the attributes of text on screen
        scorefont = font.render('Score:' + str(SCORE), True, GREEN)
        scorefont_rect = scorefont.get_rect()
        scorefont_rect.center = (250, imgfb2_rect.bottom + scorefont_rect.height / 2)
        canvas.blit(scorefont, scorefont_rect)

        levelfont = font.render('Level:' + str(LEVEL), True, GREEN)
        levelfont_rect = levelfont.get_rect()
        levelfont_rect.center = (550, imgfb2_rect.bottom + scorefont_rect.height / 2)
        canvas.blit(levelfont, levelfont_rect)

        topscorefont = font.render('Top Score:' + str(HIGHSCORE), True, GREEN)
        topscorefont_rect = topscorefont.get_rect()
        topscorefont_rect.center = (850, imgfb2_rect.bottom + scorefont_rect.height / 2)
        canvas.blit(topscorefont, topscorefont_rect)

        # setting both the fire images
        canvas.blit(imgfb2, imgfb2_rect)
        canvas.blit(imgfb1, imgfb1_rect)
        PLAYER.update()

        for f in fire_list:

            if f.imgFire_rect.colliderect(PLAYER.imgP_rect):                 # deciding when the game is lost
                game_over()

        pygame.display.update()
        CLOCK.tick(FPS)


game_start()
