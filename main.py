import pygame
from button import Button

pygame.init()

# Button colours: Green 15d798,
# VARIABLES
WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)


def main():
    # LOAD IMGS
    background = pygame.image.load("assets/spaceBG.jpeg")
    btnSpaceQuery = pygame.image.load(
        "assets/btnSpaceQuery.png").convert_alpha()
    btnQuit = pygame.image.load("assets/btnQuit.png").convert_alpha()

    # TITLE
    font = pygame.font.SysFont("corbel", 60)
    title = font.render("Welcome to Space Query!", True, GREEN, BLUE)
    titleRect = title.get_rect()
    titleRect.center = (WIDTH//2, HEIGHT//8)

    # BUTTONS
    btnSpaceQuery = Button(WIDTH//4*3, HEIGHT//8*2, btnSpaceQuery, 0.8)
    btnQuit = Button(WIDTH/5*3, HEIGHT/3*2, btnQuit, 0.8)

    # TEXT INPUT
    baseFont = pygame.font.Font(None, 40)
    userText = ""
    previousLetters = 0
    inputRect = pygame.Rect(WIDTH//10, HEIGHT//8*2, 600, 50)
    activeColour = pygame.Color("cadetblue1")
    passiveColour = pygame.Color("blueviolet")
    colour = passiveColour
    active = False

    # DISPLAY
    pygame.display.set_caption("Main Menu")
    clock = pygame.time.Clock()
    run = True
    while run:
        # Sets FPS to 60. Adds background and title to screen.
        clock.tick(60)
        SCREEN.blit(background, (0, 0))
        SCREEN.blit(title, titleRect)

        # Adds buttons to screen and checks if it is pressed every frame
        if btnSpaceQuery.draw(SCREEN):
            print("PRESSED")
        if btnQuit.draw(SCREEN):
            run = False

        # Puts input text box on display
        if active:
            colour = activeColour
        else:
            colour = passiveColour
        pygame.draw.rect(SCREEN, colour, inputRect)
        textSurface = baseFont.render(
            userText[previousLetters:], True, (255, 255, 255))
        SCREEN.blit(textSurface, (inputRect.x+5, inputRect.y+5))
        inputRect.w = max(800, textSurface.get_width()+10)
        pygame.display.flip()

        # Quits program if application is closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

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
                        print(userText)

        pygame.display.update()


def spaceQuery():
    return


main()
