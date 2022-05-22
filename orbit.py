import pygame
import math

pygame.init()
WIDTH = HEIGHT = 800  # pixels
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLACK = (000, 000, 000)
FONT = pygame.font.SysFont("comicsans", 16)
FRAMES = 30


class Planet:
    G = 6.67428e-11  # gravitational const
    TIME_INC = 86400  # one day in secs
    AU = 149.6e9  # in meters
    SCALE = 230 / AU  # convert AU to pixels
    PLANET_SCALE = 4000
    SUN_SCALE = 60

    def __init__(self, x, y, img, dia, mass, isSun, xVel=0, yVel=0):
        self.x = x * self.AU
        self.y = y * self.AU
        dim = dia * self.SCALE
        if not isSun:  # scale up planet size
            dim = dim * self.PLANET_SCALE
        else:  # scale up the size of the sun (less)
            dim = dim * self.SUN_SCALE
        self.img = pygame.transform.scale(img, (dim, dim))
        self.mass = mass
        self.isSun = isSun
        self.sunDist = 0
        self.xVel = xVel
        self.yVel = yVel

    def display(self):
        x = self.x * self.SCALE + WIDTH / 2 - self.img.get_width() // 2
        y = self.y * self.SCALE + HEIGHT / 2 - self.img.get_height() // 2
        SCREEN.blit(self.img, (x, y))
        if not self.isSun:
            distance_text = FONT.render(
                "{:.3e}km".format(self.sunDist), 1, WHITE)
            SCREEN.blit(distance_text, (x - distance_text.get_width() /
                        2,  y - distance_text.get_height()/2 - 10))

    def gravity(self, plnt):
        xDist = plnt.x - self.x
        yDist = plnt.y - self.y
        dist = math.sqrt(xDist ** 2 + yDist ** 2)
        if plnt.isSun:  # is the other plnt the sun
            self.sunDist = dist
        f = self.G * (self.mass * plnt.mass / dist**2)
        theta = math.atan2(yDist, xDist)
        fx = math.cos(theta) * f  # force in x dir
        fy = math.sin(theta) * f  # force in y dir
        return fx, fy  # return the x and y forces

    def move(self, planets):
        tfx = tfy = 0
        for plnt in planets:
            if plnt != self:
                fx, fy = self.gravity(plnt)
                tfx += fx
                tfy += fy
        self.xVel += tfx / self.mass * self.TIME_INC
        self.yVel += tfy / self.mass * self.TIME_INC
        self.x += self.xVel * self.TIME_INC
        self.y += self.yVel * self.TIME_INC


# initialize all the planets
planets = []
planets.append(Planet(0, 0, pygame.image.load(
    "assets/sun.png"), 1.3927e9, 1.98892e30, True, 0))
planets.append(Planet(0, 0.387, pygame.image.load(
    "assets/mercury.jpeg"), 4.8794e6, 3.3e23, False, 47400))
planets.append(Planet(0, 0.723, pygame.image.load(
    "assets/venus.jpeg"), 1.2104e7, 4.8685e24, False, 35020))
planets.append(Planet(0, 1.000, pygame.image.load(
    "assets/earth.jpeg"), 1.2742e7, 5.9742e24, False, 29783))
planets.append(Planet(0, 1.524, pygame.image.load(
    "assets/mars.jpeg"), 6.779e6, 6.39e23, False, 24077))

# run the simulation
sim = True
clock = pygame.time.Clock()
while sim:
    clock.tick(FRAMES)
    SCREEN.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sim = False
    for plnt in planets:
        plnt.move(planets)
        plnt.display()
    pygame.display.update()
pygame.quit()
