from __future__ import annotations

import pygame


class Barrier:
    def __init__(self, y: int, board_rect: pygame.Rect) -> None:
        self.y = y
        self.board_rect = board_rect

    def draw(self, surface: pygame.Surface, color: tuple[int, int, int]) -> None:
        left = self.board_rect.left + 16
        right = self.board_rect.right - 16
        pygame.draw.line(surface, color, (left, self.y), (right, self.y), width=6)
        pygame.draw.line(surface, (255, 217, 200), (left, self.y - 4), (right, self.y - 4), width=2)
