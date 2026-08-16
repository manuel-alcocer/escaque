from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AttemptListView, ExerciseViewSet, ProgressSummaryView

router = DefaultRouter()
router.register("exercises", ExerciseViewSet, basename="exercise")

urlpatterns = [
    path("", include(router.urls)),
    path("attempts/", AttemptListView.as_view(), name="attempt-list"),
    path("progress/summary/", ProgressSummaryView.as_view(), name="progress-summary"),
]
