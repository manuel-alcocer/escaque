from django.db.models import Count, Prefetch, Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from apps.exercises.models import ExerciseProgress

from .models import Opening, Section, Variation
from .serializers import (
    OpeningDetailSerializer,
    OpeningListSerializer,
    SectionSerializer,
    VariationDetailSerializer,
)


def variations_with_stats(queryset, user):
    """Count exercises per variation, split by how the user is doing on them."""

    solved = Q(
        exercises__progress__user=user,
        exercises__progress__status=ExerciseProgress.Status.SOLVED,
    )
    failed = Q(
        exercises__progress__user=user,
        exercises__progress__status=ExerciseProgress.Status.FAILED,
    )
    return queryset.annotate(
        exercise_total=Count("exercises", filter=Q(exercises__is_active=True), distinct=True),
        exercise_solved=Count("exercises", filter=solved, distinct=True),
        exercise_failed=Count("exercises", filter=failed, distinct=True),
    )


def openings_with_counts():
    """Openings carrying their variation and exercise totals.

    Shared by both viewsets: the section list nests openings, and without the
    same annotations there they would all report zero.
    """
    return (
        Opening.objects.select_related("section")
        .annotate(
            variation_count=Count("variations", distinct=True),
            exercise_count=Count(
                "variations__exercises",
                filter=Q(variations__exercises__is_active=True),
                distinct=True,
            ),
        )
        .order_by("position", "name")
    )


class SectionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SectionSerializer
    lookup_field = "slug"
    pagination_class = None

    def get_queryset(self):
        return Section.objects.prefetch_related(
            Prefetch("openings", queryset=openings_with_counts())
        )


class OpeningViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"
    pagination_class = None

    def get_queryset(self):
        return openings_with_counts()

    def get_serializer_class(self):
        return OpeningDetailSerializer if self.action == "retrieve" else OpeningListSerializer

    def retrieve(self, request, *args, **kwargs):
        opening = self.get_object()
        variations = variations_with_stats(
            Variation.objects.filter(opening=opening), request.user
        ).order_by("position", "name")
        serializer = self.get_serializer(
            opening, context={**self.get_serializer_context(), "variations": variations}
        )
        return Response(serializer.data)


class VariationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VariationDetailSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Variation.objects.select_related("opening").prefetch_related("theory_blocks")
        opening_slug = self.request.query_params.get("opening")
        if opening_slug:
            queryset = queryset.filter(opening__slug=opening_slug)
        return variations_with_stats(queryset, self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        lookup = self.kwargs.get("pk", "")
        if lookup.isdigit():
            return get_object_or_404(queryset, pk=int(lookup))
        return get_object_or_404(queryset, slug=lookup)
