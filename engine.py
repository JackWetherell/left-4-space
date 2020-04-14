'''Define the game mechanics and all possible states'''
import random
from enum import Enum
import pygame
import entities
from utilities import Vector, Directions, collision


class GameStates(Enum):
    '''Define at the possible states the game can be in'''
    QUIT = 0
    MAIN = 1
    PAUSED = 2
    MENU = 3
    INFO = 4
    DEAD = 5


class Game():
    def __init__(self):
        self.state = GameStates.MENU
        self.player = entities.Player(position=Vector(370, 480))
        self.enemy_grid = entities.EnemyGrid(dimentions=(8, 3), position=Vector(100, 50), spacing=Vector(80, 90))
        self.bullets = []
        self.bombs = []

    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = GameStates.QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == 276 or event.key == 97:
                    self.player.update_velocity(Directions.LEFT)
                if event.key == 275 or event.key == 100:
                    self.player.update_velocity(Directions.RIGHT)
                if event.unicode == ' ':
                    self.player.fire()
            if event.type == pygame.KEYUP:
                if event.key == 97 or event.key == 100 or event.key == 276  or  event.key == 275:
                    self.player.update_velocity(Directions.NONE)

    def update(self, resolution, fps, dt, timestep, time):
        # move player
        self.player.update_position(dt, limits=resolution)

        # fire bullet
        if self.player.firing is True:
            self.bullets.append(entities.Bullet(position=self.player.position + Vector(21, -64), damage=self.player.damage))
            self.player.firing = False
        if self.player.last_time_fire is not None:
            self.player.last_time_fire += dt

        # move bullets
        for bullet in self.bullets:
            bullet.update_position(dt)

        # check bullet collision
        for bullet in self.bullets:
            if bullet.position.y <= -bullet.hieght:
                self.bullets.remove(bullet)
            for enemy in self.enemy_grid.enemies:
                if collision(bullet, enemy):
                    try:
                        self.bullets.remove(bullet)
                    except ValueError:
                        pass
                    enemy.hit(self, bullet)

        # move enemies
        if int(timestep * self.enemy_grid.move_rate) % fps == 0:
            self.enemy_grid.update_position(limits=resolution)

        # remove dead enemies
        for enemy in self.enemy_grid.enemies:
            if enemy.health <= 0:
                self.enemy_grid.enemies.remove(enemy)

        # fire bombs
        for enemy in self.enemy_grid.enemies:
            if int(timestep * enemy.fire_rate) % fps  == 0:
                if random.random() < enemy.fire_chance:
                    self.bombs.append(entities.Bomb(position=enemy.position + Vector(35, 40), damage=enemy.damage, color=enemy.color))

        # move bombs
        for bomb in self.bombs:
            bomb.update_position(dt)

        # check bomb collision
        for bomb in self.bombs:
            if bomb.position.y > resolution[1] + bomb.hieght:
                self.bombs.remove(bomb)
            if collision(bomb, self.player):
                self.player.hit(self, bomb)
                self.bombs.remove(bomb)

        # check player-enemy collision
        for enemy in self.enemy_grid.enemies:
            if collision(enemy, self.player):
                self.player.health -= enemy.damage*3
                self.enemy_grid.enemies.remove(enemy)
