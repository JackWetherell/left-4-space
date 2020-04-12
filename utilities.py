from enum import Enum


class Directions(Enum):
    '''Define at the possible directions'''
    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class Vector:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector(x, y)

    def __mul__(self, other):
        x = self.x * other
        y = self.y * other
        return Vector(x, y)

    def __str__(self):
        return '({0}, {1})'.format(self.x, self.y)

    def __iter__(self):
        items = [self.x, self.y]
        for i in items:
            yield i


def collision(entity1, entity2):
    rect1 = entity1.image.get_rect()
    rect2 = entity2.image.get_rect()
    rect1.move_ip(entity1.position.x, entity1.position.y)
    rect2.move_ip(entity2.position.x, entity2.position.y)
    return rect1.colliderect(rect2)
