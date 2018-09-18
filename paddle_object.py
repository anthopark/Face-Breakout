import pygame
from os import path
from constants import *



class Paddle(pygame.sprite.Sprite):
    # paddle sprite class for the player to control
    def __init__(self, paddleImg):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(paddleImg, (100, 20))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT*0.9)
        self.speedx = 0

    def update(self):
        # need to set speedx to 0 everytime update() is called
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        self.rect.x += self.speedx

    def updateByXCoord(self, faceXCoord, lastFaceXCoord):
        if faceXCoord is None:
            self.rect.centerx = lastFaceXCoord
        else:
            self.rect.centerx = faceXCoord

        if self.rect.left < 100:
            self.rect.left = 100
        if self.rect.right > 700:
            self.rect.right = 700
