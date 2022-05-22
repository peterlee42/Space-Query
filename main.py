import pygame
import sys
from button import Button
from query import q

pygame.init()

# VARIABLES
WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
BLACK = (0, 0, 0)


def main():
    # LOAD IMGS
    background = pygame.image.load("assets/spaceBG.jpeg")
    btnSearch = pygame.image.load(
        "assets/btnSearch.png").convert_alpha()
    btnSearchVoice = pygame.image.load(
        "assets/btnSearchVoice.png").convert_alpha()
    btnSolarSystem = pygame.image.load(
        "assets/btnSolarSystem.png").convert_alpha()
    btnTrackISS = pygame.image.load("assets/btnTrackISS.png")
    btnQuit = pygame.image.load("assets/btnQuit.png").convert_alpha()

    # TITLE
    font = pygame.font.SysFont("corbel", 60)
    title = font.render("Welcome to Space Query!", True, GREEN, BLUE)
    titleRect = title.get_rect()
    titleRect.center = (WIDTH//2, HEIGHT//8)

    # BUTTONS
    btnSearch = Button(WIDTH//4*3, HEIGHT//4, btnSearch, 0.8)
    btnQuit = Button(WIDTH//4*3, HEIGHT//8*7, btnQuit, 0.8)
    btnSearchVoice = Button(WIDTH//4*3, HEIGHT//8*3, btnSearchVoice, 0.8)

    # TEXT INPUT
    baseFont = pygame.font.Font(None, 40)
    userText = ""
    previousLetters = 0
    inputRect = pygame.Rect(WIDTH//10, HEIGHT//8*2, 800, 50)
    activeColour = pygame.Color("cadetblue1")
    passiveColour = pygame.Color("blueviolet")
    colour = passiveColour
    active = False

    # DISPLAY
    pygame.display.set_caption("Main Menu")

    SCREEN.fill(BLACK)

    clock = pygame.time.Clock()
    while True:
        # Sets FPS to 60. Adds background and title to screen.
        clock.tick(60)
        SCREEN.blit(background, (0, 0))
        SCREEN.blit(title, titleRect)

        # DISPLAY BUTTONS AND CHECK IF IT HAS BEEN PRESSED
        if btnSearch.draw(SCREEN):
            spaceQuery()
        if btnSearchVoice.draw(SCREEN):
            searchVoice()
        if btnQuit.draw(SCREEN):
            pygame.quit()
            sys.exit()

        # DISPLAY AND TYPE IN TEXT INPUT
        if active:
            colour = activeColour
        else:
            colour = passiveColour
        pygame.draw.rect(SCREEN, colour, inputRect)
        textSurface = baseFont.render(
            userText[previousLetters:], True, (255, 255, 255))
        SCREEN.blit(textSurface, (inputRect.x+5, inputRect.y+5))
        pygame.display.flip()

        # Quits program if application is closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Input text of query
            if event.type == pygame.MOUSEBUTTONDOWN:
                if inputRect.collidepoint(event.pos):
                    active = True
                else:
                    active = False

            if event.type == pygame.KEYDOWN:
                if active == True:

                    if len(userText) >= 45:
                        if event.key == pygame.K_BACKSPACE:
                            userText = userText[:-1]
                            if previousLetters > 0:
                                previousLetters -= 1
                        else:
                            previousLetters += 1
                            userText += event.unicode
                    else:
                        if event.key == pygame.K_BACKSPACE:
                            userText = userText[:-1]
                        else:
                            userText += event.unicode
                    if event.key == pygame.K_RETURN:
                        print(q.main(userText))

        pygame.display.update()


def spaceQuery():
    # LOAD IMGS
    background = pygame.image.load("assets/spaceBG.jpeg")
    btnQuit = pygame.image.load("assets/btnQuit.png").convert_alpha()
    btnBack = pygame.image.load("assets/btnBack.png").convert_alpha()

    # TITLE
    font = pygame.font.SysFont("corbel", 60)
    title = font.render("To Answer Your Question...", True, GREEN, BLUE)
    titleRect = title.get_rect()
    titleRect.center = (WIDTH//2, HEIGHT//8)

    # BUTTONS
    btnQuit = Button((WIDTH//4*3), HEIGHT/8*7, btnQuit, 0.8)
    btnBack = Button(WIDTH//10, HEIGHT/8*7, btnBack, 0.8)

    # DISPLAY
    pygame.display.set_caption("Query")

    SCREEN.fill(BLACK)

    clock = pygame.time.Clock()
    while True:
        # Sets FPS to 60. Adds background and title to screen.
        clock.tick(60)
        SCREEN.blit(background, (0, 0))
        SCREEN.blit(title, titleRect)

        # Adds buttons to screen and checks if it is pressed every frame
        if btnBack.draw(SCREEN):
            main()
        if btnQuit.draw(SCREEN):
            pygame.quit()
            sys.exit()

        # Quits program if application is closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


def searchVoice():
    return


main()
