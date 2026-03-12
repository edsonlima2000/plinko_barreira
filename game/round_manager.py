from __future__ import annotations

from dataclasses import dataclass
import random

import settings
from game.ball import Ball
from game.board import Board


@dataclass
class RoundResult:
    bet_count: int = 0
    kept_count: int = 0
    abandoned_count: int = 0
    slot_values: list[int] | None = None
    total_score: int = 0


class RoundManager:
    def __init__(self, board: Board) -> None:
        self.board = board
        self.rng = random.Random()
        self.bet_count = settings.DEFAULT_BET
        self.balls: list[Ball] = []
        self.result = RoundResult(slot_values=[])
        self._phase_two_slot_order: list[int] = []

    def reset(self) -> None:
        self.balls = []
        self.result = RoundResult(slot_values=[])
        self._phase_two_slot_order = []

    def start_round(self, bet_count: int) -> None:
        self.reset()
        self.bet_count = bet_count
        spawn_x, spawn_y = self.board.get_spawn_point()
        paths = self.board.get_random_path_targets(self.rng, bet_count)
        for idx in range(bet_count):
            ball = Ball(id=idx, x=spawn_x, y=spawn_y, release_delay=idx * settings.BALL_RELEASE_DELAY)
            ball.set_path(paths[idx], "FALLING_PHASE_1")
            self.balls.append(ball)
        self.result.bet_count = bet_count

    def all_at_barrier(self) -> bool:
        return bool(self.balls) and all(ball.state == "AT_BARRIER" for ball in self.balls)

    def confirm_selection(self) -> None:
        kept = [ball for ball in self.balls if ball.selected and not ball.abandoned]
        abandoned = [ball for ball in self.balls if ball not in kept]
        for ball in abandoned:
            ball.abandon()

        self._phase_two_slot_order = self._build_slot_order(len(kept))
        for idx, ball in enumerate(kept):
            slot_index = self._phase_two_slot_order[idx]
            ball.final_slot = slot_index
            ball.append_path(self.board.get_phase_two_targets(ball.x, slot_index), "FALLING_PHASE_2")

        self.result.kept_count = len(kept)
        self.result.abandoned_count = len(abandoned)

    def _build_slot_order(self, count: int) -> list[int]:
        preferred = [3, 2, 4, 1, 5, 6, 0]
        self.rng.shuffle(preferred)
        return preferred[:count]

    def update(self, dt: float) -> None:
        for ball in self.balls:
            ball.update(dt)

    def finished(self) -> bool:
        if not self.balls:
            return False
        return all(ball.state in {"FINISHED", "ABANDONED"} for ball in self.balls)

    def calculate_result(self) -> RoundResult:
        values: list[int] = []
        for ball in self.balls:
            if ball.final_slot is None or not ball.reached_final:
                continue
            slot = self.board.slots[ball.final_slot]
            values.append(slot.value)
        self.result.slot_values = values
        self.result.total_score = sum(values)
        return self.result

    def kept_count(self) -> int:
        return len([ball for ball in self.balls if ball.selected and not ball.abandoned])
