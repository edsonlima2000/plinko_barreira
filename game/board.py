from __future__ import annotations

import pygame

import settings
from game.slot import Slot


class Board:
    def __init__(self) -> None:
        self.rect = pygame.Rect(settings.BOARD_X, settings.BOARD_Y, settings.BOARD_WIDTH, settings.BOARD_HEIGHT)
        self.row_y_positions = self._build_row_positions()
        self.phase_one_rows, self.phase_two_rows = self._split_rows_by_barrier()
        self.pins = self._build_pins()
        self.slots = self._build_slots()

    def _build_row_positions(self) -> list[float]:
        top = self.rect.y + 56
        bottom = settings.SLOT_TOP - 30
        step = (bottom - top) / (settings.PIN_ROWS - 1)
        return [top + (step * i) for i in range(settings.PIN_ROWS)]

    def _split_rows_by_barrier(self) -> tuple[list[float], list[float]]:
        phase_one = [y for y in self.row_y_positions if y < settings.BARRIER_Y - 18]
        phase_two = [y for y in self.row_y_positions if settings.BARRIER_Y + 18 < y < settings.SLOT_TOP - 18]

        if not phase_one:
            phase_one = self.row_y_positions[: max(1, len(self.row_y_positions) // 2)]
        if not phase_two:
            phase_two = self.row_y_positions[max(1, len(self.row_y_positions) // 2) :]

        return phase_one, phase_two

    def _build_pins(self) -> list[tuple[int, int]]:
        pins: list[tuple[int, int]] = []
        left = self.rect.x + 70
        right = self.rect.right - 70
        width = right - left
        top_count = max(1, settings.PIN_BASE_COLUMNS - (settings.PIN_ROWS - 1))
        base_gap = width / max(settings.PIN_BASE_COLUMNS - 1, 1)

        for row, y in enumerate(self.row_y_positions):
            cols = min(settings.PIN_BASE_COLUMNS, top_count + row)
            row_width = base_gap * max(cols - 1, 0)
            offset = (width - row_width) / 2
            for col in range(cols):
                pins.append((int(left + offset + col * base_gap), int(y)))
        return pins

    def _build_slots(self) -> list[Slot]:
        slots: list[Slot] = []
        slot_width = self.rect.width // settings.SLOT_COUNT
        for idx, multiplier in enumerate(settings.SLOT_MULTIPLIERS):
            rect = pygame.Rect(
                self.rect.x + idx * slot_width,
                settings.SLOT_TOP,
                slot_width,
                settings.SLOT_HEIGHT,
            )
            slots.append(Slot(idx, multiplier, rect))
        slots[-1].rect.width = self.rect.right - slots[-1].rect.x
        return slots

    def get_spawn_point(self) -> tuple[float, float]:
        return float(self.rect.centerx), float(self.rect.y + 30)

    def clamp_ball_position(self, x: float, radius: int) -> float:
        min_x = self.rect.left + radius + 8
        max_x = self.rect.right - radius - 8
        return max(min_x, min(max_x, x))

    def apply_pin_collisions(self, ball) -> None:
        if ball.state not in {"FALLING_PHASE_1", "FALLING_PHASE_2"}:
            return

        min_distance = max(ball.radius * 0.62, ball.radius + settings.PIN_RADIUS - 7)
        min_distance_sq = min_distance * min_distance
        nearest_pin: tuple[int, int] | None = None
        nearest_distance_sq: float | None = None

        for pin_x, pin_y in self.pins:
            if ball.last_pin_collision == (pin_x, pin_y) and ball.pin_collision_cooldown > 0:
                continue
            dx = ball.x - pin_x
            dy = ball.y - pin_y
            distance_sq = (dx * dx) + (dy * dy)
            if distance_sq >= min_distance_sq:
                continue
            if nearest_distance_sq is None or distance_sq < nearest_distance_sq:
                nearest_pin = (pin_x, pin_y)
                nearest_distance_sq = distance_sq

        if nearest_pin is None or nearest_distance_sq is None:
            return

        pin_x, pin_y = nearest_pin
        dx = ball.x - pin_x
        dy = ball.y - pin_y
        if nearest_distance_sq == 0:
            dx = -1.0 if ball.x >= self.rect.centerx else 1.0
            dy = -0.2
            nearest_distance_sq = (dx * dx) + (dy * dy)

        distance = nearest_distance_sq ** 0.5
        overlap = min_distance - distance
        normal_x = dx / distance
        ball.x += normal_x * overlap * 0.75
        ball.y += 1.2
        ball.last_pin_collision = nearest_pin
        ball.pin_collision_cooldown = 0.08

    def get_barrier_positions(self, count: int) -> list[float]:
        start = self.rect.x + 130
        end = self.rect.right - 130
        if count == 1:
            return [self.rect.centerx]
        return [start + ((end - start) * idx / (count - 1)) for idx in range(count)]

    def get_random_path_targets(self, rng, count: int) -> list[list[tuple[float, float]]]:
        barrier_positions = self.get_barrier_positions(count)
        paths: list[list[tuple[float, float]]] = []
        min_x = self.rect.left + 30
        max_x = self.rect.right - 30

        for barrier_x in barrier_positions:
            x = float(self.rect.centerx + rng.uniform(-20, 20))
            points: list[tuple[float, float]] = []
            for row_y in self.phase_one_rows:
                x += rng.choice((-34, -24, -12, 12, 24, 34))
                x = max(min_x, min(max_x, x))
                points.append((x, row_y))
            points.append((barrier_x, settings.BARRIER_Y - settings.BALL_RADIUS - 2))
            paths.append(points)
        return paths

    def get_phase_two_targets(self, start_x: float, slot_index: int, rng) -> list[tuple[float, float]]:
        slot = self.slots[slot_index]
        min_x = self.rect.left + 30
        max_x = self.rect.right - 30
        x = start_x
        points: list[tuple[float, float]] = [(x, settings.BARRIER_Y + settings.BALL_RADIUS + 14)]

        for row_y in self.phase_two_rows:
            drift = rng.choice((-34, -24, -12, 12, 24, 34))
            target_bias = (slot.center_x - x) * 0.22
            x = max(min_x, min(max_x, x + drift + target_bias))
            points.append((x, row_y))

        points.append((slot.center_x, slot.rect.y - settings.BALL_RADIUS - 10))
        points.append((slot.center_x, slot.rect.y + 14))
        return points

    def resolve_slot(self, x: float) -> Slot:
        for slot in self.slots:
            if slot.rect.left <= x < slot.rect.right:
                return slot
        return self.slots[-1]

    def draw(self, surface: pygame.Surface, fonts: dict[str, pygame.font.Font], colors: dict[str, tuple[int, int, int]]) -> None:
        pygame.draw.rect(surface, colors["board_bg"], self.rect, border_radius=28)
        pygame.draw.rect(surface, colors["board_border"], self.rect, width=4, border_radius=28)

        wall_top = self.rect.top + 16
        wall_bottom = self.rect.bottom - 16
        left_wall_x = self.rect.left + 10
        right_wall_x = self.rect.right - 10
        pygame.draw.line(surface, colors["board_border"], (left_wall_x, wall_top), (left_wall_x, wall_bottom), width=6)
        pygame.draw.line(surface, colors["board_border"], (right_wall_x, wall_top), (right_wall_x, wall_bottom), width=6)

        for x, y in self.pins:
            pygame.draw.circle(surface, colors["pin"], (x, y), settings.PIN_RADIUS)

        for slot in self.slots:
            slot.draw(surface, fonts["small"], colors)
