"""Answer checking and progress bookkeeping.

The rule the product asks for: an exercise that is not solved correctly is recorded
as failed. `register_attempt` is the only place that writes that outcome, so the
counters cannot disagree with the attempt log.
"""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, field

import chess
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from .models import Attempt, Exercise, ExerciseProgress

logger = logging.getLogger(__name__)

IN_PROGRESS = "in_progress"
SOLVED = "solved"
FAILED = "failed"


class InvalidMove(ValueError):
    """The submitted move is not legal in the position it was played from."""


@dataclass
class Evaluation:
    """Outcome of replaying the user's moves against the stored line."""

    status: str
    ply: int = 0
    moves_expected: int = 0
    moves_correct: int = 0
    fen: str = ""
    # Opponent reply to animate once the user's move is accepted.
    reply_uci: str = ""
    reply_san: str = ""
    # Populated only when the attempt is over.
    expected_uci: str = ""
    expected_san: str = ""
    played_uci: str = ""
    played_san: str = ""
    truncated: bool = False
    line_san: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return asdict(self)


def _san_for(board: chess.Board, uci: str) -> str:
    try:
        return board.san(chess.Move.from_uci(uci))
    except (ValueError, AssertionError):
        return uci


def evaluate(exercise: Exercise, user_moves: list[str]) -> Evaluation:
    """Replay `user_moves` against the exercise line.

    Returns IN_PROGRESS while the user still owes moves, SOLVED once the whole line
    is played, FAILED on the first move that leaves the line.
    """

    board = chess.Board(exercise.fen)
    solution = exercise.solution or []
    total_user_plies = sum(1 for ply in solution if ply.get("by") == "user")
    consumed = 0
    correct = 0

    for index, ply in enumerate(solution):
        if ply.get("by") != "user":
            uci = ply.get("uci", "")
            move = _legal_move(board, uci, context="stored opponent reply")
            board.push(move)
            continue

        if consumed >= len(user_moves):
            # Waiting for the user. If the previous ply was an opponent reply the
            # caller has already been told about it.
            return Evaluation(
                status=IN_PROGRESS,
                ply=index,
                moves_expected=total_user_plies,
                moves_correct=correct,
                fen=board.fen(),
            )

        submitted = _normalise(board, user_moves[consumed])
        consumed += 1
        expected = ply.get("uci", "")
        accepted = {expected, *ply.get("also", [])}

        if submitted not in accepted:
            return Evaluation(
                status=FAILED,
                ply=index,
                moves_expected=total_user_plies,
                moves_correct=correct,
                fen=board.fen(),
                expected_uci=expected,
                expected_san=_san_for(board, expected),
                played_uci=submitted,
                played_san=_san_for(board, submitted),
                line_san=_full_line_san(exercise),
            )

        correct += 1
        board.push(_legal_move(board, submitted, context="accepted user move"))

        if submitted != expected:
            # An accepted alternative can transpose out of the stored line, so the
            # exercise ends here rather than forcing a reply that may be illegal.
            return Evaluation(
                status=SOLVED,
                ply=index + 1,
                moves_expected=total_user_plies,
                moves_correct=correct,
                fen=board.fen(),
                truncated=True,
                line_san=_full_line_san(exercise),
            )

        reply = _next_opponent_reply(board, solution, index + 1)
        if reply and consumed >= len(user_moves):
            return Evaluation(
                status=IN_PROGRESS,
                ply=index + 1,
                moves_expected=total_user_plies,
                moves_correct=correct,
                fen=board.fen(),
                reply_uci=reply[0],
                reply_san=reply[1],
            )

    return Evaluation(
        status=SOLVED,
        ply=len(solution),
        moves_expected=total_user_plies,
        moves_correct=correct,
        fen=board.fen(),
        line_san=_full_line_san(exercise),
    )


def _next_opponent_reply(board: chess.Board, solution: list[dict], index: int):
    if index >= len(solution):
        return None
    ply = solution[index]
    if ply.get("by") == "user":
        return None
    uci = ply.get("uci", "")
    return uci, _san_for(board, uci)


def _normalise(board: chess.Board, raw: str) -> str:
    """Accept UCI or SAN from the client and return canonical UCI."""

    candidate = (raw or "").strip()
    if not candidate:
        raise InvalidMove("No move was submitted.")

    try:
        move = chess.Move.from_uci(candidate)
    except ValueError:
        try:
            move = board.parse_san(candidate)
        except (ValueError, AssertionError) as exc:
            raise InvalidMove(f"'{raw}' is not a move this position allows.") from exc

    if move not in board.legal_moves:
        # A queen promotion sent without the suffix is a common client slip.
        promoted = chess.Move(move.from_square, move.to_square, promotion=chess.QUEEN)
        if promoted in board.legal_moves:
            move = promoted
        else:
            raise InvalidMove(f"'{raw}' is not a move this position allows.")

    return move.uci()


def _legal_move(board: chess.Board, uci: str, *, context: str) -> chess.Move:
    try:
        move = chess.Move.from_uci(uci)
    except ValueError as exc:
        raise InvalidMove(f"Corrupt {context}: '{uci}'.") from exc
    if move not in board.legal_moves:
        raise InvalidMove(f"Corrupt {context}: '{uci}' is illegal in {board.fen()}.")
    return move


def _full_line_san(exercise: Exercise) -> list[str]:
    board = chess.Board(exercise.fen)
    line = []
    for ply in exercise.solution or []:
        uci = ply.get("uci", "")
        try:
            move = chess.Move.from_uci(uci)
            line.append(board.san(move))
            board.push(move)
        except (ValueError, AssertionError):
            break
    return line


@transaction.atomic
def register_attempt(
    *,
    user,
    exercise: Exercise,
    evaluation: Evaluation,
    moves_played: list[str],
    duration_ms: int = 0,
    hints_used: int = 0,
    gave_up: bool = False,
) -> tuple[Attempt, ExerciseProgress]:
    """Persist a finished attempt and roll the user's counters forward."""

    status = Attempt.Status.SOLVED if evaluation.status == SOLVED else Attempt.Status.FAILED
    now = timezone.now()

    attempt = Attempt.objects.create(
        user=user,
        exercise=exercise,
        status=status,
        moves_played=moves_played,
        failed_at_ply=evaluation.ply if status == Attempt.Status.FAILED else None,
        expected_move=evaluation.expected_uci,
        played_move=evaluation.played_uci,
        hints_used=hints_used,
        gave_up=gave_up,
        duration_ms=max(0, duration_ms),
    )

    progress, _ = ExerciseProgress.objects.select_for_update().get_or_create(
        user=user, exercise=exercise
    )
    progress.attempts_count = F("attempts_count") + 1
    progress.last_attempt_at = now

    if status == Attempt.Status.SOLVED:
        progress.solved_count = F("solved_count") + 1
        progress.status = ExerciseProgress.Status.SOLVED
        progress.needs_review = False
        if progress.first_solved_at is None:
            progress.first_solved_at = now
        if duration_ms and (
            progress.best_duration_ms is None or duration_ms < progress.best_duration_ms
        ):
            progress.best_duration_ms = duration_ms
    else:
        progress.failed_count = F("failed_count") + 1
        progress.status = ExerciseProgress.Status.FAILED
        progress.needs_review = True

    progress.save()
    progress.refresh_from_db()
    return attempt, progress
