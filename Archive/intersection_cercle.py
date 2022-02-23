from math import sqrt
from typing import Tuple, Optional

from structures import Cercle, Point


def intersection_cercle(cercle: Cercle, debut: Point, fin: Point) -> Optional[Point]:
    a, b, nb = intersections(cercle, debut, fin)

    if nb == 0:
        return None
    elif nb == 1:
        return a
    else:
        return a if a.distance_points(debut) < b.distance_points(debut) else b


def intersections(cercle, debut, fin) -> Tuple[Optional[Point], Optional[Point], int]:
    # https://stackoverflow.com/questions/23016676/line-segment-and-circle-intersection
    cx, cy = cercle.pos.tuple()
    r = cercle.rayon

    dx = fin.x - debut.x
    dy = fin.y - debut.y

    a = dx ** 2 + dy ** 2
    b = 2 * (dx * (debut.x - cx) + dy * (debut.y - cy))
    c = (debut.x - cx) ** 2 + (debut.y - cy) ** 2 - r ** 2

    delta = b ** 2 - 4 * a * c

    if delta < 0:
        return None, None, 0
    elif delta == 0:
        t = -b / (2 * a)
        return Point(debut.x + t * dx, debut.y + t * dy), None, 1
    else:
        t1 = (-b + sqrt(delta)) / (2 * a)
        t2 = (-b - sqrt(delta)) / (2 * a)
        return Point(debut.x + t1 * dx, debut.y + t1 * dy), Point(debut.x + t2 * dx, debut.y + t2 * dy), 2
