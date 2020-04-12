'''Define the graphics'''
import random
from enum import Enum
import pygame
import entities
from utilities import Vector, Directions, collision


def draw(game, buffer):
    '''Draw all of the elements to the buffer'''
    buffer.fill((0, 70, 90))
    buffer.blit(game.player.image, tuple(game.player.position))
    for enemy in game.enemy_grid.enemies:
        buffer.blit(enemy.image, tuple(enemy.position))
    for bullet in game.bullets:
        buffer.blit(bullet.image, tuple(bullet.position))
    for bomb in game.bombs:
        buffer.blit(bomb.image, tuple(bomb.position))
    pygame.draw.rect(buffer, (0, 30, 50), (108, 558, 604, 24))
    pygame.draw.rect(buffer, (0, 70, 90), (110, 560, 600, 20))
    pygame.draw.rect(buffer, (0, 30, 50), (110, 560, 600*(game.player.health / game.player.max_health), 20))
