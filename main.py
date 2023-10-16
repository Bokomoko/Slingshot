import sys

import pygame
from pygame.locals import QUIT

WIDTH, HEIGHT = 800, 600
PLANET_MASS = 100
SHIP_MASS = 5
G = 5
FPS = 60
PLANET_SIZE = 50
OBJ_SIZE = 5
VEL_SCALE = 100
BG = pygame.transform.scale(pygame.image.load("assets/background.jpg"),
                            (WIDTH, HEIGHT))
PLANET = pygame.transform.scale(pygame.image.load("assets/jupiter.png"),
                                (PLANET_SIZE * 2, PLANET_SIZE * 2))
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LEFT_MOUSE = 1
RIGHT_MOUSE = 3


def main():
  pygame.init()
  clock = pygame.time.Clock()
  win = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption('Space orbit simulation!')
  # a list of positions and velocities
  spacecrafts = []
  adding_spacecraft = False
  while True:
    clock.tick(FPS)
    mouse_pos = pygame.mouse.get_pos()
    velocity_vector = mouse_pos
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        print("Thansk for playing")
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == LEFT_MOUSE:
          if not adding_spacecraft:
            adding_spacecraft = True
            # add a spacecraft with velocity 0
            spacecrafts.append([mouse_pos, (0, 0)])
          else:
            adding_spacecraft = False
            if len(spacecrafts):
              print(spacecrafts[-1])
              print(velocity_vector)
              spacecrafts[-1][1] = (velocity_vector[0] - spacecrafts[-1][1][0],
                                    velocity_vector[1] - spacecrafts[-1][1][1])

        if event.button == RIGHT_MOUSE:
          # remove the last spacecraft
          spacecrafts.pop()

    win.blit(BG, (0, 0))
    win.blit(PLANET, (WIDTH // 2 - PLANET_SIZE, HEIGHT // 2 - PLANET_SIZE))
    # will draw the updates after the background and before
    # the display.update()

    # first, draw the existing spacecrafts
    for spacecraft in spacecrafts:
      pygame.draw.circle(win, RED, spacecraft[0], OBJ_SIZE)

    # if adding a new spacecraft draw the velocity vector
    if adding_spacecraft:
      if len(spacecrafts):
        pygame.draw.line(win, BLUE, spacecrafts[-1][0], velocity_vector, 2)

    pygame.display.update()


if __name__ == "__main__":
  main()
