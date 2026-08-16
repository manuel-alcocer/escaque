from rest_framework import serializers

from .models import Attempt, Exercise, ExerciseProgress


class ExerciseSerializer(serializers.ModelSerializer):
    """Everything the board needs, and nothing that gives the answer away.

    `solution` and `hint` are deliberately absent: the hint is served by its own
    endpoint and the solution only ever arrives in the response to an attempt.
    """

    variation_name = serializers.CharField(source="variation.name", read_only=True)
    variation_slug = serializers.CharField(source="variation.slug", read_only=True)
    opening_name = serializers.CharField(source="variation.opening.name", read_only=True)
    opening_slug = serializers.CharField(source="variation.opening.slug", read_only=True)
    eco = serializers.CharField(source="variation.eco", read_only=True)
    required_moves = serializers.IntegerField(read_only=True)
    has_hint = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    attempts_count = serializers.SerializerMethodField()
    failed_count = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = (
            "id",
            "reference",
            "kind",
            "difficulty",
            "prompt",
            "fen",
            "orientation",
            "side_to_move",
            "setup_moves_san",
            "themes",
            "required_moves",
            "has_hint",
            "variation",
            "variation_name",
            "variation_slug",
            "opening_name",
            "opening_slug",
            "eco",
            "status",
            "attempts_count",
            "failed_count",
        )

    def get_has_hint(self, obj) -> bool:
        return bool(obj.hint)

    def get_status(self, obj) -> str:
        return getattr(obj, "user_status", None) or ExerciseProgress.Status.UNSEEN

    def get_attempts_count(self, obj) -> int:
        return getattr(obj, "user_attempts", 0) or 0

    def get_failed_count(self, obj) -> int:
        return getattr(obj, "user_failed", 0) or 0


class AttemptRequestSerializer(serializers.Serializer):
    moves = serializers.ListField(
        child=serializers.CharField(max_length=10), allow_empty=True, max_length=60
    )
    duration_ms = serializers.IntegerField(min_value=0, max_value=86_400_000, default=0)
    hints_used = serializers.IntegerField(min_value=0, max_value=20, default=0)
    give_up = serializers.BooleanField(default=False)


class AttemptSerializer(serializers.ModelSerializer):
    exercise_reference = serializers.CharField(source="exercise.reference", read_only=True)
    prompt = serializers.CharField(source="exercise.prompt", read_only=True)
    opening_name = serializers.CharField(source="exercise.variation.opening.name", read_only=True)
    variation_name = serializers.CharField(source="exercise.variation.name", read_only=True)

    class Meta:
        model = Attempt
        fields = (
            "id",
            "exercise",
            "exercise_reference",
            "prompt",
            "opening_name",
            "variation_name",
            "status",
            "moves_played",
            "expected_move",
            "played_move",
            "hints_used",
            "gave_up",
            "duration_ms",
            "created_at",
        )
        read_only_fields = fields


class ProgressSerializer(serializers.ModelSerializer):
    exercise_reference = serializers.CharField(source="exercise.reference", read_only=True)
    accuracy = serializers.FloatField(read_only=True)

    class Meta:
        model = ExerciseProgress
        fields = (
            "exercise",
            "exercise_reference",
            "status",
            "attempts_count",
            "solved_count",
            "failed_count",
            "best_duration_ms",
            "first_solved_at",
            "last_attempt_at",
            "needs_review",
            "accuracy",
        )
        read_only_fields = fields
