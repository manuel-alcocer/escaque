"""The answer checker and the failure bookkeeping.

These cover the product's central rule: an exercise that is not solved correctly
is recorded as failed, and it stays flagged until it is solved cleanly.
"""

import pytest

from apps.exercises.models import Attempt, ExerciseProgress
from apps.exercises.services import FAILED, IN_PROGRESS, SOLVED, InvalidMove, evaluate, register_attempt


def test_correct_single_move_solves(single_move_exercise):
    result = evaluate(single_move_exercise, ["b5a4"])
    assert result.status == SOLVED
    assert result.moves_correct == 1


def test_wrong_but_legal_move_fails_and_reports_the_answer(single_move_exercise):
    result = evaluate(single_move_exercise, ["d2d4"])
    assert result.status == FAILED
    assert result.expected_san == "Ba4"
    assert result.played_san == "d4"


def test_accepted_alternative_also_solves(single_move_exercise):
    result = evaluate(single_move_exercise, ["b5c6"])
    assert result.status == SOLVED


def test_illegal_move_is_rejected_rather_than_failed(single_move_exercise):
    """An impossible move is a bad request, not a wrong answer."""
    with pytest.raises(InvalidMove):
        evaluate(single_move_exercise, ["a1a8"])


def test_san_is_accepted_as_well_as_uci(single_move_exercise):
    assert evaluate(single_move_exercise, ["Ba4"]).status == SOLVED


def test_partial_line_reports_the_opponent_reply(two_move_exercise):
    result = evaluate(two_move_exercise, ["b5a4"])
    assert result.status == IN_PROGRESS
    assert result.reply_san == "Nf6"
    assert result.moves_expected == 2


def test_full_line_solves(two_move_exercise):
    assert evaluate(two_move_exercise, ["b5a4", "e1g1"]).status == SOLVED


def test_second_move_wrong_fails_after_a_correct_first(two_move_exercise):
    result = evaluate(two_move_exercise, ["b5a4", "d2d4"])
    assert result.status == FAILED
    assert result.moves_correct == 1


@pytest.mark.django_db
def test_failure_is_recorded_and_flags_the_exercise(user, single_move_exercise):
    evaluation = evaluate(single_move_exercise, ["d2d4"])
    attempt, progress = register_attempt(
        user=user,
        exercise=single_move_exercise,
        evaluation=evaluation,
        moves_played=["d2d4"],
        duration_ms=5000,
    )

    assert attempt.status == Attempt.Status.FAILED
    assert progress.status == ExerciseProgress.Status.FAILED
    assert progress.needs_review is True
    assert progress.failed_count == 1
    assert progress.attempts_count == 1


@pytest.mark.django_db
def test_solving_after_a_failure_clears_the_flag(user, single_move_exercise):
    register_attempt(
        user=user,
        exercise=single_move_exercise,
        evaluation=evaluate(single_move_exercise, ["d2d4"]),
        moves_played=["d2d4"],
    )
    _, progress = register_attempt(
        user=user,
        exercise=single_move_exercise,
        evaluation=evaluate(single_move_exercise, ["b5a4"]),
        moves_played=["b5a4"],
        duration_ms=3000,
    )

    assert progress.needs_review is False
    assert progress.status == ExerciseProgress.Status.SOLVED
    assert progress.attempts_count == 2
    assert progress.solved_count == 1
    assert progress.failed_count == 1
    # The failure is not erased; it stays in the history.
    assert user.attempts.filter(status=Attempt.Status.FAILED).count() == 1


@pytest.mark.django_db
def test_best_duration_only_improves(user, single_move_exercise):
    for duration in (9000, 4000, 7000):
        register_attempt(
            user=user,
            exercise=single_move_exercise,
            evaluation=evaluate(single_move_exercise, ["b5a4"]),
            moves_played=["b5a4"],
            duration_ms=duration,
        )
    progress = ExerciseProgress.objects.get(user=user, exercise=single_move_exercise)
    assert progress.best_duration_ms == 4000
