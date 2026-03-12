from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass
class Slot:
    index: int
    multiplier: float
    rect: pygame.Rect

    @property
    def center_x(self) -> int:
        return self.rect.centerx

    def draw(self, surface: pygame.Surface, font: pygame.font.Font, colors: dict[str, tuple[int, int, int]]) -> None:
        pygame.draw.rect(surface, colors["slot_fill"], self.rect)
        pygame.draw.rect(surface, colors["slot_line"], self.rect, width=2)

        multiplier_text = font.render(self._format_multiplier(), True, colors["button_text"])
        surface.blit(multiplier_text, multiplier_text.get_rect(center=self.rect.center))

    def _format_multiplier(self) -> str:
        if self.multiplier.is_integer():
            return f"{int(self.multiplier)}x"
        return f"{self.multiplier:.1f}x"
