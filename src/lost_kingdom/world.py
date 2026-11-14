import math
from dataclasses import dataclass, field

import pygame

from lost_kingdom.entities import Coin, Direction, Enemy, FallenEnemy, Player, State
from lost_kingdom.level import COIN_SPAWNS, ENEMY_SPAWNS, Level
from lost_kingdom.settings import Settings


@dataclass
class Controls:
    movement: pygame.Vector2 = field(default_factory=pygame.Vector2)
    attack: bool = False


class World:
    def __init__(self, level: Level, settings: Settings) -> None:
        self.level = level
        self.settings = settings
        self.player = Player(settings)
        self.enemies = [Enemy(pygame.Vector2(point)) for point in ENEMY_SPAWNS]
        self.coins = [Coin(pygame.Vector2(point)) for point in COIN_SPAWNS]
        self.fallen: list[FallenEnemy] = []
        self.events: list[str] = []
        self.state = State.PLAYING
        self.elapsed = 0.0

    def update(self, dt: float, controls: Controls) -> None:
        if not math.isfinite(dt) or dt < 0:
            raise ValueError("Frame duration must be finite and nonnegative.")
        self.events.clear()
        if self.state is not State.PLAYING or dt == 0:
            return
        steps = max(1, math.ceil(dt / (1 / 60)))
        for _ in range(steps):
            if self.state is not State.PLAYING:
                break
            self._step(dt / steps, controls)

    def _step(self, dt: float, controls: Controls) -> None:
        self.elapsed += dt
        player = self.player
        player.tick(dt)
        movement = controls.movement.copy()
        if movement.length_squared() > 1:
            movement.normalize_ip()
        if movement.length_squared() and player.attack_left == 0:
            player.facing = Direction.from_vector(movement)
        if controls.attack:
            player.attack(self.settings)
        speed = self.settings.player_speed * (0.55 if player.attack_left else 1.0)
        player.moving = self.level.move(player.position, movement * speed * dt)

        for fallen in self.fallen:
            fallen.age += dt
        self.fallen = [fallen for fallen in self.fallen if fallen.age < 0.65]

        for enemy in self.enemies:
            self._move_enemy(enemy, dt)
            if (
                player.attack_left > 0
                and player.attack_box.colliderect(enemy.body)
                and self.level.clear_line(player.position, enemy.position)
            ):
                enemy.health -= 1
                self.fallen.append(FallenEnemy(enemy.position.copy(), enemy.facing))
                self.events.append("enemy-dying")
            elif player.body.colliderect(enemy.body) and player.take_damage(
                self.settings
            ):
                enemy.contact_left = 0.35
                self.events.append("player-hit" if player.health else "player-dying")
        self.enemies = [enemy for enemy in self.enemies if enemy.health > 0]

        if player.health == 0:
            player.moving = False
            player.attack_left = 0.0
            self.state = State.GAME_OVER
            return
        remaining_coins: list[Coin] = []
        for coin in self.coins:
            if player.body.colliderect(coin.body):
                player.coins += 1
                self.events.append("getting-coin")
            else:
                remaining_coins.append(coin)
        self.coins = remaining_coins
        if self.level.goal.collidepoint(player.position):
            self.state = State.VICTORY
            self.events.append("winning-level")

    def _move_enemy(self, enemy: Enemy, dt: float) -> None:
        enemy.animation_time += dt
        enemy.contact_left = max(0.0, enemy.contact_left - dt)
        to_player = self.player.position - enemy.position
        chasing = (
            to_player.length_squared() <= self.settings.chase_radius** 2
            and self.level.clear_line(enemy.position, self.player.position)
        )
        if chasing:
            direction = to_player
        else:
            target = enemy.home + pygame.Vector2(30 * enemy.patrol_direction, 0)
            direction = target - enemy.position
            if direction.length_squared() < 16:
                enemy.patrol_direction *= -1
        if direction.length_squared() < 1:
            enemy.moving = False
            return
        direction.normalize_ip()
        enemy.facing = Direction.from_vector(direction)
        speed = self.settings.enemy_speed * (1.0 if chasing else 0.45)
        enemy.moving = self.level.move(enemy.position, direction * speed * dt)
        if not enemy.moving and not chasing:
            enemy.patrol_direction *= -1
