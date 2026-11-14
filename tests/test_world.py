from collections import deque

import pygame
import pytest

from lost_kingdom.entities import Coin, Direction, Enemy, State
from lost_kingdom.level import COIN_SPAWNS, ENEMY_SPAWNS
from lost_kingdom.settings import BODY_SIZE, START, Settings
from lost_kingdom.world import Controls, World


@pytest.mark.parametrize(
    ("movement", "facing"),
    [
        ((-1, 0), Direction.LEFT),
        ((1, 0), Direction.RIGHT),
        ((0, -1), Direction.UP),
        ((0, 1), Direction.DOWN),
        ((1, 1), Direction.DOWN),
    ],
)
def test_movement_speed_and_facing(world, movement, facing):
    start = world.player.position.copy()
    world.update(0.2, Controls(pygame.Vector2(movement)))
    assert world.player.position.distance_to(start) == pytest.approx(36)
    assert world.player.facing is facing


def test_frame_rate_independent_movement(level):
    worlds = [World(level, Settings()) for _ in range(2)]
    for world in worlds:
        world.enemies.clear()
        world.coins.clear()
        world.player.position.update(600, 1190)
    controls = Controls(pygame.Vector2(1, 0))
    worlds[0].update(0.25, controls)
    for _ in range(25):
        worlds[1].update(0.01, controls)
    assert worlds[0].player.position.distance_to(worlds[1].player.position) < 0.001


@pytest.mark.parametrize(
    ("start", "movement", "minimum_x", "maximum_x"),
    [
        ((578, 1000), (-400, 0), 553, 578),  # Bridge bank and water.
        ((280, 640), (120, 0), 280, 308),  # Tree trunk.
        ((510, 1260), (150, 0), 510, 520),  # START monument.
        ((778, 780), (-300, 0), 746, 778),  # Lake and raised bank.
    ],
)
def test_solid_obstacles_cannot_be_crossed(
    level, start, movement, minimum_x, maximum_x
):
    position = pygame.Vector2(start)
    level.move(position, pygame.Vector2(movement))
    assert minimum_x <= position.x <= maximum_x
    body = pygame.Rect((0, 0), BODY_SIZE)
    body.center = position
    assert level.can_stand(body)


def test_full_body_collision_and_sliding(level):
    position = pygame.Vector2(558, 1000)
    level.move(position, pygame.Vector2(-60, -60))
    assert position.x >= 552
    assert position.y == pytest.approx(940)
    assert not level.can_stand(pygame.Rect(-5, 100, *BODY_SIZE))


@pytest.mark.parametrize("facing", list(Direction))
def test_melee_is_directional_and_deals_one_damage(world, facing):
    player = world.player
    player.facing = facing
    front = Enemy(player.position + facing.vector * 40)
    behind = Enemy(player.position - facing.vector * 40)
    distant = Enemy(player.position + facing.vector * 105)
    world.enemies = [front, behind, distant]
    world.update(1 / 60, Controls(attack=True))
    assert front.health == 0
    assert front not in world.enemies
    assert behind.health == distant.health == 1
    assert world.events.count("enemy-dying") == 1


def test_attack_cooldown_and_facing_lock(world):
    player = world.player
    player.facing = Direction.RIGHT
    world.update(0.01, Controls(attack=True))
    assert not player.attack(world.settings)
    world.update(0.1, Controls(pygame.Vector2(-1, 0)))
    assert player.facing is Direction.RIGHT
    world.update(0.25, Controls())
    assert player.attack_left == 0
    assert not player.attack(world.settings)
    world.update(0.13, Controls())
    assert player.attack(world.settings)


def test_attacks_and_chasing_do_not_pass_through_solids(world):
    world.player.position.update(631, 1289)
    world.player.facing = Direction.RIGHT
    enemy = Enemy(pygame.Vector2(677, 1289))
    assert not world.level.clear_line(world.player.position, enemy.position)
    world.enemies = [enemy]
    world.update(0.1, Controls(attack=True))
    assert enemy.health == 1
    assert enemy.position.x > 677  # Patrols rather than chasing through the pillar.


