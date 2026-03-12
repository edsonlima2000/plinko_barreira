from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass
class Button:
    label: str
    rect: pygame.Rect
    enabled: bool = True

    def draw(self, surface: pygame.Surface, font: pygame.font.Font, colors: dict[str, tuple[int, int, int]], hovered: bool) -> None:
        if not self.enabled:
            color = colors["button_disabled"]
        elif hovered:
            color = colors["button_hover"]
        else:
            color = colors["button"]

        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        text = font.render(self.label, True, colors["button_text"])
        surface.blit(text, text.get_rect(center=self.rect.center))

    def contains(self, pos: tuple[int, int]) -> bool:
        return self.enabled and self.rect.collidepoint(pos)
