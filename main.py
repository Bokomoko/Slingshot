import sys

import pygame
from pygame.locals import QUIT

WIDTH, HEIGHT = 800, 600
PLANET_MASS = 100
SHIP_MASS = 5
G = 5
FPS = 5
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


def add_vector(v1, v2):
  return (v1[0] + v2[0], v1[1] + v2[1])


def subtract_vector(v1, v2):
  return (v1[0] - v2[0], v1[1] - v2[1])


class Ship:

  def __init__(self, position, velocity, mass):
    self.position = position
    self.velocity = velocity
    self.mass = mass

  def move(self):
    self.position = add_vector(self.position, self.velocity)

  def draw_ship(self, screen):
    pygame.draw.circle(screen, RED, self.position, OBJ_SIZE)


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
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    score_text = my_font.render('Ships: ' + str(len(spacecrafts)), True, WHITE)
    # remove ships out of bounds
    spacecrafts = [
        ship for ship in spacecrafts
        if ship.position[0] >= 0 and ship.position[0] <= WIDTH
        and ship.position[1] >= 0 and ship.position[1] <= HEIGHT
    ]
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
            spacecrafts.append(Ship(mouse_pos, (0, 0), SHIP_MASS))
          else:
            adding_spacecraft = False
            if len(spacecrafts):
              spacecrafts[-1].velocity = subtract_vector(
                  velocity_vector, spacecrafts[-1].position)

        if event.button == RIGHT_MOUSE:
          # remove the last spacecraft
          spacecrafts.pop()

    # clear the screen
    win.blit(BG, (0, 0))
    win.blit(PLANET, (WIDTH // 2 - PLANET_SIZE, HEIGHT // 2 - PLANET_SIZE))
    win.blit(score_text, (10, 10))
    # will draw the updates after the background and before
    # the display.update()

    # first, draw the existing spacecrafts
    for spacecraft in spacecrafts:
      # apply movement
      spacecraft.move()
      spacecraft.draw_ship(win)

    # if adding a new spacecraft draw the velocity vector
    if adding_spacecraft:
      if len(spacecrafts):
        pygame.draw.line(win, BLUE, spacecrafts[-1].position, velocity_vector,
                         2)

    pygame.display.update()


if __name__ == "__main__":
  main()
