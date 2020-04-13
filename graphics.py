'''Define the game graphics, colors, and layout'''
from enum import Enum
import pygame
import entities


class Colors(Enum):
    '''Define at the possible directions'''
    BACKGROUND = (0, 0, 0)
    PLAYER = (255, 255, 255)
    ENEMY = (0, 0, 0)
    HOARD = (255, 255, 255)
    TANK = (186, 0, 0)
    WITCH = (150, 150, 150)
    SPITTER = (11, 255, 0)
    CHARGER = (255, 255, 0)
    BOOMER = (82, 131, 68)
    HUNTER = (84, 162, 255)
    SMOKER = (172, 0, 255)
    JOCKEY = (255, 184, 0)


def draw(game, buffer):
    '''Draw all of the elements to the buffer'''
    # draw the background
    buffer.fill(Colors.BACKGROUND.value)

    # draw the player
    if game.player.pinned_by == entities.Smoker:
        pygame.draw.circle(buffer, Colors.SMOKER.value, (int(game.player.position.x + game.player.width/2.0) ,int(game.player.position.y + game.player.width/2.0)), game.player.width)
    if game.player.pinned_by == entities.Hunter:
        pygame.draw.circle(buffer, Colors.HUNTER.value, (int(game.player.position.x + game.player.width/2.0) ,int(game.player.position.y + game.player.width/2.0)), game.player.width)
    buffer.blit(game.player.image, tuple(game.player.position))

    # draw the enemies
    for enemy in game.enemy_grid.enemies:
        buffer.blit(enemy.image, tuple(enemy.position))

    # draw the enemy health bars
    for enemy in game.enemy_grid.enemies:
        pygame.draw.rect(buffer, enemy.color.value, (enemy.position.x + enemy.width*0.1, enemy.position.y - enemy.hieght*0.1, enemy.width*0.8*(enemy.health / enemy.max_health), 3))

    # draw the bullets
    for bullet in game.bullets:
        buffer.blit(bullet.image, tuple(bullet.position))

    # draw the bombs
    for bomb in game.bombs:
        pygame.draw.circle(buffer, bomb.color.value, (int(bomb.position.x) ,int(bomb.position.y)), bomb.width)

    # draw the player health bar
    pygame.draw.rect(buffer, Colors.PLAYER.value, (108, 558, 604, 24))
    pygame.draw.rect(buffer, Colors.BACKGROUND.value, (110, 560, 600, 20))
    pygame.draw.rect(buffer, Colors.PLAYER.value, (110, 560, 600*max(game.player.health / game.player.max_health, 0), 20))
