import pygame
import sys
from button import Button
from query import answerQuery as aq
import speech_recognition as sr

pygame.init()

# VARIABLES
WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLURPLE = (138, 43, 226)
BLUE = (0, 0, 128)
BLACK = (0, 0, 0)
PLANETS = ["earth", "jupiter", "mars", "mercury",
           "neptune", "saturn", "uranus", "venus", "sun"]


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
    title = font.render("Welcome to Space Query!", True, WHITE, BLUE)
    titleRect = title.get_rect()
    titleRect.center = (WIDTH//2, HEIGHT//8)

    # BUTTONS
    btnSearch = Button(WIDTH//4*3, HEIGHT//4, btnSearch, 0.8)
    btnQuit = Button(WIDTH//4*3, HEIGHT//8*7, btnQuit, 0.8)
    btnSearchVoice = Button(WIDTH//4*3, HEIGHT//2, btnSearchVoice, 0.8)

    # TEXT INPUT
    baseFont = pygame.font.Font(None, 40)
    userText = ""
    previousLetters = 0
    inputRect = pygame.Rect(WIDTH//10, HEIGHT//8*2, 800, 50)
    activeColour = pygame.Color("cadetblue1")
    passiveColour = pygame.Color("blueviolet")
    colour = passiveColour
    active = False

    # VOICE INPUT
    searchVoice = False
    voiceText = ""
    voiceInputrect = pygame.Rect(WIDTH//10, HEIGHT//2, 800, 50)
    voiceActiveColour = pygame.Color("cadetblue1")
    voicePassiveColour = pygame.Color("blueviolet")
    voiceColour = passiveColour
    voiceActive = False

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
            spaceQuery(userText)
        if btnSearchVoice.draw(SCREEN):
            voiceText = "Ask your question."

            # DISPLAY VOICE INPUT
            voiceColour = voiceActiveColour
            pygame.draw.rect(SCREEN, voiceColour, voiceInputrect)
            voiceTextSurface = baseFont.render(
                voiceText, True, (255, 255, 255))
            SCREEN.blit(voiceTextSurface,
                        (voiceInputrect.x+5, voiceInputrect.y+5))
            pygame.display.flip()
            searchVoice = True
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

        # DISPLAY VOICE INPUT
        voiceColour = voicePassiveColour
        pygame.draw.rect(SCREEN, voiceColour, voiceInputrect)
        voiceTextSurface = baseFont.render(
            voiceText, True, (255, 255, 255))
        SCREEN.blit(voiceTextSurface, (voiceInputrect.x+5, voiceInputrect.y+5))
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
                        spaceQuery(userText)
            if searchVoice:
                # variable for checking if the program did't cath the voice
                correct = True
                r = sr.Recognizer()
                while correct:
                    text = ''
                    with sr.Microphone() as source:
                        # listen for 1 second to calibrate the energy threshold for ambient noise levels
                        r.adjust_for_ambient_noise(source)
                        audio_data = r.listen(source)
                        correct = True
                        try:
                            text = r.recognize_google(audio_data)
                            voiceText = "Did you say: " + text

                            # DISPLAY VOICE INPUT
                            voiceColour = voicePassiveColour
                            pygame.draw.rect(
                                SCREEN, voiceColour, voiceInputrect)
                            voiceTextSurface = baseFont.render(
                                voiceText, True, (255, 255, 255))
                            SCREEN.blit(
                                voiceTextSurface, (voiceInputrect.x+5, voiceInputrect.y+5))
                            pygame.display.flip()

                            while correct:
                                if btnSearchVoice.rect.collidepoint(event.pos):
                                    spaceQuery(voiceText)
                                elif background.rect.collidepoint(event.pos):
                                    correct = False
                                    raise Exception()
                        except:
                            voiceText = "Sorry, I didn't get that. Try again."
                            # DISPLAY VOICE INPUT
                            voiceColour = voicePassiveColour
                            pygame.draw.rect(
                                SCREEN, voiceColour, voiceInputrect)
                            voiceTextSurface = baseFont.render(
                                voiceText, True, (255, 255, 255))
                            SCREEN.blit(
                                voiceTextSurface, (voiceInputrect.x+5, voiceInputrect.y+5))
                            pygame.display.flip()
                            main()
                searchVoice = False

                # except sr.RequestError as e:
                #print("Could not request results from Google Speech Recognition service; {0}".format(e))

        pygame.display.update()


def spaceQuery(userText):
    # LOAD IMGS
    background = pygame.image.load("assets/spaceBG.jpeg")
    btnQuit = pygame.image.load("assets/btnQuit.png").convert_alpha()
    btnBack = pygame.image.load("assets/btnBack.png").convert_alpha()
    earthImg = pygame.image.load("assets/earth.jpeg")
    jupiterImg = pygame.image.load("assets/jupiter.jpeg")
    marsImg = pygame.image.load("assets/mars.jpeg")
    mercuryImg = pygame.image.load("assets/mercury.jpeg")
    neptuneImg = pygame.image.load("assets/neptune.jpeg")
    saturnImg = pygame.image.load("assets/saturn.jpeg")
    uranusImg = pygame.image.load("assets/uranus.png")
    venusImg = pygame.image.load("assets/venus.jpeg")
    sunImg = pygame.image.load("assets/sun.jpeg")
    planetImgs = [earthImg, jupiterImg, marsImg, mercuryImg,
                  neptuneImg, saturnImg, uranusImg, venusImg, sunImg]
    for i in range(len(planetImgs)):
        planetImgs[i] = pygame.transform.scale(planetImgs[i], (250, 250))

    # TITLE
    font = pygame.font.SysFont("corbel", 60)
    title = font.render("To Answer Your Question...",
                        True, WHITE, BLUE)
    titleRect = title.get_rect()
    titleRect.center = (WIDTH//2, HEIGHT//8)

    # ANSWER
    answerText = aq(userText)[0]
    font = pygame.font.SysFont("corbel", 40)
    if len(answerText) > 60:
        answerText1 = answerText[:81]
        if answerText[81] != " ":
            answerText2 = "-" + answerText[81:]
        else:
            answerText2 = answerText[81:]

        answerText1 = font.render(answerText1, True, WHITE, BLURPLE)
        answerText2 = font.render(answerText2, True, WHITE, BLURPLE)

        answerRect1 = answerText1.get_rect()
        answerRect2 = answerText2.get_rect()

        answerRect1.center = (WIDTH//2, HEIGHT//8*3)
        answerRect2.center = (WIDTH//2, HEIGHT//2)
    else:
        answerText = font.render(answerText, True, WHITE, BLURPLE)
        answerRect = answerText.get_rect()
        answerRect.center = (WIDTH//2, HEIGHT//8*3)

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

        try:
            SCREEN.blit(answerText, answerRect)
        except:
            SCREEN.blit(answerText1, answerRect1)
            SCREEN.blit(answerText2, answerRect2)

        for i in range(len(PLANETS)):
            if PLANETS[i] in userText.lower():
                SCREEN.blit(planetImgs[i], (WIDTH//5*2, HEIGHT//3*2))

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


main()
