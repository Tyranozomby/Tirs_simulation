from math import sqrt
from tkinter import Canvas


# Class representing a geometrical point on the window
class Point:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


# Class representing a circle for the shooter or the target
class Circle:
    pos: Point
    radius: int
    color: str

    def __init__(self, pos: Point, rayon: int, couleur: str):
        self.pos = pos
        self.radius = rayon
        self.color = couleur

    def draw(self, screen: Canvas):
        x0 = self.pos.x - self.radius
        y0 = self.pos.y - self.radius
        x1 = self.pos.x + self.radius
        y1 = self.pos.y + self.radius

        screen.create_oval(x0, y0, x1, y1, fill=self.color, outline=self.color)

    # Indicate if this circle is in another one (collision detection)
    def is_in(self, other: "Circle"):
        dx = self.pos.x - other.pos.x
        dy = self.pos.y - other.pos.y

        distance = sqrt(dx * dx + dy * dy)

        return distance < self.radius + other.radius


class Rectangle:
    pass  # TODO
