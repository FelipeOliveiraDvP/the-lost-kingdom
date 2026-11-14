import math
import textwrap

import pygame

from lost_kingdom.entities import Actor, Direction, Enemy, State
from lost_kingdom.level import Level
from lost_kingdom.resources import Audio, Resources
from lost_kingdom.settings import FPS, MAP_SIZE, SCREEN_SIZE, Settings
from lost_kingdom.ui import CREAM, GOLD, GREEN, INK, UI, Action, buttons
from lost_kingdom.world import Controls, World


class Game:
    def __init__(self, settings: Settings | None = None) -> None:
        pygame.display.init()
        pygame.font.init()
        self.window = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
        pygame.display.set_caption("The Lost Kingdom")
        self.canvas = pygame.Surface(SCREEN_SIZE)
        self.settings = settings or Settings()
        self.resources = Resources()
        icon = self.resources.frame("player", "idle", Direction.DOWN, 0)
        pygame.display.set_icon(icon)
        self.audio = Audio()
        self.ui = UI()
        self.level = Level()
        self.world = World(self.level, self.settings)
        self.state = State.MENU
        self.state_time = 0.0
        self.selected = 0
        self.running = True
        self.camera = pygame.Vector2()
        self.viewport = pygame.Rect((0, 0), SCREEN_SIZE)

    def transition(self, state: State) -> None:
        self.state = state
        self.world.state = state
        self.state_time = 0.0
        self.selected = 0
        self.audio.pause(state is State.PAUSED)

    def activate(self, action: Action) -> None:
        match action:
            case Action.START:
                self.audio.stop_effects()
                self.world = World(self.level, self.settings)
                self.transition(State.PLAYING)
            case Action.RESUME:
                self.transition(State.PLAYING)
            case Action.MENU:
                self.audio.stop_effects()
                self.transition(State.MENU)
            case Action.EXIT:
                self.running = False

    def mouse_position(self, position: tuple[int, int]) -> tuple[int, int] | None:
        if not self.viewport.collidepoint(position):
            return None
        return (
            int((position[0] - self.viewport.x) * SCREEN_SIZE[0] / self.viewport.width),
            int(
                (position[1] - self.viewport.y) * SCREEN_SIZE[1] / self.viewport.height
            ),
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.VIDEORESIZE:
            self.window = pygame.display.set_mode(
                (max(480, event.w), max(360, event.h)), pygame.RESIZABLE
            )
            self._resize_viewport()
        elif event.type == pygame.WINDOWFOCUSLOST and self.state is State.PLAYING:
            self.transition(State.PAUSED)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            match self.state:
                case State.PLAYING:
                    self.transition(State.PAUSED)
                case State.PAUSED:
                    self.transition(State.PLAYING)
                case State.VICTORY | State.GAME_OVER:
                    self.activate(Action.MENU)
        elif self.state is not State.PLAYING:
            choices = buttons(self.state)
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.selected = (self.selected - 1) % len(choices)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.selected = (self.selected + 1) % len(choices)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.activate(choices[self.selected][0])
            elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
                position = self.mouse_position(event.pos)
                for index, (action, _, rect) in enumerate(choices):
                    if position is not None and rect.collidepoint(position):
                        self.selected = index
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            self.activate(action)
                        break

    @staticmethod
    def controls() -> Controls:
        keys = pygame.key.get_pressed()
        return Controls(
            pygame.Vector2(
                int(keys[pygame.K_d] or keys[pygame.K_RIGHT])
                - int(keys[pygame.K_a] or keys[pygame.K_LEFT]),
                int(keys[pygame.K_s] or keys[pygame.K_DOWN])
                - int(keys[pygame.K_w] or keys[pygame.K_UP]),
            ),
            bool(keys[pygame.K_SPACE]),
        )

    def advance(self, dt: float, controls: Controls) -> None:
        self.state_time += dt
        if self.state is State.PLAYING:
            self.world.update(dt, controls)
            for event in self.world.events:
                self.audio.play(event)
            if self.world.state is not State.PLAYING:
                self.transition(self.world.state)

    def _resize_viewport(self) -> None:
        width, height = self.window.get_size()
        scale = min(width / SCREEN_SIZE[0], height / SCREEN_SIZE[1])
        self.viewport = pygame.Rect(
            0, 0, round(SCREEN_SIZE[0] * scale), round(SCREEN_SIZE[1] * scale)
        )
        self.viewport.center = (width // 2, height // 2)

    def _screen_position(self, position: pygame.Vector2) -> tuple[int, int]:
        return round(position.x - self.camera.x), round(position.y - self.camera.y)

    def _draw_actor(self, actor: Actor, kind: str) -> None:
        animation = "walk" if actor.moving else "idle"
        time = actor.animation_time
        duration = None
        if kind == "player":
            player = self.world.player
            if self.state is State.GAME_OVER:
                animation, time, duration = "death", self.state_time, 0.7
            elif player.attack_left:
                animation = "attack"
                duration = self.settings.attack_duration
                time = duration - player.attack_left
            elif player.hurt_left:
                animation, time, duration = "hurt", 0.22 - player.hurt_left, 0.22
            if (
                player.invulnerable_left
                and self.state is State.PLAYING
                and int(self.world.elapsed * 14) % 2
            ):
                return
        elif isinstance(actor, Enemy) and actor.contact_left:
            animation, time, duration = "attack", 0.35 - actor.contact_left, 0.35
        frame = self.resources.frame(kind, animation, actor.facing, time, duration)
        x, y = self._screen_position(actor.position)
        self.canvas.blit(frame, (x - 64, y - 94))

    def _draw_world(self) -> None:
        world = self.world
        player = world.player
        self.camera.update(
            max(0, min(MAP_SIZE[0] - SCREEN_SIZE[0], player.position.x - 480)),
            max(0, min(MAP_SIZE[1] - SCREEN_SIZE[1], player.position.y - 390)),
        )
        self.canvas.blit(
            self.resources.map, (-round(self.camera.x), -round(self.camera.y))
        )
        goal_center = self._screen_position(pygame.Vector2(self.level.goal.center))
        radius = 24 + round(3 * math.sin(world.elapsed * 3))
        pygame.draw.circle(self.canvas, GOLD, goal_center, radius, 2)
        self.ui.text(
            self.canvas,
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
                self.canvas,
                (x, y + round(math.sin(phase) * 3)),
                max(4, round(abs(math.cos(phase)) * 15)),
            )
        for fallen in world.fallen:
            frame = self.resources.frame(
                "enemy", "death", fallen.facing, fallen.age, 0.65
            )
            x, y = self._screen_position(fallen.position)
            self.canvas.blit(frame, (x - 64, y - 94))
        actors: list[tuple[Actor, str]] = [(player, "player")]
        actors.extend((enemy, "enemy") for enemy in world.enemies)
        for actor, kind in sorted(actors, key=lambda item: item[0].position.y):
            self._draw_actor(actor, kind)
        self.ui.hud(self.canvas, player.health, self.settings.max_health, player.coins)
        self.ui.panel(self.canvas, pygame.Rect(336, 18, 288, 44))
        self.ui.text(self.canvas, "^  ALCANCE O SANTUARIO", (480, 40), 23, GOLD, True)
        self.ui.panel(self.canvas, pygame.Rect(808, 522, 132, 178))
        self.canvas.blit(self.resources.minimap, (814, 531))
        marker = (
            814 + round(player.position.x / MAP_SIZE[0] * 120),
            531 + round(player.position.y / MAP_SIZE[1] * 160),
        )
        pygame.draw.circle(self.canvas, INK, marker, 5)
        pygame.draw.circle(self.canvas, GREEN, marker, 3)
        pygame.draw.circle(self.canvas, GOLD, (874, 541), 3)

    def draw(self) -> pygame.Surface:
        self._draw_world()
        if self.state is not State.PLAYING:
            self.ui.overlay(
                self.canvas, self.state, self.selected, self.world.player.coins
            )
        if self.audio.warning:
            pygame.draw.rect(self.canvas, INK, (0, 701, SCREEN_SIZE[0], 19))
            self.ui.text(self.canvas, self.audio.warning, (20, 702), 20, CREAM)
        self._resize_viewport()
        self.window.fill(INK)
        self.window.blit(
            pygame.transform.scale(self.canvas, self.viewport.size), self.viewport
        )
        pygame.display.flip()
        return self.canvas

    def run(self) -> None:
        clock = pygame.time.Clock()
        while self.running:
            dt = min(clock.tick(FPS) / 1000.0, 0.05)
            for event in pygame.event.get():
                self.handle_event(event)
            if not self.running:
                break
            self.advance(dt, self.controls())
            self.draw()


def show_error(message: str) -> None:
    window = pygame.display.get_surface()
    if window is None:
        return
    ui = UI()
    window.fill(INK)
    ui.text(window, "Nao foi possivel abrir o jogo.", (30, 35), 36, GOLD)
    for index, line in enumerate(textwrap.wrap(message, width=72)[:12]):
        ui.text(window, line, (30, 100 + index * 28), 24)
    ui.text(window, "ENTER / ESC para fechar.", (30, window.get_height() - 50), 24)
    pygame.display.flip()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN
            and event.key in (pygame.K_ESCAPE, pygame.K_RETURN)
        ):
            return
