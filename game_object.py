"""This is game module

It helps control game status and contains some helper functions
"""
import pygame
import brick
from constants import *
import random
import time


class Game(object):
    def __init__(self):
        self.initialScreen = True
        self.standByStatus = True
        self.running = True
        self.lives = 3

    def runningStatus(self):
        return self.running

    def setRunningStatus(self, val):
        assert type(val) == bool, 'incorrect type of parameter "val"'
        self.running = val

    def die(self):
        """if ball is dropped decrement the life"""
        self.lives -= 1
        if self.lives == 0:
            self.initialScreen = True

    def getStandByMode(self):
        return self.standByStatus

    def setStandByMode(self, val):
        assert type(val) == bool, 'incorrect type of parameter "val"'
        self.standByStatus = val

    def getInitialScreenStatus(self):
        return self.initialScreen

    def setInitialScreenStatus(self, val):
        assert type(val) == bool, 'incorrect type of parameter "val"'
        self.initialScreen = val


# pygame will search the system for font with similar name
fontName = pygame.font.match_font('arial')


def initSound():
    """load various sound effects"""
    WALLOPENSND = pygame.mixer.Sound(path.join(SNDDIR, 'wallopen.wav'))
    BALLFALLSND = pygame.mixer.Sound(path.join(SNDDIR, 'ballfalling.wav'))
    PADDLECOLSND = pygame.mixer.Sound(path.join(SNDDIR, 'paddlecollide.wav'))

    SINGCOLSNDS = []
    SINGCOLSNDSLIST = ['singlebrickcol1.wav', 'singlebrickcol2.wav', 'singlebrickcol3.wav', 'singlebrickcol4.wav']
    for snd in SINGCOLSNDSLIST:
        SINGCOLSNDS.append(pygame.mixer.Sound(path.join(SNDDIR, snd)))

    MULTICOLSNDS = []
    MULTICOLSNDSLIST = ['multibrickcol1.wav', 'multibrickcol2.wav']
    for snd in MULTICOLSNDSLIST:
        MULTICOLSNDS.append(pygame.mixer.Sound(path.join(SNDDIR, snd)))

    return WALLOPENSND, BALLFALLSND, PADDLECOLSND, SINGCOLSNDS, MULTICOLSNDS


def drawText(surface, text, size, x, y):
    """size: font size. x, y: location."""
    font = pygame.font.Font(fontName, size)
    # False - alias / True - Anti-aliased(look smoother and nice)
    text_surface = font.render(text, True, GREEN)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def showInitialScreen(game, surface, clock):
    surface.blit(LEFTBRICKIMG, (0, 0))
    surface.blit(RIGHTBRICKIMG, (700, 0))
    surface.blit(CENTERBRICKIMG, (100, 0))
    drawText(surface, "FACE BREAKOUT!", 80, WIDTH//2, HEIGHT//4 - 40)
    drawText(surface, "Space to shoot the ball, Move face to control paddle", 34, WIDTH//2, HEIGHT//2+15)
    drawText(surface, "Press any key to play", 30, WIDTH//2, (HEIGHT*3/4) + 10)
    pygame.display.flip()
    waiting = True
    quit = False
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                quit = True
                break
            elif event.type == pygame.KEYUP:
                waiting = False
    if quit:
        pygame.quit()


def openUpScreen(surface, clock, snd):
    height = 0
    ySpeed = 8
    snd.play()
    while height > -HEIGHT:
        clock.tick(FPS)
        surface.fill(BLACK)
        surface.blit(LEFTBRICKIMG, (0, 0))
        surface.blit(RIGHTBRICKIMG, (700, 0))
        surface.blit(CENTERBRICKIMG, (100, height))
        height -= ySpeed
        pygame.display.flip()


def closeDownScreen(surface, clock, snd):
    height = -HEIGHT
    ySpeed = 8
    snd.play()
    while height < 0:
        clock.tick(FPS)
        surface.fill(BLACK)
        surface.blit(LEFTBRICKIMG, (0, 0))
        surface.blit(RIGHTBRICKIMG, (700, 0))
        surface.blit(CENTERBRICKIMG, (100, height))
        height += ySpeed
        pygame.display.flip()


def createBricks(brickGroup, allSprites):
    """Create and place brick objects
    """

    brickPlaceY = 0
    for i in range(6):
        if i % 2:
            brickPlaceX = 100
        else:
            brickPlaceX = 50
        for j in range(6):
            brickImg = pygame.image.load(path.join(IMGDIR, random.choice(BRICKIMGLIST)))
            brickObj = brick.Brick(brickImg, brickPlaceX, brickPlaceY)
            allSprites.add(brickObj)
            brickGroup.add(brickObj)
            brickPlaceX += 100
            if not i % 2:
                brickImg = pygame.image.load(path.join(IMGDIR, random.choice(BRICKIMGLIST)))
                brickObj = brick.Brick(brickImg, brickPlaceX, brickPlaceY)
                allSprites.add(brickObj)
                brickGroup.add(brickObj)

        brickPlaceY += 30
