import pygame
import engine
import graphics


def main(resolution, fps):
    # initialse pygame
    pygame.init()

    # frame rate
    clock = pygame.time.Clock()
    dt = 1.0 / float(fps)
    timestep = 0
    time = 0.0

    # create the buffer and display
    buffer = pygame.display.set_mode(resolution)
    pygame.display.set_caption('Space Invaders - L4D')
    pygame.display.set_icon(pygame.image.load('data/spaceship.png'))

    # initialse the game
    game = engine.Game()

    # main game loop
    while game.state is not engine.GameStates.QUIT:
        game.check_input()
        game.update(resolution, fps, dt, timestep, time)
        graphics.draw(game, buffer)
        pygame.display.flip()
        clock.tick(fps)
        timestep += 1
        time += dt


if __name__ == '__main__':
    main(resolution=(800, 600), fps=120)
