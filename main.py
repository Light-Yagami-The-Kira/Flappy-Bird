import random
import sys
import pygame
from pygame.locals import *

## GLOBAL VARIABLES
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8

GAME_SPRITES = {}
GAME_SOUNDS = {}

PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.jpg'
PIPE = 'gallery/sprites/pipe.png'


## GAME FUNCTIONS

def gameOver():
    print("Game Over")
    gameoverImage = pygame.image.load('gallery/sprites/gameover.png')
    gameoverImage = pygame.transform.scale(gameoverImage, (300,300))
    GOIx = (SCREENWIDTH - gameoverImage.get_width())/2
    GOIy = (SCREENHEIGHT - gameoverImage.get_height())/2
    SCREEN.blit(gameoverImage, (GOIx, GOIy - 50))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            


def welcomeScreen():
    playerx = SCREENWIDTH // 5 + 100
    playery = (SCREENHEIGHT - GAME_SPRITES['player'].get_height())//2 - 50

    messagex = (SCREENWIDTH - GAME_SPRITES['message'].get_width())//2
    messagey = (SCREENHEIGHT - GAME_SPRITES['message'].get_height())//2

    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            elif pygame.mouse.get_pressed()[0]:
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0,0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx,playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    
    playerx = 100
    playery = (SCREENHEIGHT - GAME_SPRITES['player'].get_height())//2 - 50
    basex = 0

    def getRandomPipe():
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        offset = GAME_SPRITES['player'].get_height() + 100
        Roof_Offset = 20
        phi = random.randrange(Roof_Offset,SCREENHEIGHT//2)
        y1 = pipeHeight - phi
        pipeX = SCREENWIDTH + 10
        y2 = phi + offset
        pipe = [
            {'x':pipeX, 'y': -y1}, ## UPPER PIPE
            {'x':pipeX, 'y': y2}   ## LOWER PIPE
        ]

        return pipe

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    ## LIST OF UPPER PIPES
    upperPipes = [
        {'x':SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH//2), 'y':newPipe2[0]['y']}
    ]

    ## LIST OF LOWER PIPES
    lowerPipes = [
        {'x':SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH//2), 'y':newPipe2[1]['y']}
    ]

    pipeVelX = -4

    playerVelY = -9  ## GRAVITATION
    playerMaxVelY = 11
    playerMinVelY = -8
    playerAccY = 1

    playerFlapVelocity = -9.5

    playerFlapped = False 

    #GAME LOOP

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if (event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)) or (pygame.mouse.get_pressed()[0]):
                if playery > 0:
                    playerVelY = playerFlapVelocity
                    playerFlapped == True
                    GAME_SOUNDS['wing'].play()

        def isCollide(playerx, playery, upperPipes, lowerPipes):
            if playery<0:
                GAME_SOUNDS['swoosh'].play()
                return True
            if playery >= GROUNDY-30:
                GAME_SOUNDS['hit'].play()
                return True
            for pipe in upperPipes:
                pipeHeight = GAME_SPRITES['pipe'][0].get_height()
                if (playery < pipeHeight + pipe['y'] and (abs(playerx - pipe['x'])) < GAME_SPRITES['pipe'][0].get_width()/2 + 9):   ##30
                    GAME_SOUNDS['hit'].play()
                    return True
            for pipe in lowerPipes:
                if (playery + GAME_SPRITES['player'].get_height() >= pipe['y'] and (abs(playerx - pipe['x'])) < GAME_SPRITES['pipe'][0].get_width()/2 + 9):
                    GAME_SOUNDS['hit'].play()
                    return True


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)

        if crashTest:
            with open('score.txt', 'a') as f:
                f.write(f'{score}\n')
            return
        
        ## SCORE SYSTEM
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2

        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        
        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery += min(playerVelY, GROUNDY - playery - playerHeight)


        ## PIPE MOTION (RIGHT ---> LEFT)
        for upperpipe, lowerpipe in zip(upperPipes, lowerPipes):
            upperpipe['x'] += pipeVelX
            lowerpipe['x'] += pipeVelX

        ## ADD NEW PIPE WHEN FIRST PIPE IS ABOUT TO GO OUTTA SCREEN
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        ## DELETING PIPES OUTTA SCREEN
        if upperPipes[0]['x'] < - GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        ## BLITTING IMAGES
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperpipe, lowerpipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperpipe['x'], upperpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerpipe['x'], lowerpipe['y']))
        SCREEN.blit(GAME_SPRITES['base'], (basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

## BLITTING SCORE
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, 10))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
## MAIN BODY
if __name__ == '__main__':
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    BGM = pygame.mixer.Sound('gallery/audio/NearTheme.mp3')
    BGM.set_volume(0.1)
    BGM.play(-1)

    ## GAME_SPRITES BEING LOADED
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png'),
        pygame.image.load('gallery/sprites/1.png'),
        pygame.image.load('gallery/sprites/2.png'),
        pygame.image.load('gallery/sprites/3.png'),
        pygame.image.load('gallery/sprites/4.png'),
        pygame.image.load('gallery/sprites/5.png'),
        pygame.image.load('gallery/sprites/6.png'),
        pygame.image.load('gallery/sprites/7.png'),
        pygame.image.load('gallery/sprites/8.png'),
        pygame.image.load('gallery/sprites/9.png')
    )
    GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    lava = pygame.image.load('gallery/sprites/lava.jpg').convert_alpha()
    lava = pygame.transform.scale(lava, (SCREENWIDTH,300))
    # lava = pygame.transform.rotate(lava,180)
    GAME_SPRITES['base'] = lava
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()
                            )
    fire = pygame.image.load(BACKGROUND).convert_alpha()
    fire = pygame.transform.scale(fire, (SCREENWIDTH,SCREENHEIGHT))
    GAME_SPRITES['background'] = fire
    GAME_SPRITES['player'] = pygame.image.load(PLAYER)

    ## GAME SOUNDS
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')
##===================================================================================================
    while True:
        welcomeScreen()
        mainGame()
        gameOver()
        pygame.display.update()
        FPSCLOCK.tick(FPS)