def test_contact_damage_invulnerability_and_defeat(world):
    player = world.player
    assert player.health == 5
    world.enemies = [Enemy(player.position.copy()) for _ in range(3)]
    world.update(0.01, Controls())
    assert player.health == 4
    world.update(1.0, Controls())
    assert player.health == 4
    for remaining in (3, 2, 1, 0):
        world.update(1.21, Controls())
        assert player.health == remaining
    assert world.state is State.GAME_OVER
    assert "player-dying" in world.events
    before = player.position.copy()
    world.update(1.0, Controls(pygame.Vector2(1, 0), attack=True))
    assert player.position == before
    assert player.attack_left == 0
    assert player.health == 0


def test_coin_is_counted_once_and_removed(world):
    coin = Coin(world.player.position.copy())
    world.coins = [coin]
    world.update(0.01, Controls())
    assert world.player.coins == 1
    assert not world.coins
    assert world.events == ["getting-coin"]
    world.update(1.0, Controls())
    assert world.player.coins == 1
    assert not world.events


def test_enemy_patrol_and_chase(world):
    enemy = Enemy(pygame.Vector2(710, 1190))
    world.enemies = [enemy]
    world.update(0.1, Controls())
    assert enemy.position.x < 710
    world.player.position.update(360, 1200)
    before = enemy.position.copy()
    world.update(0.1, Controls())
    assert enemy.position.x > before.x


def test_victory_without_coins_and_terminal_state(world):
    world.player.position.update(world.level.goal.center)
    world.update(0.01, Controls())
    assert world.state is State.VICTORY
    assert world.player.coins == 0
    assert world.events == ["winning-level"]
    before = world.player.position.copy()
    world.update(2.0, Controls(pygame.Vector2(0, 1), True))
    assert world.player.position == before
    assert not world.events


def test_defeat_takes_precedence_over_goal(world):
    world.player.position.update(world.level.goal.center)
    world.player.health = 1
    world.enemies = [Enemy(world.player.position.copy())]
    world.update(0.01, Controls())
    assert world.state is State.GAME_OVER
    assert "winning-level" not in world.events


@pytest.mark.parametrize("combat", [False, True])
def test_start_to_goal_is_walkable(world, combat):
    world.player.position.update(START)
    if combat:
        world.enemies = [Enemy(pygame.Vector2(point)) for point in ENEMY_SPAWNS]
        world.coins = [Coin(pygame.Vector2(point)) for point in COIN_SPAWNS]
    waypoints = (
        (690, 1320),
        (690, 1190),
        (578, 1190),
        (578, 880),
        (777, 880),
        (777, 675),
        (951, 675),
        (951, 404),
        (541, 404),
        (541, 95),
    )
    for waypoint in waypoints:
        target = pygame.Vector2(waypoint)
        for _ in range(500):
            offset = target - world.player.position
            if offset.length() < 3 or world.state is State.VICTORY:
                break
            world.update(1 / 60, Controls(offset.normalize(), attack=combat))
        else:
            pytest.fail(f"Route blocked before {waypoint}: {world.player.position}")
    assert world.state is State.VICTORY
    if combat:
        assert world.player.health > 0
        assert world.player.coins > 0
        assert len(world.enemies) < len(ENEMY_SPAWNS)


def test_all_collectibles_and_enemies_are_reachable(level):
    step = 8
    visited = {START}
    queue = deque([START])
    body = pygame.Rect((0, 0), BODY_SIZE)
    while queue:
        x, y = queue.popleft()
        for neighbor in ((x - step, y), (x + step, y), (x, y - step), (x, y + step)):
            if neighbor in visited:
                continue
            body.center = neighbor
            if level.can_stand(body):
                visited.add(neighbor)
                queue.append(neighbor)
    for x, y in (*COIN_SPAWNS, *ENEMY_SPAWNS, level.goal.center):
        assert any(abs(px - x) <= step and abs(py - y) <= step for px, py in visited), (
            f"Unreachable level element: {(x, y)}"
        )


def test_pause_freezes_all_simulation(world):
    world.enemies = [Enemy(pygame.Vector2(710, 1190))]
    world.player.attack(world.settings)
    before = world.enemies[0].position.copy()
    cooldown = world.player.cooldown
    world.state = State.PAUSED
    world.update(30, Controls(pygame.Vector2(1, 0), True))
    assert world.elapsed == 0
    assert world.player.cooldown == cooldown
    assert world.enemies[0].position == before


@pytest.mark.parametrize("dt", [-1, float("nan"), float("inf")])
def test_invalid_frame_duration_is_reported(world, dt):
    with pytest.raises(ValueError, match="Frame duration"):
        world.update(dt, Controls())
