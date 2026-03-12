from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass
class Slot:
    index: int
    value: int
    rect: pygame.Rect

    @property
    def center_x(self) -> int:
        return self.rect.centerx

    def draw(self, surface: pygame.Surface, font: pygame.font.Font, colors: dict[str, tuple[int, int, int]]) -> None:
        pygame.draw.rect(surface, colors["slot_fill"], self.rect)
        pygame.draw.rect(surface, colors["slot_line"], self.rect, width=2)

        index_text = font.render(str(self.index + 1), True, colors["button_text"])
        value_text = font.render(str(self.value), True, colors["button_text"])
        surface.blit(index_text, index_text.get_rect(center=(self.rect.centerx, self.rect.y + 22)))
        surface.blit(value_text, value_text.get_rect(center=(self.rect.centerx, self.rect.y + 54)))
