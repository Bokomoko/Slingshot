import sys

import pygame
import math
from pygame.locals import QUIT

WIDTH, HEIGHT = 1000, 800
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


def add_vector(v1, v2):
  return (v1[0] + v2[0], v1[1] + v2[1])


def get_velocity(v1, v2):
  return ((v1[0] - v2[0])/VEL_SCALE, (v1[1] - v2[1])/VEL_SCALE)


class Ship:

  def __init__(self, position, velocity, mass):
    self.position = position
    self.velocity = velocity
    self.mass = mass

  def move(self, planet):
    distance = math.sqrt((self.position[0] - planet.position[0])**2 +
                         (self.position[1] - planet.position[1])**2)
    force = (G * self.mass * planet.mass) / (distance**2)
    acceleration = force / self.mass
    angle = math.atan2((planet.position[1] - self.position[1]),
                       (planet.position[0] - self.position[0]))
    pull_velocity = (math.cos(angle) * acceleration,
                     math.sin(angle) * acceleration)
    self.velocity = add_vector(self.velocity, pull_velocity)
    scaled_velocity = (self.velocity[0] ,
                       self.velocity[1] )
    self.position = add_vector(self.position, scaled_velocity)

  def draw_ship(self, screen):
    pygame.draw.circle(screen, RED, self.position, OBJ_SIZE)


class Planet:

  def __init__(self, position, mass):
    self.position = position
    self.mass = mass

  def draw(self, screen):
    screen.blit(
        PLANET,
        (self.position[0] - PLANET_SIZE, self.position[1] - PLANET_SIZE))

  def has_collided_with(self, ship):
    distance = ((self.position[0] - ship.position[0])**2 +
                (self.position[1] - ship.position[1])**2)**0.5
    return distance < PLANET_SIZE + OBJ_SIZE


def main():
  pygame.init()
  clock = pygame.time.Clock()
  win = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption('Space orbit simulation!')
  # a list of Ship obejcts
  spacecrafts = []
  adding_spacecraft = False
  jupiter = Planet((WIDTH // 2, HEIGHT // 2), PLANET_MASS)
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
    # remove the ships that collided with the planet
    spacecrafts = [
        ship for ship in spacecrafts if not jupiter.has_collided_with(ship)
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
              spacecrafts[-1].velocity = get_velocity(velocity_vector,
                                                      spacecrafts[-1].position)

        if event.button == RIGHT_MOUSE:
          # remove the last spacecraft
          if len(spacecrafts):
            spacecrafts.pop()

    # clear the screen
    win.blit(BG, (0, 0))
    jupiter.draw(win)
    win.blit(score_text, (10, 10))
    # will draw the updates after the background and before
    # the display.update()

    # first, draw the existing spacecrafts
    for spacecraft in spacecrafts:
      # apply movement
      spacecraft.move(jupiter)
      spacecraft.draw_ship(win)

    # if adding a new spacecraft draw the velocity vector
    if adding_spacecraft:
      if len(spacecrafts):
        pygame.draw.line(win, BLUE, spacecrafts[-1].position, velocity_vector,
                         2)

    pygame.display.update()


if __name__ == "__main__":
  main()
