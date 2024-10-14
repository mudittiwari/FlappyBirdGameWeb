import pygame
import sys
import random
import asyncio

pygame.init()

# Define constants
ScreenWidth = 400
ScreenHeight = 500
GameSprites = []
GameMusic = []
Crossed = False
Score = 0
Clock = pygame.time.Clock()
Screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
pygame.display.set_caption("Flappy Bird")
ExitGame = False
BirdVelocity = 3
i = 0
TapCount = 0

# Load sprites and music
GameSprites.append(pygame.image.load("flappy-bird-hero-1240x1240.jpeg"))
Bird = pygame.image.load("bird.png")
GameSprites.append(Bird)
GameSprites.append(pygame.image.load("base.png"))
GameSprites.append(pygame.image.load("upper.jpg"))
GameSprites.append(pygame.image.load("pipe.png"))
GameSprites.append(pygame.transform.rotate(pygame.image.load("pipe.png"), 180))
GameSprites.append(pygame.image.load("gameover.png"))

# Scaling images
GameSprites[2] = pygame.transform.scale(GameSprites[2], (400, 100)).convert_alpha()
GameSprites[1] = pygame.transform.scale(GameSprites[1], (90, 90)).convert_alpha()
GameSprites[3] = pygame.transform.scale(GameSprites[3], (400, 400)).convert_alpha()
GameSprites[4] = pygame.transform.scale(GameSprites[4], (60, 300)).convert_alpha()
GameSprites[5] = pygame.transform.scale(GameSprites[5], (60, 300)).convert_alpha()
GameSprites[6] = pygame.transform.scale(GameSprites[6], (400, 500)).convert_alpha()

# Music
GameMusic.append(pygame.mixer.Sound("hit.ogg"))
GameMusic.append(pygame.mixer.Sound("wing.ogg"))
GameMusic.append(pygame.mixer.Sound("point.ogg"))

# Font and colors
Font = pygame.font.SysFont(None, 30)
Black = (0, 0, 0)
White = (192, 192, 192)
GameOver = False
BirdAcc = 0

# Function to generate lower pipe
def LowerPipeGenerator():
    posiY = random.randint(150, 350)
    return posiY

# Function to generate upper pipe
def UpperPipeGenerator(y):
    y = y - 100
    posiY = GameSprites[4].get_height() - y
    return posiY

# Function to generate text on screen
def TextGenerator(text, color, x, y):
    textToShow = Font.render(text, True, color)
    Screen.blit(textToShow, [x, y])
    pygame.display.update()

# Collision detection
async def Collision(birdPosi, lowerPipe, upperPipe):
    global Crossed
    if birdPosi < -40 or birdPosi > 325:
        GameMusic[0].play()
        await GameEnd()
    elif birdPosi > lowerPipe[1] - 75 and abs(lowerPipe[0] - 50) < GameSprites[4].get_width():
        GameMusic[0].play()
        await GameEnd()
    elif birdPosi < (upperPipe[1] + GameSprites[4].get_height() - 50) and abs(lowerPipe[0] - 50) < GameSprites[4].get_width():
        GameMusic[0].play()
        await GameEnd()
    elif lowerPipe[0] < 50 and not Crossed:
        global Score
        GameMusic[2].play()
        Score += 10
        Crossed = True

# End game
async def GameEnd():
    global ExitGame
    while not ExitGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ExitGame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                await StartScreen()

        Screen.blit(GameSprites[6], (0, 0))
        pygame.display.update()
        Clock.tick(60)
        await asyncio.sleep(0)
    pygame.quit()
    quit()

# Main game logic (async)
async def MainGame():
    global BirdAcc
    global GameOver
    global BirdVelocity
    global Crossed
    global Score  # Make sure score is global to reset it
    Score = 0  # Reset score when the game starts

    ready = False
    pipesList = [[400, 300], [400, -100]]
    birdPosi = 140
    velocityPipe = -9
    GameOver = False  # Track game over state
    while not ExitGame:
        if GameOver:  # Handle game over state
            await GameEnd()
            break  # Exit the game loop once GameEnd() completes

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                GameMusic[1].play()
                if ready:
                    BirdAcc = -1
                ready = True

        if ready:
            for pipes in pipesList:
                pipes[0] = pipes[0] + velocityPipe
                if pipesList[0][0] < -170:
                    y = LowerPipeGenerator()
                    pipesList = [[400, y], [400, -UpperPipeGenerator(y)]]
                    Crossed = False
            BirdVelocity = BirdVelocity + BirdAcc
            if BirdVelocity < -6:
                BirdAcc = 1
                birdPosi = birdPosi - BirdVelocity
            else:
                birdPosi = birdPosi + BirdVelocity

            await Collision(birdPosi, pipesList[0], pipesList[1])

        Screen.blit(GameSprites[3], (0, 0))
        Screen.blit(GameSprites[5], (pipesList[0][0], pipesList[0][1]))
        Screen.blit(GameSprites[4], (pipesList[1][0], pipesList[1][1]))
        Screen.blit(GameSprites[2], (0, 400))
        Screen.blit(GameSprites[1], (50, birdPosi))

        # Remove high score logic
        TextGenerator(f"score: {Score}", Black, 20, 30)

        pygame.display.update()
        Clock.tick(30)
        await asyncio.sleep(0)

# Start screen (async)
async def StartScreen():
    global TapCount
    GameSprites[0] = pygame.transform.scale(GameSprites[0], (ScreenWidth, ScreenHeight)).convert_alpha()
    Screen.blit(GameSprites[0], (0, 0))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                TapCount += 1
                if TapCount >= 2:
                    await MainGame()

        await asyncio.sleep(0)

# Main function to start the asyncio event loop
async def Main():
    await StartScreen()

# Run the game
if __name__ == "__main__":
    asyncio.run(Main())
