import pygame
import numpy as np
from abc import ABC as Interface
from abc import abstractmethod
from utilities import Vector
from utilities import Directions


class Entitiy(Interface):
    @abstractmethod
    def update_position(self):
        pass


class Player(Entitiy):
    def __init__(self, position):
        self.image = pygame.image.load('data/player.png')
        self.width = self.image.get_rect()[2]
        self.hieght = self.image.get_rect()[3]
        self.position = position
        self.velocity = Vector(0, 0)
        self.speed = 500.0
        self.last_timestep_fire = None
        self.sleep_time = 50
        self.max_health = 100
        self.health = self.max_health
        self.firing = False

    def update_velocity(self, direction):
        if direction == Directions.LEFT:
            self.velocity.x = -self.speed
        elif direction == Directions.RIGHT:
            self.velocity.x = self.speed
        elif direction == Directions.NONE:
            self.velocity.x = 0
        else:
            raise ValueError('direction must be a valid direction, got {}'.format(direction))

    def update_position(self, dt, limits):
        self.position += self.velocity*dt
        if self.position.x <= 0:
            self.position.x = 0
        if self.position.x >= limits[0] - self.width:
            self.position.x = limits[0] - self.width

    def fire(self):
        if self.last_timestep_fire == None or self.last_timestep_fire > self.sleep_time:
            self.firing = True
            self.last_timestep_fire = 0


class Bullet(Entitiy):
    def __init__(self, position):
        self.image = pygame.image.load('data/bullet.png')
        self.width = self.image.get_rect()[2]
        self.hieght = self.image.get_rect()[3]
        self.position = position
        self.velocity = Vector(0, -200)

    def update_position(self, dt):
        self.position += self.velocity*dt


class Bomb(Entitiy):
    def __init__(self, position):
        self.image = pygame.image.load('data/bomb.png')
        self.width = self.image.get_rect()[2]
        self.hieght = self.image.get_rect()[3]
        self.position = position
        self.velocity = Vector(0, 350)

    def update_position(self, dt):
        self.position += self.velocity*dt


class Enemy(Entitiy):
    def __init__(self, position):
        self.image = pygame.image.load('data/ufo.png')
        self.width = self.image.get_rect()[2]
        self.hieght = self.image.get_rect()[3]
        self.position = position - Vector(self.width / 2, self.hieght / 2)
        self.magnitude = 30.0
        self.velocity = 1.0
        self.fire_chance = 0.15

    def update_position(self):
        self.position.x += self.magnitude * self.velocity

    def shift(self):
        self.position.y += self.magnitude * 1.0


class EnemyGrid():
    def __init__(self, dimentions, position, spacing):
        self.enemies = []
        for i in range(dimentions[0]):
            for j in range(dimentions[1]):
                x = position.x + spacing.x*i
                y = position.y + spacing.y*j
                self.enemies.append(Enemy(position=Vector(x, y)))

    def update_position(self, limits):
        for enemy in self.enemies:
            enemy.update_position()
        for enemy in self.enemies:
            if enemy.position.x <= 0:
                self.shift(1)
                break
            if enemy.position.x >= limits[0] - enemy.width:
                self.shift(-1)
                break

    def shift(self, direction):
        assert direction == -1 or  direction == 1, 'direction must be -1 or 1, got {}.'.format(direction)
        for enemy in self.enemies:
            enemy.velocity = direction
            enemy.update_position()
            enemy.shift()
