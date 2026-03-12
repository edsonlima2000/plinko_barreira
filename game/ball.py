from __future__ import annotations

from dataclasses import dataclass, field
import math

import pygame

import settings


@dataclass
class Ball:
    id: int
    x: float
    y: float
    radius: int = settings.BALL_RADIUS
    speed: float = settings.BALL_SPEED
    state: str = "WAITING"
    selected: bool = False
    abandoned: bool = False
    reached_barrier: bool = False
    reached_final: bool = False
    final_slot: int | None = None
    release_delay: float = 0.0
    pin_collision_cooldown: float = 0.0
    last_pin_collision: tuple[int, int] | None = None
    _path: list[tuple[float, float]] = field(default_factory=list)
    _path_index: int = 0

    def set_path(self, path: list[tuple[float, float]], state: str) -> None:
        self._path = path
        self._path_index = 0
        self.state = state

    def append_path(self, path: list[tuple[float, float]], state: str) -> None:
        self._path = path
        self._path_index = 0
        self.state = state

    def toggle_selected(self) -> None:
        if self.state == "AT_BARRIER":
            self.selected = not self.selected

    def contains(self, pos: tuple[int, int]) -> bool:
        return math.dist((self.x, self.y), pos) <= self.radius + 4

    def abandon(self) -> None:
        self.abandoned = True
        self.selected = False
        self.state = "ABANDONED"

    def update(self, dt: float) -> None:
        if self.pin_collision_cooldown > 0:
            self.pin_collision_cooldown = max(0.0, self.pin_collision_cooldown - dt)
            if self.pin_collision_cooldown == 0:
                self.last_pin_collision = None

        if self.release_delay > 0:
            self.release_delay = max(0.0, self.release_delay - dt)
            return

        if self.state not in {"FALLING_PHASE_1", "FALLING_PHASE_2"} or self._path_index >= len(self._path):
            return

        target_x, target_y = self._path[self._path_index]
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)
        if distance <= self.speed * dt:
            self.x = target_x
            self.y = target_y
            self._path_index += 1
            if self._path_index >= len(self._path):
                if self.state == "FALLING_PHASE_1":
                    self.reached_barrier = True
                    self.state = "AT_BARRIER"
                elif self.state == "FALLING_PHASE_2":
                    self.reached_final = True
                    self.state = "FINISHED"
            return

        step = (self.speed * dt) / distance
        self.x += dx * step
        self.y += dy * step

    def draw(self, surface: pygame.Surface, colors: dict[str, tuple[int, int, int]], font: pygame.font.Font) -> None:
        if self.abandoned:
            color = colors["ball_abandoned"]
        elif self.reached_final:
            color = colors["ball_finished"]
        elif self.selected:
            color = colors["ball_selected"]
        else:
            color = colors["ball"]

        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, (255, 248, 229), (int(self.x), int(self.y)), self.radius, width=2)

        if self.state == "AT_BARRIER":
            label = font.render(str(self.id + 1), True, (18, 24, 28))
            surface.blit(label, label.get_rect(center=(int(self.x), int(self.y))))

        if self.abandoned:
            pygame.draw.line(surface, (255, 232, 232), (self.x - 10, self.y - 10), (self.x + 10, self.y + 10), width=3)
            pygame.draw.line(surface, (255, 232, 232), (self.x + 10, self.y - 10), (self.x - 10, self.y + 10), width=3)
