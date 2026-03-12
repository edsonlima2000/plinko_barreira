from __future__ import annotations

import pygame

import settings
from game.barrier import Barrier
from game.board import Board
from game.round_manager import RoundManager
from game.state_machine import BARRIER_DECISION, DROP_PHASE_1, DROP_PHASE_2, ROUND_RESULT, SELECT_BET
from game.ui import GameUI


class PlinkoGame:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.fonts = {
            "title": pygame.font.SysFont("verdana", 30, bold=True),
            "body": pygame.font.SysFont("verdana", 22),
            "small": pygame.font.SysFont("verdana", 18),
        }

        self.board = Board()
        self.barrier = Barrier(settings.BARRIER_Y, self.board.rect)
        self.round_manager = RoundManager(self.board)
        self.ui = GameUI(self.fonts)

        self.state = SELECT_BET
        self.bet_count = settings.DEFAULT_BET
        self.result_processed = False

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(settings.FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_click(event.pos)

    def handle_click(self, pos: tuple[int, int]) -> None:
        if self.state == SELECT_BET:
            if self.ui.minus_button.contains(pos):
                self.bet_count = max(1, self.bet_count - 1)
            elif self.ui.plus_button.contains(pos):
                self.bet_count = min(settings.MAX_BALLS, self.bet_count + 1)
            elif self.ui.start_button.contains(pos):
                self.round_manager.start_round(self.bet_count)
                self.result_processed = False
                self.state = DROP_PHASE_1
        elif self.state == BARRIER_DECISION:
            if self.ui.confirm_button.contains(pos):
                self.round_manager.confirm_selection()
                if self.round_manager.result.kept_count == 0:
                    self.round_manager.calculate_result()
                    self.result_processed = True
                    self.state = ROUND_RESULT
                else:
                    self.state = DROP_PHASE_2
                return

            for ball in self.round_manager.balls:
                if ball.contains(pos):
                    ball.toggle_selected()
                    break
        elif self.state == ROUND_RESULT and self.ui.reset_button.contains(pos):
            self.round_manager.reset()
            self.result_processed = False
            self.state = SELECT_BET

    def update(self, dt: float) -> None:
        if self.state in {DROP_PHASE_1, DROP_PHASE_2}:
            self.round_manager.update(dt)

        if self.state == DROP_PHASE_1 and self.round_manager.all_at_barrier():
            self.state = BARRIER_DECISION

        if self.state == DROP_PHASE_2 and self.round_manager.finished() and not self.result_processed:
            self.round_manager.calculate_result()
            self.result_processed = True
            self.state = ROUND_RESULT

    def draw(self) -> None:
        hovered_pos = pygame.mouse.get_pos()
        self.screen.fill(settings.UI["bg"])

        top_rect = pygame.Rect(20, 16, settings.WINDOW_WIDTH - 40, settings.TOP_PANEL_HEIGHT)
        bottom_rect = pygame.Rect(20, settings.WINDOW_HEIGHT - settings.BOTTOM_PANEL_HEIGHT - 16, settings.WINDOW_WIDTH - 40, settings.BOTTOM_PANEL_HEIGHT)
        pygame.draw.rect(self.screen, settings.UI["panel"], top_rect, border_radius=24)
        pygame.draw.rect(self.screen, settings.UI["panel"], bottom_rect, border_radius=24)

        self.ui.draw_header(
            self.screen,
            self.state,
            self.round_manager.result.bet_count or self.bet_count,
            self.round_manager.result.kept_count,
            self.round_manager.result.total_score,
            self.round_manager.balance,
            settings.UI,
        )
        self.ui.draw_result_summary(
            self.screen,
            self.round_manager.result.total_score,
            self.round_manager.result.slot_multipliers or [],
            settings.UI,
            98,
        )

        self.board.draw(self.screen, self.fonts, settings.UI)
        self.barrier.draw(self.screen, settings.UI["barrier"])

        for ball in self.round_manager.balls:
            ball.draw(self.screen, settings.UI, self.fonts["small"])

        self.ui.draw_footer(self.screen, self.state, self.bet_count, hovered_pos, settings.UI)

        pygame.display.flip()
