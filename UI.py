import pygame
import math
pygame.init()

# Set width, height, and caption
resolution = (800, 800)
window = pygame.display.set_mode(resolution)
pygame.display.set_caption("Space Query")

width = window.get_width()
height = window.get_height()

white = (255, 255, 255)
mouse = pygame.mouse.get_pos()

# BUTTON
color_light = (170, 170, 170)
color_dark = (100, 100, 100)

# font
smallfont = pygame.font.SysFont('Corbel', 35)

# rendering a text
text = smallfont.render('QUIT', True, white)


def main():
    run = True

    while run:

        window.fill(white)
        mouse = pygame.mouse.get_pos()

        # As long as game is running, run. If app closes, quit the program.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:
                    run = False

        if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:
            pygame.draw.rect(window, color_light, [width/2, height/2, 140, 40])

        else:
            pygame.draw.rect(window, color_dark, [width/2, height/2, 140, 40])

        window.blit(text, (width/2+50, height/2))

        # Make sures it runs at 60FPS
        pygame.time.Clock().tick(60)

        # Update frames
        pygame.display.update()

    pygame.quit()


main()
