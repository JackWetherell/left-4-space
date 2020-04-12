'''Define the game object and all possible states'''
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
        '''Initialise the game objects'''
        self.state = GameStates.MENU
        self.player = entities.Player(position=Vector(370, 480))
        self.enemy_grid = entities.EnemyGrid(dimentions=(8, 3), position=Vector(100, 50), spacing=Vector(80, 70))
        self.bullets = []
        self.bombs = []
        self.score = 0

    def check_input(self):
        '''Check the input and make the changes to the game objects, defining the controls'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = GameStates.QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == 276 or event.unicode == 'a':
                    self.player.update_velocity(Directions.LEFT)
                if event.key == 275 or event.unicode == 'd':
                    self.player.update_velocity(Directions.RIGHT)
                if event.unicode == ' ':
                    self.player.fire()
            if event.type == pygame.KEYUP:
                if event.key == 97 or event.key == 100 or event.key == 276  or  event.key == 275:
                    self.player.update_velocity(Directions.NONE)

    def update(self, resolution, fps, dt, timestep, time):
        # update player
        self.player.update_position(dt, limits=resolution)
        if self.player.firing is True:
            self.bullets.append(entities.Bullet(position=self.player.position + Vector(21, -64)))
            self.player.firing = False
        if self.player.last_timestep_fire is not None:
            self.player.last_timestep_fire += 1

        # update enemies
        if int(timestep * 2.5) % fps  == 0:
            self.enemy_grid.update_position(limits=resolution)
        for enemy in self.enemy_grid.enemies:
            if collision(enemy, self.player):
                self.player.health -= 10
                self.enemy_grid.enemies.remove(enemy)

        # update bombs
        if int(timestep * 2.0) % fps  == 0:
            for enemy in self.enemy_grid.enemies:
                if random.random() < enemy.fire_chance:
                    self.bombs.append(entities.Bomb(position=enemy.position + Vector(21, 34)))

        # update bullets
        for bullet in self.bullets:
            bullet.update_position(dt)
            if bullet.position.y <= -bullet.hieght:
                self.bullets.remove(bullet)
            for enemy in self.enemy_grid.enemies:
                if collision(bullet, enemy):
                    try:
                        self.bullets.remove(bullet)
                    except ValueError:
                        pass
                    self.enemy_grid.enemies.remove(enemy)
                    self.score += 1

        # update bombs
        for bomb in self.bombs:
            bomb.update_position(dt)
            if bomb.position.y > resolution[1] + bomb.hieght:
                self.bombs.remove(bomb)
            if collision(bomb, self.player):
                self.player.health -= 10
                self.bombs.remove(bomb)
