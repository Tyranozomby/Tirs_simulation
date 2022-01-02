from math import cos, radians, sin
from typing import List

import pygame

from intersection_cercle import intersection_cercle
from structures import Cercle, Point

MAX_REBONDS = 3


class Tir:
    points: List[Point]
    touche: bool
    depart: Point
    angle: float
    cible: Cercle

    def __init__(self, depart: Point, angle: float, cible: Cercle):
        self.depart = depart
        self.angle = angle
        self.cible = cible
        self.points = [self.depart]

    def calculer(self):
        origine = self.depart
        angle = self.angle
        for i in range(0, MAX_REBONDS):
            p_rebond, collision = self.calculer_segment(origine, angle)
            self.points.append(p_rebond)
            if collision:
                # TODO angle et origine
                pass
            else:
                self.touche = True
                break
        self.touche = False

    def calculer_segment(self, origine: Point, angle: float):
        direction = pygame.Vector2(cos(radians(angle)),
                                   sin(radians(angle)))
        d1 = origine
        d2 = d1 + direction * 900

        truc = intersection_cercle(self.cible, d1, d2)

        if truc:
            return truc, None
        else:  # Rebond
            # TODO rebond
            return Point(0, 0), Point(0, 0)

    def draw(self, screen: pygame.Surface):
        for a, b in zip(self.points, self.points[1:]):
            color = "green" if self.touche else "red"
            pygame.draw.line(screen, color, a.tuple(), b.tuple())
