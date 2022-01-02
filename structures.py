from math import sqrt
from typing import Union

import pygame

W_COLOR = "black"


class Point:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __getitem__(self, item: int) -> float:
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            return 0

    def __add__(self, other):
        if other is Point or pygame.Vector2:
            return Point(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return str(self.tuple()) + '#' + str(id(self))

    def distance_points(self, to: "Point") -> float:
        return sqrt(((self[0] - to[0]) ** 2) + ((self[1] - to[1]) ** 2))

    def vers(self, point: "Point") -> pygame.Vector2:
        return pygame.Vector2(self.x - point.x, self.y - point.y)

    def tuple(self):
        return self.x, self.y

    def clone(self):
        return Point(self.x, self.y)


class Cercle:
    pos: Point
    rayon: float
    couleur: Union[str, pygame.Color]

    def __init__(self, pos: Point, rayon: float, couleur: Union[str, pygame.Color]):
        self.pos = pos
        self.rayon = rayon
        self.couleur = couleur

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.couleur, self.pos.tuple(), self.rayon)


class Rectangle:
    hg: Point
    bd: Point
    height: float
    weight: float

    def __init__(self, p1: Point, p2: Point):
        self.hg = Point(0, 0)
        self.bd = Point(0, 0)

        self.hg.x, self.bd.x = (p1.x, p2.x) if p1.x < p2.x else (p2.x, p1.x)
        self.hg.y, self.bd.y = (p1.y, p2.y) if p1.y < p2.y else (p2.y, p1.y)

        self.height = self.bd.y - self.hg.y
        self.weight = self.bd.x - self.hg.x

    def __repr__(self):
        return f"{self.hg = } et {self.bd = }"

    def draw(self, screen: pygame.Surface):
        rect = pygame.Rect(self.hg.x, self.hg.y, self.weight, self.height)
        pygame.draw.rect(screen, W_COLOR, rect)

    def is_in(self, p: Point) -> bool:
        return (self.bd.x >= p.x >= self.hg.x) and (self.bd.y >= p.y >= self.hg.y)
