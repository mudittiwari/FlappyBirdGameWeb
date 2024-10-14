import pygame
import sys
import random
import asyncio

pygame.init()

# Define constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 500
GAME_SPRITES = []
GAME_MUSIC = []
crossed = False
score = 0
clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
exit_game = False
bird_velocity = 3
i = 0

# Load sprites and music
GAME_SPRITES.append(pygame.image.load("flappy-bird-hero-1240x1240.png"))
BIRD = pygame.image.load("bird.png")
GAME_SPRITES.append(BIRD)
GAME_SPRITES.append(pygame.image.load("base.png"))
GAME_SPRITES.append(pygame.image.load("upper.jpg"))
GAME_SPRITES.append(pygame.image.load("pipe.png"))
GAME_SPRITES.append(pygame.transform.rotate(pygame.image.load("pipe.png"), 180))
GAME_SPRITES.append(pygame.image.load("gameover.png"))

# Scaling images
GAME_SPRITES[2] = pygame.transform.scale(GAME_SPRITES[2], (400, 100)).convert_alpha()
GAME_SPRITES[1] = pygame.transform.scale(GAME_SPRITES[1], (90, 90)).convert_alpha()
GAME_SPRITES[3] = pygame.transform.scale(GAME_SPRITES[3], (400, 400)).convert_alpha()
GAME_SPRITES[4] = pygame.transform.scale(GAME_SPRITES[4], (60, 300)).convert_alpha()
GAME_SPRITES[5] = pygame.transform.scale(GAME_SPRITES[5], (60, 300)).convert_alpha()
GAME_SPRITES[6] = pygame.transform.scale(GAME_SPRITES[6], (400, 500)).convert_alpha()

# Music
GAME_MUSIC.append(pygame.mixer.Sound("hit.wav"))
GAME_MUSIC.append(pygame.mixer.Sound("wing.wav"))
GAME_MUSIC.append(pygame.mixer.Sound("point.wav"))

# Font and colors
font = pygame.font.SysFont(None, 30)
black = (0, 0, 0)
white = (192, 192, 192)
game_over = False
bird_acc = 0

# Function to generate lower pipe
def lowerpipegenerator():
    posi_y = random.randint(150, 350)
    return posi_y

# Function to generate upper pipe
def upperpipegenerator(y):
    y = y - 100
    posi_y = GAME_SPRITES[4].get_height() - y
    return posi_y

# Function to generate text on screen
def text_generator(text, color, x, y):
    texttoshow = font.render(text, True, color)
    SCREEN.blit(texttoshow, [x, y])
    pygame.display.update()

# Collision detection
async def collison(bird_posi, lowerpipe, upperpipe):
    global crossed
    if bird_posi < -40 or bird_posi > 325:
        GAME_MUSIC[0].play()
        await game_end()
    elif bird_posi > lowerpipe[1] - 75 and abs(lowerpipe[0] - 50) < GAME_SPRITES[4].get_width():
        GAME_MUSIC[0].play()
        await game_end()
    elif bird_posi < (upperpipe[1] + GAME_SPRITES[4].get_height() - 50) and abs(lowerpipe[0] - 50) < GAME_SPRITES[4].get_width():
        GAME_MUSIC[0].play()
        await game_end()
    elif lowerpipe[0] < 50 and not crossed:
        global score
        GAME_MUSIC[2].play()
        score += 10
        crossed = True

# End game
async def game_end():
    global exit_game
    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                await start_screen()

        SCREEN.blit(GAME_SPRITES[6], (0, 0))
        enter = pygame.image.load("entertoplay.png")
        enter = pygame.transform.scale(enter, (200, 50)).convert_alpha()
        SCREEN.blit(enter, (100, 380))
        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)
    pygame.quit()
    quit()

# Main game logic (async)
async def main_game():
    global bird_acc
    global game_over
    global bird_velocity
    global crossed
    ready = False
    pipes_list = [[400, 300], [400, -100]]
    bird_posi = 140
    velocity_pipe = -9
    game_over = False  # Track game over state
    while not exit_game:
        if game_over:  # Handle game over state
            await game_end()
            break  # Exit the game loop once game_end() completes

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                GAME_MUSIC[1].play()
                if ready:
                    bird_acc = -1
                ready = True

        if ready:
            for pipes in pipes_list:
                pipes[0] = pipes[0] + velocity_pipe
                if pipes_list[0][0] < -170:
                    y = lowerpipegenerator()
                    pipes_list = [[400, y], [400, -upperpipegenerator(y)]]
                    crossed = False
            bird_velocity = bird_velocity + bird_acc
            if bird_velocity < -6:
                bird_acc = 1
                bird_posi = bird_posi - bird_velocity
            else:
                bird_posi = bird_posi + bird_velocity

            await collison(bird_posi, pipes_list[0], pipes_list[1])

        SCREEN.blit(GAME_SPRITES[3], (0, 0))
        SCREEN.blit(GAME_SPRITES[5], (pipes_list[0][0], pipes_list[0][1]))
        SCREEN.blit(GAME_SPRITES[4], (pipes_list[1][0], pipes_list[1][1]))
        SCREEN.blit(GAME_SPRITES[2], (0, 400))
        SCREEN.blit(GAME_SPRITES[1], (50, bird_posi))

        text_generator(f"score: {score}", black, 20, 30)  # Only display the current score

        pygame.display.update()
        clock.tick(30)
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()

# Start screen (async)
async def start_screen():
    GAME_SPRITES[0] = pygame.transform.scale(GAME_SPRITES[0], (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
    SCREEN.blit(GAME_SPRITES[0], (0, 0))
    text_generator("Flappy Bird by Mudit Tiwari", white, 65, 340)
    enter = pygame.image.load("entertoplay.png")
    enter = pygame.transform.scale(enter, (200, 50)).convert_alpha()
    SCREEN.blit(enter, (100, 380))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                await main_game()

        await asyncio.sleep(0)

# Main function to start the asyncio event loop
async def main():
    await start_screen()

# Run the game
if __name__ == "__main__":
    asyncio.run(main())
