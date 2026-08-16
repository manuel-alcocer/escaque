import django_filters
from django.db.models import (
    BooleanField,
    Count,
    IntegerField,
    OuterRef,
    Q,
    Subquery,
    Value,
)
from django.db.models.functions import Coalesce
from rest_framework import status as http_status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.curriculum.models import Opening

from .models import Attempt, Exercise, ExerciseProgress
from .serializers import (
    AttemptRequestSerializer,
    AttemptSerializer,
    ExerciseSerializer,
)
from .services import FAILED, IN_PROGRESS, InvalidMove, evaluate, register_attempt

CHAR = "user_status"


def annotate_for_user(queryset, user):
    """Attach the signed-in user's counters to every exercise row."""

    progress = ExerciseProgress.objects.filter(user=user, exercise=OuterRef("pk"))
    return queryset.annotate(
        user_status=Coalesce(
            Subquery(progress.values("status")[:1]),
            Value(ExerciseProgress.Status.UNSEEN),
        ),
        user_needs_review=Coalesce(
            Subquery(progress.values("needs_review")[:1], output_field=BooleanField()),
            Value(False),
            output_field=BooleanField(),
        ),
        user_attempts=Coalesce(
            Subquery(progress.values("attempts_count")[:1], output_field=IntegerField()),
            Value(0),
            output_field=IntegerField(),
        ),
        user_failed=Coalesce(
            Subquery(progress.values("failed_count")[:1], output_field=IntegerField()),
            Value(0),
            output_field=IntegerField(),
        ),
        user_solved=Coalesce(
            Subquery(progress.values("solved_count")[:1], output_field=IntegerField()),
            Value(0),
            output_field=IntegerField(),
        ),
    )


class ExerciseFilter(django_filters.FilterSet):
    opening = django_filters.CharFilter(field_name="variation__opening__slug")
    section = django_filters.CharFilter(field_name="variation__opening__section__slug")
    variation = django_filters.NumberFilter(field_name="variation_id")
    variation_slug = django_filters.CharFilter(field_name="variation__slug")
    kind = django_filters.CharFilter(field_name="kind")
    difficulty = django_filters.NumberFilter(field_name="difficulty")
    difficulty_max = django_filters.NumberFilter(field_name="difficulty", lookup_expr="lte")
    theme = django_filters.CharFilter(method="filter_theme")
    status = django_filters.CharFilter(method="filter_status")

    class Meta:
        model = Exercise
        fields = ["opening", "section", "variation", "kind", "difficulty"]

    def filter_theme(self, queryset, name, value):
        return queryset.filter(themes__icontains=value)

    def filter_status(self, queryset, name, value):
        if value == "review":
            return queryset.filter(user_needs_review=True)
        if value in {"solved", "failed", "unseen"}:
            return queryset.filter(user_status=value)
        return queryset


class ExerciseViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ExerciseSerializer
    filterset_class = ExerciseFilter
    ordering_fields = ("difficulty", "position", "id")

    def get_queryset(self):
        queryset = Exercise.objects.filter(is_active=True).select_related(
            "variation", "variation__opening", "variation__opening__section"
        )
        return annotate_for_user(queryset, self.request.user)

    @action(detail=True, methods=["get"])
    def hint(self, request, pk=None):
        """Serve the hint separately so asking for it is a deliberate act."""
        exercise = self.get_object()
        if not exercise.hint:
            return Response(
                {"detail": "This exercise has no hint."}, status=http_status.HTTP_404_NOT_FOUND
            )
        return Response({"hint": exercise.hint})

    @action(detail=True, methods=["post"])
    def attempt(self, request, pk=None):
        """Check the moves played so far and record the result once it is decided."""
        exercise = self.get_object()
        payload = AttemptRequestSerializer(data=request.data)
        payload.is_valid(raise_exception=True)
        data = payload.validated_data

        if data["give_up"]:
            evaluation = evaluate(exercise, [])
            evaluation.status = FAILED
            evaluation.line_san = _line_san(exercise)
            attempt, progress = register_attempt(
                user=request.user,
                exercise=exercise,
                evaluation=evaluation,
                moves_played=data["moves"],
                duration_ms=data["duration_ms"],
                hints_used=data["hints_used"],
                gave_up=True,
            )
            return Response(
                {
                    "result": evaluation.as_dict(),
                    "recorded": True,
                    "solution": exercise.solution,
                    "explanation": exercise.explanation,
                    "progress": _progress_payload(progress),
                }
            )

        try:
            evaluation = evaluate(exercise, data["moves"])
        except InvalidMove as exc:
            raise ValidationError({"moves": str(exc)}) from exc

        if evaluation.status == IN_PROGRESS:
            return Response({"result": evaluation.as_dict(), "recorded": False})

        attempt, progress = register_attempt(
            user=request.user,
            exercise=exercise,
            evaluation=evaluation,
            moves_played=data["moves"],
            duration_ms=data["duration_ms"],
            hints_used=data["hints_used"],
        )
        return Response(
            {
                "result": evaluation.as_dict(),
                "recorded": True,
                "attempt_id": attempt.id,
                "solution": exercise.solution,
                "explanation": exercise.explanation,
                "progress": _progress_payload(progress),
            }
        )

    @action(detail=False, methods=["get"])
    def queue(self, request):
        """The next exercises to work on.

        Order: failed ones first (that is the point of marking them), then unseen,
        then solved ones for review. Ties break on difficulty so a session warms up.
        """
        queryset = self.filter_queryset(self.get_queryset())
        limit = min(int(request.query_params.get("limit", 20)), 100)

        buckets = []
        for predicate in (
            Q(user_needs_review=True),
            Q(user_status=ExerciseProgress.Status.UNSEEN),
            Q(user_status=ExerciseProgress.Status.SOLVED),
        ):
            remaining = limit - len(buckets)
            if remaining <= 0:
                break
            chunk = list(
                queryset.filter(predicate)
                .exclude(id__in=[item.id for item in buckets])
                .order_by("difficulty", "variation__position", "position", "id")[:remaining]
            )
            buckets.extend(chunk)

        return Response(
            {
                "count": len(buckets),
                "results": ExerciseSerializer(buckets, many=True).data,
            }
        )


