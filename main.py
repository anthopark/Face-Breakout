import pygame
import cv2
from constants import *
import face_detect
import game_object
from game_object import random
import paddle_object
import ball_object
import time


# Initialize video stream and load face detection DNN
print("Starting Video Stream...")
videoStream = face_detect.VideoStream(src=0).start()
time.sleep(3)

net = face_detect.getDNN()


# Initialize pygame and window
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

# Initialize essential objects
clock = pygame.time.Clock()
game = game_object.Game()

# Initialize sound objects
wallOpenSnd, ballFallSnd, paddleColSnd, singColSnds, \
    multiColSnds = game_object.initSound()
paddleColSnd.set_volume(0.4)

# some required variables for game
paddleCollideTime = 0
lastFaceXCoord = WIDTH // 2
isFirstGame = True

# main game loop
while game.runningStatus():

    # go to inital screen when program first starts
    # when game over(lives == 0), come back to initial screen
    if game.getInitialScreenStatus():
        # when player exhausted all of the lives and coming back to initial screen
        # or player broke all the bricks and coming back to initial screen
        if game.lives == 0 or not isFirstGame:
            pygame.mixer.music.stop()
            game_object.closeDownScreen(screen, clock, wallOpenSnd)

        game.lives = 3
        game_object.showInitialScreen(game, screen, clock)
        game_object.openUpScreen(screen, clock, wallOpenSnd)
        game.setInitialScreenStatus(False)
        game.setStandByMode(True)

        isFirstGame = False

        # Initialize essential sprites of game
        allSprites = pygame.sprite.Group()
        brickGroup = pygame.sprite.Group()
        ball = ball_object.Ball(BALLIMG, ballFallSnd)
        paddle = paddle_object.Paddle(PADDLEIMG)
        game_object.createBricks(brickGroup, allSprites)
        allSprites.add(paddle)
        allSprites.add(ball)

        # background music
        pygame.mixer.music.load(path.join(SNDDIR, 'bgm2.mp3'))
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
        pygame.mixer.music.play()


    # adjust game speed
    clock.tick(FPS)

    # process video frame and detect face
    # get the center x coord of detected face
    camFrame = face_detect.getCamFrame(videoStream)
    faceXCoord = face_detect.getFaceXCoord(camFrame, net)

    # test mouse control
    # mouseX, mouseY = pygame.mouse.get_pos()

    if faceXCoord is not None:
        lastFaceXCoord = faceXCoord


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.setRunningStatus(False)
        elif event.type == pygame.constants.USEREVENT:
            pygame.mixer.music.load(path.join(SNDDIR, 'bgm2.mp3'))
            pygame.mixer.music.play()

        elif event.type == pygame.KEYDOWN:  # keydown event = any key pressed
            if event.key == pygame.K_SPACE and game.getStandByMode():
                game.setStandByMode(False)
                ball.initialMove()

    if not game.getStandByMode():
        # play mode

        # check if all the bricks are gone
        if not brickGroup:
            game.setInitialScreenStatus(True)

        # paddle.updateByXCoord(mouseX, lastFaceXCoord)
        paddle.updateByXCoord(faceXCoord, lastFaceXCoord)
        ball.update(game, paddle)

        # ball - paddle collision
        currentTime = time.time()

        if pygame.sprite.collide_rect(ball, paddle) \
                and currentTime - paddleCollideTime > 0.3:
            paddleColSnd.play()
            paddleCollideTime = ball.paddleDeflection(paddle)
            print("Collision!")

        # ball - bricks collision
        hits = pygame.sprite.spritecollide(ball, brickGroup, True)

        if len(hits) == 1:
            random.choice(singColSnds).play()
            ball.brickSingleDeflection(hits[0])
        elif len(hits) >= 2:
            random.choice(multiColSnds).play()
            ball.brickDoubleDeflection(hits[0], hits[1])

    else:
        # standby mode

        # ball.updateStandBy(mouseX, lastFaceXCoord)
        # paddle.updateByXCoord(mouseX, lastFaceXCoord)
        ball.updateStandBy(faceXCoord, lastFaceXCoord)
        paddle.updateByXCoord(faceXCoord, lastFaceXCoord)

    screen.fill(BLACK)

    # screen.blit(camFrame, (0, 200))
    allSprites.draw(screen)

    screen.blit(LEFTBRICKIMG, (0, 0))
    screen.blit(RIGHTBRICKIMG, (700, 0))

    pygame.display.flip()
    cv2.imshow("Frame", camFrame)
    cv2.waitKey(1)

cv2.destroyAllWindows()

videoStream.stop()
time.sleep(3)
pygame.quit()
