import pygame
import math
import random
import time

from constants import *


class Ball(pygame.sprite.Sprite):
    # paddle sprite class for the player to control
    def __init__(self, ballImg, ballFallSnd):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(ballImg, (20, 20))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT*0.9 - 20)
        self.radius = int(self.rect.width / 2)
        self.speedx = 0
        self.speedy = 0
        self.travelSpeed = 9
        self.cp = [False] * 8
        self.ballFallSnd = ballFallSnd

    def updateStandBy(self, faceXCoord, lastFaceXCoord):
        """standby status. moves right and left,
        the ball stay top of the paddle
        """

        if faceXCoord is None:
            self.rect.centerx = lastFaceXCoord
        else:
            self.rect.centerx = faceXCoord

        if self.rect.left < 150:
            self.rect.centerx = 100 + 50
        if self.rect.right > 650:
            self.rect.centerx = 700 - 50

    def initialMove(self):
        """Set ball inital speed and direction"""
        angle = random.uniform(45, 135)
        while angle > 75 and angle < 105:
            angle = random.uniform(45, 135)
        print("angle: ", angle)
        self.speedx = self.travelSpeed * math.cos(math.radians(angle))
        self.speedy = self.travelSpeed * math.sin(math.radians(angle))

    def update(self, game, paddle):
        """playing status. Ball will be traveling"""
        self.rect.x += self.speedx
        self.rect.y -= self.speedy

        if self.rect.left < 100:
            self.rect.left = 100
            self.speedx *= -1
        if self.rect.right > 700:
            self.rect.right = 700
            self.speedx *= -1

        if self.rect.top <= 0:
            self.speedy *= -1
        if self.rect.bottom > HEIGHT:
            self.ballFallSnd.play()
            game.die()
            game.setStandByMode(True)
            time.sleep(1)
            paddle.rect.center = (WIDTH/2, HEIGHT*0.9)
            self.rect.center = (WIDTH/2, HEIGHT*0.9 - 20)

    def collideSides(self, otherRect):
        self.cp[0] = otherRect.collidepoint(self.rect.topleft)
        self.cp[1] = otherRect.collidepoint(self.rect.topright)
        self.cp[2] = otherRect.collidepoint(self.rect.bottomleft)
        self.cp[3] = otherRect.collidepoint(self.rect.bottomright)
        self.cp[4] = otherRect.collidepoint(self.rect.midleft)
        self.cp[5] = otherRect.collidepoint(self.rect.midright)
        self.cp[6] = otherRect.collidepoint(self.rect.midtop)
        self.cp[7] = otherRect.collidepoint(self.rect.midbottom)

        left = (self.cp[1] and self.cp[5] and not self.cp[0]) or \
               (self.cp[5] and self.cp[3] and not self.cp[2])
        right = (self.cp[0] and self.cp[4] and not self.cp[1]) or \
                (self.cp[4] and self.cp[2] and not self.cp[3])
        top = (self.cp[2] and self.cp[7] and self.cp[3] and not self.cp[6]) or \
              (self.cp[3] and not self.cp[5]) or (self.cp[2] and not self.cp[4])
        bottom = (self.cp[0] and self.cp[6] and self.cp[1] and not self.cp[7]) or \
                 (self.cp[1] and not self.cp[5]) or (self.cp[0] and not self.cp[4])

        return left, right, top, bottom


    def paddleDeflection(self, paddle):

        left, right, top, bottom = self.collideSides(paddle.rect)

        # when ball hits the left side of paddle
        if self.speedx > 0 and left:
            self.rect.right = paddle.rect.left
            self.speedx *= -1
        # when ball hits the right side of paddle
        elif self.speedx < 0 and right:
            self.rect.left = paddle.rect.right
            self.speedx *= -1
        elif top:
            self.speedy *= -1
        elif bottom:
            pass


        # return paddle - ball collide time to avoid keep colliding
        return time.time()

    def brickSingleDeflection(self, brick):
        # left side Collision
        print("Single brick Collide")
        left, right, top, bottom = self.collideSides(brick.rect)

        # ball hits left side of brick
        if self.speedx > 0 and left:
            self.rect.right = brick.rect.left-1
            self.speedx *= -1
            print("Left Collision")
        # ball hits right side of brick
        elif self.speedx < 0 and right:
            self.rect.left = brick.rect.right+1
            self.speedx *= -1
            print("Right Collision")
        # ball hits top of brick
        elif top:
            self.rect.bottom = brick.rect.top-1
            self.speedy *= -1
            print("Top Collision")
        # ball hits bottom of brick
        elif bottom:
            self.rect.top = brick.rect.bottom+1
            self.speedy *= -1
            print("Bottom Collision")

    def brickDoubleDeflection(self, brick1, brick2):

        print("Multiple brick Collide")

        # ball hits the middle of two bricks
        if brick1.rect.bottom == brick2.rect.bottom:
            self.speedy *= -1
        else:
            self.speedy *= -1
            self.speedx *= -1
