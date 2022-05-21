import pygame
import math
pygame.init()

# Set width, height, and caption
width, height = 800, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Query")

white = (255, 255, 255)


def main():
    run = True

    while run:
        # Make sures it runs at 60FPS
        pygame.time.Clock().tick(60)

        window.fill(white)

        # Update frames
        pygame.display.update()

        # As long as game is running, run. If app closes, quit the program.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()


# Run main
main()
