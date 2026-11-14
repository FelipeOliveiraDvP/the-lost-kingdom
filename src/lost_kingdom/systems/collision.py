import math

import pygame

from lost_kingdom.core.settings import BODY_SIZE, MAP_SIZE


class Collision:
    def __init__(self, walkable: pygame.Mask) -> None:
        self.walkable = walkable
        self.footprint = pygame.Mask(BODY_SIZE, fill=True)

    def can_stand(self, body: pygame.Rect) -> bool:
        return (
            self.walkable.overlap_area(self.footprint, body.topleft)
            == self.footprint.count()
        )

    def move(self, position: pygame.Vector2, delta: pygame.Vector2) -> bool:
        # Small axis-separated steps prevent tunneling and allow sliding along banks.
        steps = max(1, math.ceil(max(abs(delta.x), abs(delta.y)) / 4))
        step = delta / steps
        original = position.copy()
        body = pygame.Rect((0, 0), BODY_SIZE)
        for _ in range(steps):
            for axis in (0, 1):
                candidate = position.copy()
                candidate[axis] += step[axis]
                body.center = (round(candidate.x), round(candidate.y))
                if self.can_stand(body):
                    position.update(candidate)
        return position != original

    def clear_line(self, start: pygame.Vector2, end: pygame.Vector2) -> bool:
        steps = max(1, math.ceil(start.distance_to(end) / 3))
        for index in range(steps + 1):
            point = start.lerp(end, index / steps)
            x, y = round(point.x), round(point.y)
            if not (0 <= x < MAP_SIZE[0] and 0 <= y < MAP_SIZE[1]):
                return False
            if not self.walkable.get_at((x, y)):
                return False
        return True
