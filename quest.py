""" Quest - An epic journey.

Simple demo that demonstrates PyTMX and pyscroll.

requires pygame and pytmx.

https://github.com/bitcraft/pytmx

pip install pytmx
"""
from __future__ import annotations

from pathlib import Path
from typing import List

import numpy as np
import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_MINUS, K_EQUALS, K_ESCAPE, K_r
from pygame.locals import KEYDOWN, VIDEORESIZE, QUIT
from pytmx.util_pygame import load_pygame
import math
import pyscroll
import pyscroll.data
from pyscroll.group import PyscrollGroup

# define configuration variables here
CURRENT_DIR = Path(__file__).parent
RESOURCES_DIR = CURRENT_DIR / "data"
HERO_MOVE_SPEED = 200  # pixels per second


# simple wrapper to keep the screen resizeable
def init_screen(width: int, height: int) -> pygame.Surface:
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    return screen


# make loading images a little easier
def load_image(filename: str) -> pygame.Surface:
    return pygame.image.load(str(RESOURCES_DIR / filename))


class Hero(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = load_image("smalltruck.png").convert_alpha()
        self.orig_image = self.image;
        self.speed = 0
        self.accelleration = 0.001
        self.angle = 0
        self._position = [0.0, 0.0]
        self.rect = self.image.get_rect()

    @property
    def position(self) -> List[float]:
        return list(self._position)

    @position.setter
    def position(self, value: List[float]) -> None:
        self._position = list(value)

    def update(self, dt: float) -> None:
        self.image = pygame.transform.rotate(self.orig_image,self.angle)
        self.rect.topleft = self._position
        print('speed: '+str(self.speed))
        #self._position[0] = self._position[0] + math.cos(self.angle) * self.speed;
        #self._position[1] = self._position[1] + math.sin(self.angle) * self.speed;
        self._position[1] = self._position[1] + math.cos(np.radians(self.angle)) * self.speed;
        self._position[0] = self._position[0] + math.sin(np.radians(self.angle)) * self.speed;


    def steer_right(self):
        self.angle -= .5

    def steer_left(self):
        self.angle += .5
    
    def accellerate(self):
        self.speed += self.accelleration

    def deccellerate(self):
        if self.speed > 0:
            self.speed -= self.accelleration
    
    def brake(self):
        if self.speed > 0:
            self.speed -= self.accelleration * 2

    def move_back(self, dt: float) -> None:
        self._position = self._old_position
        self.rect.topleft = self._position


class QuestGame:
    map_path = "map.tmx"

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen

        # true while running
        self.running = False

        # load data from pytmx
        tmx_data = load_pygame(self.map_path)

        # setup level geometry with simple pygame rects, loaded from pytmx
        self.walls = []
        for obj in tmx_data.objects:
            self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # create new renderer (camera)
        self.map_layer = pyscroll.BufferedRenderer(
            data=pyscroll.data.TiledMapData(tmx_data),
            size=screen.get_size(),
            clamp_camera=False,
        )
        self.map_layer.zoom = 2

        self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=2)

        # put the hero in the center of the map
        self.hero = Hero()
        self.hero.position = self.map_layer.map_rect.center

        # add our hero to the group
        self.group.add(self.hero)

    def draw(self) -> None:
        # center the map/screen on our Hero
        self.group.center(self.hero.rect.center)

        # draw the map and all sprites
        self.group.draw(self.screen)

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                break

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    break

                elif event.key == K_r:
                    self.map_layer.reload()

                elif event.key == K_EQUALS:
                    self.map_layer.zoom += 0.25

                elif event.key == K_MINUS:
                    value = self.map_layer.zoom - 0.25
                    if value > 0:
                        self.map_layer.zoom = value

            # this will be handled if the window is resized
            elif event.type == VIDEORESIZE:
                self.screen = init_screen(event.w, event.h)
                self.map_layer.set_size((event.w, event.h))

        # use `get_pressed` for an easy way to detect held keys
        pressed = pygame.key.get_pressed()
        if pressed[K_UP]:
            self.hero.accellerate()
        elif pressed[K_DOWN]:
            self.hero.brake()
        else:
            self.hero.deccellerate()
        if pressed[K_LEFT]:
            self.hero.steer_left();
        elif pressed[K_RIGHT]:
            self.hero.steer_right()
    def update(self, dt: float):
        """
        Tasks that occur over time should be handled here

        """
        self.group.update(dt)

        # check if the sprite's feet are colliding with wall
        # sprite must have a rect called feet, and move_back method,
        # otherwise this will fail
        for sprite in self.group.sprites():
            if sprite.rect.collidelist(self.walls) > -1:
                sprite.move_back(dt)

    def run(self):
        """
        Run the game loop

        """
        clock = pygame.time.Clock()
        self.running = True

        try:
            while self.running:
                dt = clock.tick() / 1000.0
                self.handle_input()
                self.update(dt)
                self.draw()
                pygame.display.flip()

        except KeyboardInterrupt:
            self.running = False


def main() -> None:
    pygame.init()
    pygame.font.init()
    screen = init_screen(800, 600)
    pygame.display.set_caption("Quest - An epic journey.")

    try:
        game = QuestGame(screen)
        game.run()
    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
