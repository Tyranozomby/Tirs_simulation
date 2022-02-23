from math import cos, radians, sin
from typing import List, Optional, Tuple

import pygame

from intersection_cercle import intersection_cercle
from intersection_rect import intersection_rectangle
from structures import Cercle, Point, Rectangle

MAX_REBONDS = 1


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
        self.touche = False
        self.points = [self.depart]

    def calculer(self, obstacles: List[Rectangle]):
        origine = self.depart
        angle = self.angle
        for i in range(0, MAX_REBONDS):
            p_rebond, obstacle = self.calculer_segment(origine, angle, obstacles)
            self.points.append(p_rebond)
            if obstacle:
                # TODO angle et origine
                return p_rebond
            else:
                self.touche = True
                break

    def calculer_segment(self, origine: Point, angle: float, obstacles: List[Rectangle]) -> Tuple[Point, Optional[Tuple[Point, Point]]]:

        direction = pygame.Vector2(cos(radians(angle)),
                                   sin(radians(angle)))
        d1 = origine
        d2 = d1 + direction * 900

        touche = intersection_cercle(self.cible, d1, d2)

        inter_obs = []
        for rect in obstacles:
            col, ligne = intersection_rectangle(rect, d1, d2)
            if col:
                inter_obs.append((col, ligne))

        inter_min = None
        ligne_min = None
        dist = None

        for inter, ligne in inter_obs:
            if inter:
                temp_dist = inter.distance_points(d1)
                if dist is None or temp_dist < dist:
                    dist = temp_dist
                    inter_min = inter
                    ligne_min = ligne

        if touche and inter_min is None:
            return touche, None
        elif not touche:
            return Point(0, 0), None
        else:  # Rebond
            return inter_min, ligne_min

    def draw(self, screen: pygame.Surface):
        for a, b in zip(self.points, self.points[1:]):
            color = "green" if self.touche else "red"
            pygame.draw.line(screen, color, a.tuple(), b.tuple())
