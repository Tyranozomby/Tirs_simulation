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
class Character:
    pos: Point
    radius: int
    color: str

    def __init__(self, pos: Point, radius: int, color: str):
        self.pos = pos
        self.radius = radius
        self.color = color

    def draw(self, screen: Canvas):
        x0 = self.pos.x - self.radius
        y0 = self.pos.y - self.radius
        x1 = self.pos.x + self.radius
        y1 = self.pos.y + self.radius

        screen.create_oval(x0, y0, x1, y1, fill=self.color, outline=self.color)

    # Indicate if this circle is in another one (collision detection)
    def is_in(self, other: "Character") -> bool:
        if other is None:
            return False

        dx = self.pos.x - other.pos.x
        dy = self.pos.y - other.pos.y

        distance = sqrt(dx * dx + dy * dy)

        return distance < self.radius + other.radius


class Wall:
    top_left: Point
    top_right: Point
    bottom_left: Point
    bottom_right: Point

    center: Point
    width: float
    height: float

    color: str

    def __init__(self, p1: Point, p2: Point, color: str):
        self.top_left = Point(0, 0)
        self.bottom_right = Point(0, 0)
        self.center = Point(0, 0)

        self.top_left.x, self.bottom_right.x = (p1.x, p2.x) if p1.x < p2.x else (p2.x, p1.x)
        self.top_left.y, self.bottom_right.y = (p1.y, p2.y) if p1.y < p2.y else (p2.y, p1.y)

        self.height = self.bottom_right.y - self.top_left.y
        self.width = self.bottom_right.x - self.top_left.x

        self.bottom_left = Point(self.top_left.x, self.top_left.y + self.height)
        self.top_right = Point(self.top_left.x + self.width, self.top_left.y)

        self.center.x = self.top_left.x + self.width / 2
        self.center.y = self.top_left.y + self.height / 2

        self.color = color

    def draw(self, screen: Canvas):
        screen.create_rectangle(self.top_left.x, self.top_left.y, self.bottom_right.x, self.bottom_right.y,
                                fill=self.color, outline=self.color)

    def surface(self):
        return self.width * self.height

    def is_in(self, other: Character):
        if other is None:
            return False

        circle_distance = Point(abs(self.center.x - other.pos.x), abs(self.center.y - other.pos.y))
        if circle_distance.x >= (self.width / 2 + other.radius) or circle_distance.y >= (
                self.height / 2 + other.radius):
            return False

        if circle_distance.x < (self.width / 2) or circle_distance.y < (self.height / 2):
            return True

        corner_distance_sq = (circle_distance.x - self.width / 2) ** 2 + (
                circle_distance.y - self.height / 2) ** 2
        return corner_distance_sq < other.radius ** 2
