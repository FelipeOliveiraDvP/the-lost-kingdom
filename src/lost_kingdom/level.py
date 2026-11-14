import math

import pygame

from lost_kingdom.settings import BODY_SIZE, GOAL, MAP_SIZE, START

# Coordinates are in the original map's pixels, independent of camera and sprites.
LAND = (
    (
        (230, 1343),
        (444, 1343),
        (444, 1398),
        (676, 1398),
        (676, 1343),
        (851, 1343),
        (851, 1195),
        (813, 1164),
        (765, 1154),
        (763, 1092),
        (615, 1092),
        (615, 1050),
        (542, 1050),
        (542, 1084),
        (323, 1084),
        (315, 1129),
        (281, 1155),
        (230, 1162),
    ),
    (
        (542, 1092),
        (616, 1092),
        (616, 914),
        (798, 914),
        (798, 715),
        (985, 715),
        (985, 373),
        (596, 373),
        (596, 145),
        (484, 145),
        (484, 405),
        (160, 405),
        (160, 901),
        (452, 901),
        (452, 746),
        (735, 746),
        (735, 835),
        (542, 835),
    ),
    ((503, 145), (584, 145), (584, 51), (503, 51)),
)

# Water, raised banks, trees, rocks and the monuments are solid, not just artwork.
SOLID_RECTS = (
    (272, 447, 426, 96),
    (469, 530, 229, 181),
    (530, 1239, 76, 64),
    (454, 1276, 27, 27),
    (642, 1277, 24, 26),
    (506, 1328, 111, 49),
)
SOLID_ELLIPSES = (
    (300, 613, 42, 62),
    (250, 719, 33, 32),
    (232, 741, 34, 33),
    (401, 749, 25, 27),
    (382, 553, 25, 25),
    (400, 666, 25, 27),
    (415, 853, 25, 28),
    (742, 458, 44, 65),
    (809, 488, 32, 36),
    (872, 554, 27, 29),
    (349, 1127, 27, 28),
    (409, 1113, 27, 28),
    (313, 1306, 26, 29),
    (723, 1302, 27, 30),
)

ENEMY_SPAWNS = (
    (420, 1190),
    (695, 1150),
    (580, 985),
    (685, 877),
    (780, 765),
    (905, 665),
    (934, 460),
    (733, 403),
    (355, 417),
    (191, 636),
    (369, 825),
    (542, 310),
    (542, 191),
)
COIN_SPAWNS = (
    (700, 1282),
    (362, 1220),
    (474, 1166),
    (684, 1190),
    (578, 1107),
    (578, 1024),
    (578, 933),
    (650, 880),
    (727, 880),
    (778, 813),
    (778, 731),
    (853, 675),
    (951, 623),
    (951, 527),
    (908, 405),
    (799, 405),
    (648, 403),
    (542, 396),
    (542, 266),
    (542, 165),
    (421, 427),
    (193, 459),
    (193, 575),
    (193, 776),
    (313, 865),
    (423, 799),
)


class Level:
    def __init__(self) -> None:
        surface = pygame.Surface(MAP_SIZE, pygame.SRCALPHA)
        for polygon in LAND:
            pygame.draw.polygon(surface, "white", polygon)
        for rect in SOLID_RECTS:
            pygame.draw.rect(surface, (0, 0, 0, 0), rect)
        for ellipse in SOLID_ELLIPSES:
            pygame.draw.ellipse(surface, (0, 0, 0, 0), ellipse)
        self.walkable = pygame.mask.from_surface(surface)
        self.footprint = pygame.Mask(BODY_SIZE, fill=True)
        self.goal = pygame.Rect(GOAL)
        for position in (START, *ENEMY_SPAWNS, *COIN_SPAWNS, self.goal.center):
            body = pygame.Rect((0, 0), BODY_SIZE)
            body.center = position
            if not self.can_stand(body):
                raise ValueError(f"Level spawn is obstructed: {position}")

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
