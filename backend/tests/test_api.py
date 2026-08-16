"""API behaviour that the interface depends on."""

import pytest
from rest_framework.test import APIClient

from apps.exercises.models import ExerciseProgress


@pytest.fixture
def client(user):
    api = APIClient()
    api.force_authenticate(user=user)
    return api


@pytest.mark.django_db
def test_exercise_detail_never_leaks_the_solution(client, single_move_exercise):
    response = client.get(f"/api/exercises/{single_move_exercise.id}/")
    assert response.status_code == 200
    assert "solution" not in response.data
    assert "hint" not in response.data
    assert response.data["has_hint"] is True
    assert response.data["required_moves"] == 1


@pytest.mark.django_db
def test_hint_is_served_from_its_own_endpoint(client, single_move_exercise):
    response = client.get(f"/api/exercises/{single_move_exercise.id}/hint/")
    assert response.status_code == 200
    assert response.data["hint"] == "Mueve un alfil."


@pytest.mark.django_db
def test_anonymous_requests_are_refused(single_move_exercise):
    assert APIClient().get(f"/api/exercises/{single_move_exercise.id}/").status_code == 401


@pytest.mark.django_db
def test_attempt_in_progress_is_not_recorded(client, two_move_exercise):
    response = client.post(
        f"/api/exercises/{two_move_exercise.id}/attempt/",
        {"moves": ["b5a4"], "duration_ms": 1000},
        format="json",
    )
    assert response.status_code == 200
    assert response.data["result"]["status"] == "in_progress"
    assert response.data["recorded"] is False
    assert "solution" not in response.data
    assert not ExerciseProgress.objects.exists()


@pytest.mark.django_db
def test_solved_attempt_returns_the_line_and_records_progress(client, single_move_exercise):
    response = client.post(
        f"/api/exercises/{single_move_exercise.id}/attempt/",
        {"moves": ["b5a4"], "duration_ms": 2500},
        format="json",
    )
    assert response.data["result"]["status"] == "solved"
    assert response.data["recorded"] is True
    assert response.data["solution"]  # Only revealed once the attempt is over.
    assert response.data["progress"]["status"] == "solved"


@pytest.mark.django_db
def test_illegal_move_is_a_bad_request(client, single_move_exercise):
    response = client.post(
        f"/api/exercises/{single_move_exercise.id}/attempt/",
        {"moves": ["a1a8"]},
        format="json",
    )
    assert response.status_code == 400
    assert not ExerciseProgress.objects.exists()


@pytest.mark.django_db
def test_giving_up_counts_as_a_failure(client, single_move_exercise):
    response = client.post(
        f"/api/exercises/{single_move_exercise.id}/attempt/",
        {"moves": [], "give_up": True},
        format="json",
    )
    assert response.data["result"]["status"] == "failed"
    assert response.data["progress"]["needs_review"] is True
    assert response.data["solution"]


@pytest.mark.django_db
def test_queue_puts_failed_exercises_first(client, single_move_exercise, two_move_exercise):
    client.post(
        f"/api/exercises/{two_move_exercise.id}/attempt/",
        {"moves": ["d2d4"]},
        format="json",
    )
    results = client.get("/api/exercises/queue/").data["results"]
    assert results[0]["reference"] == "test-double"
    assert results[0]["status"] == "failed"


@pytest.mark.django_db
def test_status_filter_selects_what_needs_review(client, single_move_exercise, two_move_exercise):
    client.post(
        f"/api/exercises/{two_move_exercise.id}/attempt/",
        {"moves": ["d2d4"]},
        format="json",
    )
    results = client.get("/api/exercises/?status=review").data["results"]
    assert [row["reference"] for row in results] == ["test-double"]


@pytest.mark.django_db
def test_summary_counts_the_whole_catalogue(client, single_move_exercise, two_move_exercise):
    client.post(
        f"/api/exercises/{single_move_exercise.id}/attempt/",
        {"moves": ["b5a4"]},
        format="json",
    )
    summary = client.get("/api/progress/summary/").data
    assert summary["exercises_total"] == 2
    assert summary["solved"] == 1
    assert summary["unseen"] == 1
    assert summary["by_opening"][0]["slug"] == "espanola"


@pytest.mark.django_db
def test_sections_report_their_opening_counts(client, single_move_exercise):
    """Regression: nested openings need the same annotations as the detail view."""
    sections = client.get("/api/sections/").data
    opening = sections[0]["openings"][0]
    assert opening["variation_count"] == 1
    assert opening["exercise_count"] == 1
