import pygame
from constants import *


class Brick(pygame.sprite.Sprite):
    def __init__(self, brickImg, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(brickImg, (100, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
