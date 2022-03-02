from tkinter import Canvas
from typing import List, Optional, Tuple

from math import sin, cos, sqrt, isclose

from constantes import MAX_BOUNCES, L_COLOR, HEIGHT, WIDTH
from structures import Point, Dude, Wall


class Shot:
    angle: float
    path: List[Point]

    def __init__(self, start: Point, angle: float):
        self.angle = angle
        self.path = [start]

    def shoot(self, target: Dude, shooter: Dude, walls: List[Wall], screen):
        for i in range(MAX_BOUNCES):
            collisions: List[Tuple[Point, str, float]] = []

            direction = Vector(cos(self.angle), sin(self.angle))

            max_length = sqrt(HEIGHT ** 2 + WIDTH ** 2)

            p2: Point = (direction * max_length + self.path[i]).to_point()

            # Collision with target
            col = (Segment(self.path[i], p2).intersect_circle(target), "TARGET", 0)

            if col[0]:
                vect = (col[0] - self.path[i]).to_vector()
                if vect.angle_between(direction) >= 0:  # Test collision valid
                    collisions.append(col)

            # Collision with wall
            for wall in walls:
                inter = Segment(self.path[i], p2).intersect_rect(wall)
                if inter:
                    col = (inter[0], "WALL", inter[1].to_vector().angle_between(direction))
                    collisions.append(col)

            nearest: Tuple[Point, str, float]
            if collisions:
                nearest = collisions[0]
                for collision in collisions:
                    if nearest[0].distance(self.path[0]) > collision[0].distance(self.path[0]):
                        nearest = collision
                p2 = nearest[0]

                if nearest[1] == "TARGET":
                    self.path.append(p2)
                    return self
            # else alors test bordures

            self.path.append(p2)

    def draw(self, screen: Canvas):
        for i in range(1, len(self.path)):
            screen.create_line(self.path[i - 1].x, self.path[i - 1].y, self.path[i].x, self.path[i].y, fill=L_COLOR)


class Vector:
    x: float
    y: float

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, val: float) -> "Vector":
        return Vector(self.x * val, self.y * val)

    def __add__(self, other) -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def magnitude(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2)

    def dot(self, other) -> float:
        return self.x * other.x + self.y * other.y

    def angle_between(self, other: "Vector"):
        return self.dot(other) / (self.magnitude() * other.magnitude())

    def to_point(self):
        return Point(self.x, self.y)


class Segment:
    p1: Point
    p2: Point

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def to_vector(self) -> Vector:
        return Vector(self.p2.x - self.p1.x, self.p2.y - self.p1.y)

    def intersect_circle(self, circle: Dude) -> Optional[Point]:
        cx, cy = circle.pos.tuple()
        r = circle.radius

        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y

        a = dx ** 2 + dy ** 2
        b = 2 * (dx * (self.p1.x - cx) + dy * (self.p1.y - cy))
        c = (self.p1.x - cx) ** 2 + (self.p1.y - cy) ** 2 - r ** 2

        delta = b ** 2 - 4 * a * c

        if delta < 0:
            return None
        elif delta == 0:
            t = -b / (2 * a)
            return Point(self.p1.x + t * dx, self.p1.y + t * dy)
        else:
            t1 = (-b + sqrt(delta)) / (2 * a)
            t2 = (-b - sqrt(delta)) / (2 * a)
            p1 = Point(self.p1.x + t1 * dx, self.p1.y + t1 * dy)
            p2 = Point(self.p1.x + t2 * dx, self.p1.y + t2 * dy)

            d1 = self.p1.distance(p1)
            d2 = self.p1.distance(p2)
            if d1 < d2:
                return p1
            else:
                return p2

    def intersect_rect(self, rect: Wall) -> Tuple[Point, "Segment"]:
        inters = []
        for side in rect.sides():
            inter = self.intersect_seg(side)
            if inter:
                inters.append((inter, side))

        if inters:
            nearest = inters[0]
            for inter in inters:
                if inter[0].distance(self.p1) > nearest[0].distance(self.p1):
                    nearest = inter
            return nearest

    def intersect_seg(self, seg: "Segment") -> Optional[Point]:
        a1 = self.p2.y - self.p1.y
        b1 = self.p1.x - self.p2.x
        c1 = a1 * self.p1.x + b1 * self.p1.y

        a2 = seg.p2.y - seg.p1.y
        b2 = seg.p1.x - seg.p2.x
        c2 = a2 * seg.p1.x + b2 * seg.p1.y

        determinant = a1 * b2 - a2 * b1

        if determinant == 0:
            return None
        else:
            x = (b2 * c1 - b1 * c2) / determinant
            y = (a1 * c2 - a2 * c1) / determinant
            inter = Point(x, y)

            if isclose(self.p1.distance(inter) + self.p2.distance(inter), self.p1.distance(self.p2), rel_tol=.01):
                if isclose(seg.p1.distance(inter) + seg.p2.distance(inter), seg.p1.distance(seg.p2), rel_tol=.01):
                    return inter

        return None
