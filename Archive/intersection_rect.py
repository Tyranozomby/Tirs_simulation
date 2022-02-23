from typing import Optional, Tuple

from structures import Point, Rectangle


def intersection_rectangle(rectangle: Rectangle, debut: Point, fin: Point) -> Tuple[Point, Tuple[Point, Point]]:
    intersections = [
        (intersection_ligne(debut, fin, rectangle.hg, rectangle.bg), (rectangle.hg, rectangle.bg)),
        (intersection_ligne(debut, fin, rectangle.bg, rectangle.bd), (rectangle.bg, rectangle.bd)),
        (intersection_ligne(debut, fin, rectangle.bd, rectangle.hd), (rectangle.bd, rectangle.hd)),
        (intersection_ligne(debut, fin, rectangle.hd, rectangle.hg), (rectangle.hd, rectangle.hg))
    ]

    inter_min = None
    ligne_min = None
    dist = None

    print(intersections)
    for inter, ligne in intersections:
        if inter:
            temp_dist = inter.distance_points(debut)
            if dist is None or temp_dist < dist:
                dist = temp_dist
                inter_min = inter
                ligne_min = ligne
    return inter_min, ligne_min


def intersection_ligne(start1: Point, end1: Point, start2: Point, end2: Point) -> Optional[Point]:
    # https://gamedev.stackexchange.com/questions/111100/intersection-of-a-line-and-a-rectangle
    a1 = end1.y - start1.y
    b1 = start1.x - end1.x

    a2 = end2.y - start2.y
    b2 = start2.x - end2.x

    delta = a1 * b2 - a2 * b1

    if delta == 0:
        return None

    c2 = a2 * start2.x + b2 * start2.y
    c1 = a1 * start1.x + b1 * start1.y

    inv_delta = 1 / delta

    return Point((b2 * c1 - b1 * c2) * inv_delta, (a1 * c2 - a2 * c1) * inv_delta)
