import pygame

from lost_kingdom.core.settings import FPS, SCREEN_SIZE, Settings
from lost_kingdom.core.states import Action, State
from lost_kingdom.entities.actor import Direction
from lost_kingdom.resources.assets import Resources
from lost_kingdom.resources.audio import Audio
from lost_kingdom.scenes import game_over, menu, pause, victory
from lost_kingdom.scenes.game_scene import GameScene
from lost_kingdom.systems.level import Level
from lost_kingdom.systems.world import Controls, World
from lost_kingdom.ui.components import CREAM, INK, UI, Button


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
        self.scene = GameScene(
            World(self.level, self.settings), self.resources, self.ui
        )
        self.state = State.MENU
        self.state_time = 0.0
        self.selected = 0
        self.running = True
        self.viewport = pygame.Rect((0, 0), SCREEN_SIZE)

    def transition(self, state: State) -> None:
        self.state = state
        self.scene.world.state = state
        self.state_time = 0.0
        self.selected = 0
        self.audio.pause(state is State.PAUSED)

    def activate(self, action: Action) -> None:
        match action:
            case Action.START:
                self.audio.stop_effects()
                self.scene.world = World(self.level, self.settings)
                self.transition(State.PLAYING)
            case Action.RESUME:
                self.transition(State.PLAYING)
            case Action.MENU:
                self.audio.stop_effects()
                self.transition(State.MENU)
            case Action.EXIT:
                self.running = False

    def buttons(self) -> list[Button]:
        match self.state:
            case State.MENU:
                return menu.buttons()
            case State.PAUSED:
                return pause.buttons()
            case State.GAME_OVER:
                return game_over.buttons()
            case State.VICTORY:
                return victory.buttons()
            case State.PLAYING:
                return []

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
            choices = self.buttons()
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
            world = self.scene.world
            world.update(dt, controls)
            for event in world.events:
                self.audio.play(event)
            if world.state is not State.PLAYING:
                self.transition(world.state)

    def _resize_viewport(self) -> None:
        width, height = self.window.get_size()
        scale = min(width / SCREEN_SIZE[0], height / SCREEN_SIZE[1])
        self.viewport = pygame.Rect(
            0, 0, round(SCREEN_SIZE[0] * scale), round(SCREEN_SIZE[1] * scale)
        )
        self.viewport.center = (width // 2, height // 2)

    def draw(self) -> pygame.Surface:
        self.scene.draw(self.canvas, self.state, self.state_time)
        match self.state:
            case State.MENU:
                menu.draw(self.canvas, self.ui, self.selected)
            case State.PAUSED:
                pause.draw(self.canvas, self.ui, self.selected)
            case State.GAME_OVER:
                game_over.draw(
                    self.canvas, self.ui, self.selected, self.scene.world.player.coins
                )
            case State.VICTORY:
                victory.draw(
                    self.canvas, self.ui, self.selected, self.scene.world.player.coins
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
