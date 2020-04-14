'''Define all game entities: player, enemies and projectiles'''
import random
import math
from abc import ABC as Interface
from abc import abstractmethod
import pygame
import graphics
from utilities import Vector, Directions


class IEntitiy(Interface):
    @abstractmethod
    def update_position(self):
        pass


class Player(IEntitiy):
    def __init__(self, position):
        self.image = pygame.image.load('data/player.png')
        self.width = self.image.get_rect()[2]
        self.hieght = self.image.get_rect()[3]
        self.position = position
        self.velocity = Vector(0, 0)
        self.speed = 500.0
        self.last_time_fire = None
        self.firing = False
        self.sleep_time = 0.35
        self.max_health = 100
        self.health = self.max_health
        self.damage = 5
        self.pinned_by = None
        self.pin_time = 3.0

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
        if self.pinned_by is not None:
            if self.pinned_for < self.pin_time:
                self.pinned_for += dt
                if self.pinned_by == Hunter:
                    self.health -= 5.0*dt
                if self.pinned_by == Jockey:
                    self.position.x += math.sin(2*self.pinned_for)
                    if self.position.x <= 0:
                        self.position.x = 0
                    if self.position.x >= limits[0] - self.width:
                        self.position.x = limits[0] - self.width
            else:
                self.pinned_by = None
        else:
            self.position += self.velocity * dt
            if self.position.x <= 0:
                self.position.x = 0
            if self.position.x >= limits[0] - self.width:
                self.position.x = limits[0] - self.width

    def fire(self):
        if self.pinned_by is None:
            if self.last_time_fire == None or self.last_time_fire > self.sleep_time:
                self.firing = True
                self.last_time_fire = 0.0

    def hit(self, game, bomb):
        self.health -= bomb.damage
        if bomb.color == graphics.Colors.SMOKER:
            self.pinned_by = Smoker
            self.pinned_for = 0.0
        elif bomb.color == graphics.Colors.HUNTER:
            self.pinned_by = Hunter
            self.pinned_for = 0.0
        elif bomb.color == graphics.Colors.JOCKEY:
            self.pinned_by = Jockey
            self.pinned_for = 0.0
        else:
            pass


class Bullet(IEntitiy):
    def __init__(self, position, damage):
        self.image = pygame.image.load('data/bullet.png')
        self.width = self.image.get_rect()[2]
        self.hieght = self.image.get_rect()[3]
        self.position = position
        self.velocity = Vector(0, -200)
        self.damage = damage

    def update_position(self, dt):
        self.position += self.velocity * dt


class Bomb(IEntitiy):
    def __init__(self, position, damage, color):
        self.width = 10
        self.hieght = self.width
        self.rect = pygame.Rect(0, 0, self.width, self.hieght)
        self.position = position
        self.velocity = Vector(0, 350)
        self.damage = damage
        self.color = color

    def update_position(self, dt):
        self.position += self.velocity * dt


class Enemy(IEntitiy):
    def __init__(self, position):
        self.image = pygame.image.load('data/enemy.png')
        self.width = self.image.get_rect()[2]
        self.hieght = self.image.get_rect()[3]
        self.position = position - Vector(self.width/2.0, self.hieght/2.0)
        self.step = Vector(30.0, 30.0)
        self.fire_chance = 0.05
        self.fire_rate = 3.0
        self.damage = 5
        self.max_health = 10
        self.health = self.max_health
        self.color = graphics.Colors.ENEMY

    def update_position(self, dt):
        self.position.x += self.step.x

    def shift(self):
        self.position.y += self.step.y

    def hit(self, game, bullet):
        self.health -= bullet.damage


class Hoard(Enemy):
    def __init__(self, position):
        super().__init__(position)
        self.image = pygame.image.load('data/hoard.png')
        self.color = graphics.Colors.HOARD
        self.probability = None


class Witch(Enemy):
    probability = 0.015

    def __init__(self, position):
        super().__init__(position)
        self.image = pygame.image.load('data/witch.png')
        self.fire_chance = 0.0
        self.damage = 100
        self.max_health = 100
        self.health = self.max_health
        self.color = graphics.Colors.WITCH

    def update_position(self, dt):
        self.position.x += self.step.x
        self.health -= 1.5

    def hit(self, game, bullet):
        game.player.health -= self.damage


class Tank(Enemy):
    probability = 0.02

    def __init__(self, position):
        super().__init__(position)
        self.image = pygame.image.load('data/tank.png')
        self.fire_chance = 0.15
        self.damage = 30
        self.max_health = 100
        self.health = self.max_health
        self.color = graphics.Colors.TANK


class Boomer(Enemy):
    probability = 0.04

    def __init__(self, position):
        super().__init__(position)
        self.image = pygame.image.load('data/boomer.png')
        self.fire_chance = 0.1
        self.damage = 5
        self.max_health = 5
        self.health = self.max_health
        self.color = graphics.Colors.BOOMER

    def hit(self, game, bullet):
        for enemy in game.enemy_grid.enemies:
            enemy.health = enemy.max_health
        self.health -= bullet.damage


class Smoker(Enemy):
    probability = 0.04

    def __init__(self, position):
        super().__init__(position)
        self.image = pygame.image.load('data/smoker.png')
        self.fire_chance = 0.15
        self.damage = 5
        self.max_health = 20
        self.health = self.max_health
        self.color = graphics.Colors.SMOKER


class Hunter(Enemy):
    probability = 0.04

    def __init__(self, position):
        super().__init__(position)
        self.image = pygame.image.load('data/hunter.png')
        self.fire_chance = 0.15
        self.damage = 5
        self.max_health = 20
        self.health = self.max_health
        self.color = graphics.Colors.HUNTER


class Jockey(Enemy):
    probability = 0.04

    def __init__(self, position):
        super().__init__(position)
        self.image = pygame.image.load('data/jockey.png')
        self.fire_chance = 0.15
        self.damage = 5
        self.max_health = 20
        self.health = self.max_health
        self.color = graphics.Colors.JOCKEY


class EnemyGrid():
    def __init__(self, dimentions, position, spacing):
        self.move_rate = 10.5
        self.enemies = []
        for i in range(dimentions[0]):
            for j in range(dimentions[1]):
                x = position.x + spacing.x * i
                y = position.y + spacing.y * j
                # enemy = Jockey(position=Vector(x, y))
                enemy = None
                for special in [Jockey, Hunter, Smoker, Boomer, Tank, Witch]:
                    if random.random() < special.probability:
                        enemy = special(position=Vector(x, y))
                        break
                if enemy == None:
                    enemy = Hoard(position=Vector(x, y))
                self.enemies.append(enemy)
                # return

    def update_position(self, dt, limits):
        for enemy in self.enemies:
            enemy.update_position(dt)
        for enemy in self.enemies:
            if enemy.position.x <= 0:
                self.shift(dt)
                break
            if enemy.position.x >= limits[0] - enemy.width:
                self.shift(dt)
                break

    def shift(self, dt):
        max_y = 0
        for enemy in self.enemies:
            enemy.step.x = -enemy.step.x
            enemy.update_position(dt)
            if enemy.position.y > max_y:
                max_y = enemy.position.y
        if max_y < 450:
            for enemy in self.enemies:
                enemy.shift()