def _line_san(exercise):
    from .services import _full_line_san

    return _full_line_san(exercise)


def _progress_payload(progress):
    return {
        "status": progress.status,
        "attempts_count": progress.attempts_count,
        "solved_count": progress.solved_count,
        "failed_count": progress.failed_count,
        "needs_review": progress.needs_review,
        "best_duration_ms": progress.best_duration_ms,
    }


class AttemptListView(ListAPIView):
    """The user's own attempt history, newest first."""

    serializer_class = AttemptSerializer

    def get_queryset(self):
        return (
            Attempt.objects.filter(user=self.request.user)
            .select_related("exercise", "exercise__variation", "exercise__variation__opening")
            .order_by("-created_at")
        )


class ProgressSummaryView(APIView):
    """Totals for the dashboard: overall, per opening, and what to fix next."""

    def get(self, request):
        user = request.user
        active = Exercise.objects.filter(is_active=True)
        total = active.count()

        rows = ExerciseProgress.objects.filter(user=user, exercise__is_active=True)
        aggregates = rows.aggregate(
            solved=Count("id", filter=Q(status=ExerciseProgress.Status.SOLVED)),
            failed=Count("id", filter=Q(status=ExerciseProgress.Status.FAILED)),
            review=Count("id", filter=Q(needs_review=True)),
            attempted=Count("id"),
        )
        attempts = Attempt.objects.filter(user=user)
        attempt_totals = attempts.aggregate(
            total=Count("id"),
            solved=Count("id", filter=Q(status=Attempt.Status.SOLVED)),
        )

        per_opening = []
        openings = Opening.objects.select_related("section").order_by("position", "name")
        for opening in openings:
            opening_exercises = active.filter(variation__opening=opening)
            opening_total = opening_exercises.count()
            if not opening_total:
                continue
            opening_rows = rows.filter(exercise__variation__opening=opening).aggregate(
                solved=Count("id", filter=Q(status=ExerciseProgress.Status.SOLVED)),
                failed=Count("id", filter=Q(status=ExerciseProgress.Status.FAILED)),
                review=Count("id", filter=Q(needs_review=True)),
            )
            per_opening.append(
                {
                    "slug": opening.slug,
                    "name": opening.name,
                    "section": opening.section.slug,
                    "eco_range": opening.eco_range,
                    "total": opening_total,
                    "solved": opening_rows["solved"],
                    "failed": opening_rows["failed"],
                    "needs_review": opening_rows["review"],
                    "unseen": opening_total
                    - opening_rows["solved"]
                    - opening_rows["failed"],
                }
            )

        return Response(
            {
                "exercises_total": total,
                "solved": aggregates["solved"],
                "failed": aggregates["failed"],
                "needs_review": aggregates["review"],
                "unseen": total - aggregates["attempted"],
                "attempts_total": attempt_totals["total"],
                "attempts_solved": attempt_totals["solved"],
                "accuracy": (
                    round(attempt_totals["solved"] / attempt_totals["total"], 3)
                    if attempt_totals["total"]
                    else None
                ),
                "by_opening": per_opening,
                "recent": AttemptSerializer(
                    attempts.select_related(
                        "exercise", "exercise__variation", "exercise__variation__opening"
                    ).order_by("-created_at")[:10],
                    many=True,
                ).data,
            }
        )
