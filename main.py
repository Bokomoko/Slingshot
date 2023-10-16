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


def main():
  pygame.init()
  clock = pygame.time.Clock()
  win = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption('Space orbit simulation!')
  while True:
    clock.tick(FPS)
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        print("Thansk for playing")
        sys.exit()
    win.blit(BG, (0, 0))
    win.blit(PLANET, (WIDTH // 2 - PLANET_SIZE, HEIGHT // 2 - PLANET_SIZE))
    pygame.display.update()


if __name__ == "__main__":
  main()
