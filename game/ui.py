from __future__ import annotations

import pygame

import settings
from utils.helpers import Button


class GameUI:
    def __init__(self, fonts: dict[str, pygame.font.Font]) -> None:
        self.fonts = fonts
        self.minus_button = Button("-", pygame.Rect(280, 610, 56, 46))
        self.plus_button = Button("+", pygame.Rect(430, 610, 56, 46))
        self.start_button = Button("Iniciar rodada", pygame.Rect(520, 605, 180, 56))
        self.confirm_button = Button("Confirmar", pygame.Rect(520, 605, 150, 56))
        self.reset_button = Button("Nova rodada", pygame.Rect(520, 605, 170, 56))

    def draw_header(self, surface: pygame.Surface, state: str, bet_count: int, kept_count: int, total_score: int, colors: dict[str, tuple[int, int, int]]) -> None:
        title = self.fonts["title"].render(settings.TITLE, True, colors["text"])
        state_label = self.fonts["body"].render(f"Fase: {state}", True, colors["text"])
        bet_label = self.fonts["body"].render(f"Bolas apostadas: {bet_count}", True, colors["text"])
        kept_label = self.fonts["body"].render(f"Bolas mantidas: {kept_count}", True, colors["text"])
        score_label = self.fonts["body"].render(f"Premio da rodada: {total_score}", True, colors["text"])
        hint = self.fonts["small"].render(settings.STATUS_TEXT[state], True, colors["muted"])

        surface.blit(title, (42, 26))
        surface.blit(state_label, (610, 22))
        surface.blit(bet_label, (610, 45))
        surface.blit(kept_label, (780, 22))
        surface.blit(score_label, (780, 45))
        surface.blit(hint, (44, 62))

    def draw_footer(self, surface: pygame.Surface, state: str, bet_count: int, hovered_pos: tuple[int, int], colors: dict[str, tuple[int, int, int]]) -> None:
        instruction = ""
        if state == "SELECT_BET":
            instruction = "Defina quantas bolas vao descer nesta rodada."
        elif state == "BARRIER_DECISION":
            instruction = "Selecione as bolas que continuam depois da barreira."
        elif state == "ROUND_RESULT":
            instruction = "Clique para limpar a tela e iniciar uma nova rodada."
        else:
            instruction = "Acompanhe a animacao e o resultado da rodada."

        text = self.fonts["body"].render(instruction, True, colors["text"])
        surface.blit(text, (42, 610))

        if state == "SELECT_BET":
            label = self.fonts["body"].render(str(bet_count), True, colors["text"])
            surface.blit(label, label.get_rect(center=(383, 633)))
            self.minus_button.enabled = bet_count > 1
            self.plus_button.enabled = bet_count < settings.MAX_BALLS
            self.start_button.enabled = 1 <= bet_count <= settings.MAX_BALLS
            self.minus_button.draw(surface, self.fonts["body"], colors, self.minus_button.rect.collidepoint(hovered_pos))
            self.plus_button.draw(surface, self.fonts["body"], colors, self.plus_button.rect.collidepoint(hovered_pos))
            self.start_button.draw(surface, self.fonts["body"], colors, self.start_button.rect.collidepoint(hovered_pos))
        elif state == "BARRIER_DECISION":
            self.confirm_button.enabled = True
            self.confirm_button.draw(surface, self.fonts["body"], colors, self.confirm_button.rect.collidepoint(hovered_pos))
        elif state == "ROUND_RESULT":
            self.reset_button.enabled = True
            self.reset_button.draw(surface, self.fonts["body"], colors, self.reset_button.rect.collidepoint(hovered_pos))

    def draw_result_summary(self, surface: pygame.Surface, total_score: int, values: list[int], colors: dict[str, tuple[int, int, int]]) -> None:
        summary_rect = pygame.Rect(42, 560, 380, 94)
        pygame.draw.rect(surface, colors["panel"], summary_rect, border_radius=20)
        pygame.draw.rect(surface, colors["board_border"], summary_rect, width=2, border_radius=20)
        total = self.fonts["body"].render(f"Total: {total_score}", True, colors["text"])
        details = self.fonts["small"].render(f"Valores das bolas mantidas: {values or [0]}", True, colors["muted"])
        surface.blit(total, (64, 582))
        surface.blit(details, (64, 613))
