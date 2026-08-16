import pytest
from django.contrib.auth import get_user_model

from apps.curriculum.models import Opening, Section, Variation
from apps.exercises.models import Exercise

User = get_user_model()

# 1.e4 e5 2.Nf3 Nc6 3.Bb5 a6 — Black has just played ...a6.
RUY_A6_FEN = "r1bqkbnr/1ppp1ppp/p1n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 4"


@pytest.fixture
def user(db):
    return User.objects.create_user(username="ana", password="tablero-de-ajedrez-42")


@pytest.fixture
def variation(db):
    section = Section.objects.create(slug="aperturas", name="Aperturas")
    opening = Opening.objects.create(
        section=section, slug="espanola", name="Apertura Española", colour="white"
    )
    return Variation.objects.create(opening=opening, slug="morphy", name="Defensa Morphy")


@pytest.fixture
def single_move_exercise(variation):
    """One move to find: 4.Ba4."""
    return Exercise.objects.create(
        variation=variation,
        reference="test-single",
        prompt="Retira el alfil.",
        fen=RUY_A6_FEN,
        side_to_move="white",
        orientation="white",
        hint="Mueve un alfil.",
        explanation="4.Aa4 mantiene la clavada.",
        solution=[{"uci": "b5a4", "san": "Ba4", "by": "user", "also": ["b5c6"]}],
    )


@pytest.fixture
def two_move_exercise(variation):
    """Two user moves with an opponent reply in between: 4.Ba4 Nf6 5.O-O."""
    return Exercise.objects.create(
        variation=variation,
        reference="test-double",
        prompt="Juega las dos siguientes jugadas.",
        fen=RUY_A6_FEN,
        side_to_move="white",
        orientation="white",
        solution=[
            {"uci": "b5a4", "san": "Ba4", "by": "user"},
            {"uci": "g8f6", "san": "Nf6", "by": "opponent"},
            {"uci": "e1g1", "san": "O-O", "by": "user"},
        ],
    )
