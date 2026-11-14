import math

import pygame

from lost_kingdom.core.settings import MAP_SIZE, SCREEN_SIZE
from lost_kingdom.core.states import State
from lost_kingdom.entities.actor import Actor
from lost_kingdom.entities.enemy import Enemy
from lost_kingdom.resources.assets import Resources
from lost_kingdom.systems.world import World
from lost_kingdom.ui.components import GOLD, GREEN, INK, UI
from lost_kingdom.ui.hud import draw_hud


class GameScene:
    def __init__(self, world: World, resources: Resources, ui: UI) -> None:
        self.world = world
        self.resources = resources
        self.ui = ui
        self.camera = pygame.Vector2()

    def _screen_position(self, position: pygame.Vector2) -> tuple[int, int]:
        return round(position.x - self.camera.x), round(position.y - self.camera.y)

    def _draw_actor(
        self,
        target: pygame.Surface,
        actor: Actor,
        kind: str,
        state: State,
        state_time: float,
    ) -> None:
        animation = "walk" if actor.moving else "idle"
        time = actor.animation_time
        duration = None
        if kind == "player":
            player = self.world.player
            if state is State.GAME_OVER:
                animation, time, duration = "death", state_time, 0.7
            elif player.attack_left:
                animation = "attack"
                duration = self.world.settings.attack_duration
                time = duration - player.attack_left
            elif player.hurt_left:
                animation, time, duration = "hurt", 0.22 - player.hurt_left, 0.22
            if (
                player.invulnerable_left
                and state is State.PLAYING
                and int(self.world.elapsed * 14) % 2
            ):
                return
        elif isinstance(actor, Enemy) and actor.contact_left:
            animation, time, duration = "attack", 0.35 - actor.contact_left, 0.35
        frame = self.resources.frame(kind, animation, actor.facing, time, duration)
        x, y = self._screen_position(actor.position)
        target.blit(frame, (x - 64, y - 94))

    def draw(self, target: pygame.Surface, state: State, state_time: float) -> None:
        world = self.world
        player = world.player
        self.camera.update(
            max(0, min(MAP_SIZE[0] - SCREEN_SIZE[0], player.position.x - 480)),
            max(0, min(MAP_SIZE[1] - SCREEN_SIZE[1], player.position.y - 390)),
        )
        target.blit(self.resources.map, (-round(self.camera.x), -round(self.camera.y)))
        goal_center = self._screen_position(pygame.Vector2(world.level.goal.center))
        radius = 24 + round(3 * math.sin(world.elapsed * 3))
        pygame.draw.circle(target, GOLD, goal_center, radius, 2)
        self.ui.text(
            target,
            "SANTUARIO",
            (goal_center[0], goal_center[1] - 44),
            20,
            GOLD,
            True,
        )
        for coin in world.coins:
            x, y = self._screen_position(coin.position)
            phase = world.elapsed * 4 + coin.position.x / 70
            self.ui.coin(
                target,
                (x, y + round(math.sin(phase) * 3)),
                max(4, round(abs(math.cos(phase)) * 15)),
            )
        for fallen in world.fallen:
            frame = self.resources.frame(
                "enemy", "death", fallen.facing, fallen.age, 0.65
            )
            x, y = self._screen_position(fallen.position)
            target.blit(frame, (x - 64, y - 94))
        actors: list[tuple[Actor, str]] = [(player, "player")]
        actors.extend((enemy, "enemy") for enemy in world.enemies)
        for actor, kind in sorted(actors, key=lambda item: item[0].position.y):
            self._draw_actor(target, actor, kind, state, state_time)
        draw_hud(
            target, self.ui, player.health, world.settings.max_health, player.coins
        )
        self.ui.panel(target, pygame.Rect(336, 18, 288, 44))
        self.ui.text(target, "^  ALCANCE O SANTUARIO", (480, 40), 23, GOLD, True)
        self.ui.panel(target, pygame.Rect(808, 522, 132, 178))
        target.blit(self.resources.minimap, (814, 531))
        marker = (
            814 + round(player.position.x / MAP_SIZE[0] * 120),
            531 + round(player.position.y / MAP_SIZE[1] * 160),
        )
        pygame.draw.circle(target, INK, marker, 5)
        pygame.draw.circle(target, GREEN, marker, 3)
        pygame.draw.circle(target, GOLD, (874, 541), 3)
