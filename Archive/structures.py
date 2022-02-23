from math import sqrt
from typing import Union

import mpmath
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
        return str(self.tuple())

    def distance_points(self, to: "Point") -> float:
        return sqrt(((self[0] - to[0]) ** 2) + ((self[1] - to[1]) ** 2))

    def vers(self, point: "Point") -> pygame.Vector2:
        return pygame.Vector2(self.x - point.x, self.y - point.y)

    def tuple(self):
        return self.x, self.y

    def clone(self):
        return Point(self.x, self.y)

    def is_in(self, debut: "Point", fin: "Point") -> bool:
        a = debut
        b = fin
        c = self

        crossproduct = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)

        # compare versus epsilon for floating point values, or != 0 if using integers
        if abs(crossproduct) > 0.000001:
            return False

        dotproduct = (c.x - a.x) * (b.x - a.x) + (c.y - a.y) * (b.y - a.y)
        if dotproduct < 0:
            return False

        squaredlengthba = (b.x - a.x) * (b.x - a.x) + (b.y - a.y) * (b.y - a.y)
        if dotproduct > squaredlengthba:
            return False


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

    def is_in(self, rect: "Rectangle") -> bool:
        circle_distance = Point(abs(self.pos.x - rect.center.x), abs(self.pos.y - rect.center.y))
        if circle_distance.x >= (rect.width / 2 + self.rayon) or circle_distance.y >= (rect.height / 2 + self.rayon):
            return False

        if circle_distance.x < (rect.width / 2) or circle_distance.y < (rect.height / 2):
            return True

        corner_distance_sq = (circle_distance.x - rect.width / 2) ** 2 + (circle_distance.y - rect.height / 2) ** 2
        return corner_distance_sq < self.rayon ** 2


class Rectangle:
    hg: Point
    bg: Point
    hd: Point
    bd: Point
    center: Point
    height: float
    width: float

    def __init__(self, hg: Point, bd: Point):
        self.hg = Point(0, 0)
        self.bd = Point(0, 0)
        self.center = Point(0, 0)

        self.hg.x, self.bd.x = (hg.x, bd.x) if hg.x < bd.x else (bd.x, hg.x)
        self.hg.y, self.bd.y = (hg.y, bd.y) if hg.y < bd.y else (bd.y, hg.y)

        self.height = self.bd.y - self.hg.y
        self.width = self.bd.x - self.hg.x

        self.bg = Point(self.hg.x, self.hg.y + self.height)
        self.hd = Point(self.hg.x + self.width, self.hg.y)

        self.center.x = self.hg.x + self.width / 2
        self.center.y = self.hg.y + self.height / 2

    def __repr__(self):
        return f"{self.hg = } et {self.bd = }"

    def draw(self, screen: pygame.Surface):
        rect = pygame.Rect(self.hg.x, self.hg.y, self.width, self.height)
        pygame.draw.rect(screen, W_COLOR, rect)
