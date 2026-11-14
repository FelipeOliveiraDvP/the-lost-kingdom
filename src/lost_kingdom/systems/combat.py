from lost_kingdom.core.settings import Settings
from lost_kingdom.entities.enemy import Enemy
from lost_kingdom.entities.player import Player
from lost_kingdom.systems.collision import Collision


def resolve_combat(
    player: Player, enemy: Enemy, collision: Collision, settings: Settings
) -> str | None:
    if (
        player.attack_left > 0
        and player.attack_box.colliderect(enemy.body)
        and collision.clear_line(player.position, enemy.position)
    ):
        enemy.health -= 1
        return "enemy-dying"
    if player.body.colliderect(enemy.body) and player.take_damage(settings):
        enemy.contact_left = 0.35
        return "player-hit" if player.health else "player-dying"
    return None
