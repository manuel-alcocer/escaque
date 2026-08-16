"""Exercises and the record of how every user does on them.

An exercise is a position plus a scripted line. `solution` is a list of plies in
order, each one either the user's move or the opponent's reply:

    [
      {"uci": "f1b5", "san": "Bb5", "by": "user", "also": ["f1c4"]},
      {"uci": "a7a6", "san": "a6",  "by": "opponent"},
      ...
    ]

`also` holds moves that are accepted as equally correct. Answers are always
checked on the server: the browser never learns the solution until the attempt is
over, so the line cannot be read out of the network tab.
"""

from django.conf import settings
from django.db import models
from django.db.models import F, Q


class Exercise(models.Model):
    class Kind(models.TextChoices):
        THEORY = "theory", "Play the theoretical move"
        TACTIC = "tactic", "Win material or mate"
        PLAN = "plan", "Find the right plan"
        TRAP = "trap", "Punish the mistake"
        RECALL = "recall", "Recall the move order"

    class Difficulty(models.IntegerChoices):
        INTRODUCTORY = 1, "Introductory"
        EASY = 2, "Easy"
        MEDIUM = 3, "Medium"
        HARD = 4, "Hard"
        EXPERT = 5, "Expert"

    variation = models.ForeignKey(
        "curriculum.Variation", related_name="exercises", on_delete=models.CASCADE
    )
    reference = models.CharField(
        max_length=120,
        unique=True,
        help_text="Stable identifier so re-seeding updates instead of duplicating.",
    )
    kind = models.CharField(max_length=10, choices=Kind.choices, default=Kind.THEORY)
    difficulty = models.PositiveSmallIntegerField(
        choices=Difficulty.choices, default=Difficulty.EASY
    )
    prompt = models.CharField(max_length=240, help_text="What the user has to do.")
    explanation = models.TextField(blank=True, help_text="Shown once the attempt is finished.")
    fen = models.CharField(max_length=100, help_text="Position the user starts from.")
    orientation = models.CharField(
        max_length=5, choices=[("white", "White"), ("black", "Black")], default="white"
    )
    side_to_move = models.CharField(
        max_length=5, choices=[("white", "White"), ("black", "Black")], default="white"
    )
    setup_moves_san = models.JSONField(
        default=list, blank=True, help_text="Moves that led to the position, for context."
    )
    solution = models.JSONField(default=list)
    hint = models.CharField(max_length=240, blank=True)
    themes = models.JSONField(default=list, blank=True, help_text="e.g. ['fork', 'pin'].")
    position = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("variation__position", "difficulty", "position", "id")
        indexes = [
            models.Index(fields=["kind", "difficulty"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.reference} — {self.prompt[:50]}"

    @property
    def user_plies(self) -> list[dict]:
        return [ply for ply in self.solution if ply.get("by") == "user"]

    @property
    def required_moves(self) -> int:
        return len(self.user_plies)


class Attempt(models.Model):
    """One completed run at an exercise. Never updated after it is written."""

    class Status(models.TextChoices):
        SOLVED = "solved", "Solved"
        FAILED = "failed", "Failed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="attempts", on_delete=models.CASCADE
    )
    exercise = models.ForeignKey(Exercise, related_name="attempts", on_delete=models.CASCADE)
    status = models.CharField(max_length=6, choices=Status.choices)
    moves_played = models.JSONField(default=list, help_text="UCI moves the user actually played.")
    failed_at_ply = models.PositiveSmallIntegerField(
        null=True, blank=True, help_text="Index in `solution` where the line broke."
    )
    expected_move = models.CharField(max_length=10, blank=True)
    played_move = models.CharField(max_length=10, blank=True)
    hints_used = models.PositiveSmallIntegerField(default=0)
    gave_up = models.BooleanField(default=False)
    duration_ms = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["user", "exercise"]),
        ]

    def __str__(self):
        return f"{self.user} · {self.exercise.reference} · {self.status}"


class ExerciseProgress(models.Model):
    """Running totals per user and exercise, so the lists do not aggregate on every read."""

    class Status(models.TextChoices):
        UNSEEN = "unseen", "Not attempted"
        SOLVED = "solved", "Solved"
        FAILED = "failed", "Failed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="progress", on_delete=models.CASCADE
    )
    exercise = models.ForeignKey(
        Exercise, related_name="progress", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=6, choices=Status.choices, default=Status.UNSEEN)
    attempts_count = models.PositiveIntegerField(default=0)
    solved_count = models.PositiveIntegerField(default=0)
    failed_count = models.PositiveIntegerField(default=0)
    best_duration_ms = models.PositiveIntegerField(null=True, blank=True)
    first_solved_at = models.DateTimeField(null=True, blank=True)
    last_attempt_at = models.DateTimeField(null=True, blank=True)
    # Once failed, an exercise stays flagged until it is solved cleanly again.
    needs_review = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("user", "exercise"), name="unique_user_exercise"),
            models.CheckConstraint(
                condition=Q(solved_count__lte=F("attempts_count")),
                name="solved_not_greater_than_attempts",
            ),
        ]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["user", "needs_review"]),
        ]

    def __str__(self):
        return f"{self.user} · {self.exercise.reference} · {self.status}"

    @property
    def accuracy(self) -> float | None:
        if not self.attempts_count:
            return None
        return round(self.solved_count / self.attempts_count, 3)
