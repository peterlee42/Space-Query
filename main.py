import pygame
from button import Button
from colours import *

pygame.init()

WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


def main_menu():
    mainMenuBG = pygame.image.load("assets/spaceBG.jpeg")
    testButton = pygame.image.load("assets/button_test.png").convert_alpha()

    pygame.display.set_caption("Menu")

    test_button = Button(100, 200, testButton, 0.8)

    run = True
    while run:
        SCREEN.blit(mainMenuBG, (0, 0))

        if test_button.draw(SCREEN):
            print("PRESSED")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()


main_menu()
