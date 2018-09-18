from os import path
import pygame

WIDTH = 800
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

IMGDIR = path.join(path.dirname(__file__), 'img')
SNDDIR = path.join(path.dirname(__file__), 'snd')

BRICKIMGLIST = ['brick1.png', 'brick2.png', 'brick3.png', 'brick4.png',
                'brick5.png', 'brick6.png', 'brick7.png', 'brick8.png',
                'brick9.png', 'brick10.png']

BALLIMG = pygame.image.load(path.join(IMGDIR, 'ball.png'))
PADDLEIMG = pygame.image.load(path.join(IMGDIR, 'paddle.png'))
LEFTBRICKIMG = pygame.image.load(path.join(IMGDIR, 'brickwallLEFT.png'))
RIGHTBRICKIMG = pygame.image.load(path.join(IMGDIR, 'brickwallRIGHT.png'))
CENTERBRICKIMG = pygame.image.load(path.join(IMGDIR, 'brickwallCENTER.png'))
