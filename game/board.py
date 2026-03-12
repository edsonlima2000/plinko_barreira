from __future__ import annotations

import pygame

import settings
from game.slot import Slot


class Board:
    def __init__(self) -> None:
        self.rect = pygame.Rect(settings.BOARD_X, settings.BOARD_Y, settings.BOARD_WIDTH, settings.BOARD_HEIGHT)
        self.row_y_positions = self._build_row_positions()
        self.pins = self._build_pins()
        self.slots = self._build_slots()

    def _build_row_positions(self) -> list[float]:
        top = self.rect.y + 70
        bottom = settings.BARRIER_Y - 22
        step = (bottom - top) / (settings.PIN_ROWS - 1)
        return [top + (step * i) for i in range(settings.PIN_ROWS)]

    def _build_pins(self) -> list[tuple[int, int]]:
        pins: list[tuple[int, int]] = []
        left = self.rect.x + 70
        right = self.rect.right - 70
        width = right - left
        for row, y in enumerate(self.row_y_positions):
            cols = settings.PIN_COLUMNS if row % 2 == 0 else settings.PIN_COLUMNS - 1
            gap = width / max(cols - 1, 1)
            offset = 0 if row % 2 == 0 else gap / 2
            for col in range(cols):
                pins.append((int(left + offset + col * gap), int(y)))
        return pins

    def _build_slots(self) -> list[Slot]:
        slots: list[Slot] = []
        slot_width = self.rect.width // settings.SLOT_COUNT
        for idx, value in enumerate(settings.SLOT_VALUES):
            rect = pygame.Rect(
                self.rect.x + idx * slot_width,
                settings.SLOT_TOP,
                slot_width,
                settings.SLOT_HEIGHT,
            )
            slots.append(Slot(idx, value, rect))
        slots[-1].rect.width = self.rect.right - slots[-1].rect.x
        return slots

    def get_spawn_point(self) -> tuple[float, float]:
        return float(self.rect.centerx), float(self.rect.y + 30)

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
            for row_y in self.row_y_positions:
                x += rng.choice((-34, -24, -12, 12, 24, 34))
                x = max(min_x, min(max_x, x))
                points.append((x, row_y))
            points.append((barrier_x, settings.BARRIER_Y - settings.BALL_RADIUS - 2))
            paths.append(points)
        return paths

    def get_phase_two_targets(self, start_x: float, slot_index: int) -> list[tuple[float, float]]:
        slot = self.slots[slot_index]
        mid_y = settings.BARRIER_Y + 92
        return [
            (start_x, settings.BARRIER_Y + 38),
            ((start_x + slot.center_x) / 2, mid_y),
            (slot.center_x, slot.rect.y - settings.BALL_RADIUS - 10),
            (slot.center_x, slot.rect.y + 14),
        ]

    def resolve_slot(self, x: float) -> Slot:
        for slot in self.slots:
            if slot.rect.left <= x < slot.rect.right:
                return slot
        return self.slots[-1]

    def draw(self, surface: pygame.Surface, fonts: dict[str, pygame.font.Font], colors: dict[str, tuple[int, int, int]]) -> None:
        pygame.draw.rect(surface, colors["board_bg"], self.rect, border_radius=28)
        pygame.draw.rect(surface, colors["board_border"], self.rect, width=4, border_radius=28)

        for x, y in self.pins:
            pygame.draw.circle(surface, colors["pin"], (x, y), settings.PIN_RADIUS)

        for slot in self.slots:
            slot.draw(surface, fonts["small"], colors)
