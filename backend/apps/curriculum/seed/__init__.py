"""Seed content for the trainer.

Every line here is written once, in SAN, from the starting position, and compiled
by `schema.py` against a real board. A typo produces a build error instead of an
exercise with an impossible answer.
"""

from .caro_kann import CARO_KANN
from .kings_indian import KINGS_INDIAN
from .schema import SectionSpec
from .spanish import SPANISH

SECTIONS: list[SectionSpec] = [
    SectionSpec(
        slug="aperturas",
        name="Aperturas",
        tagline="Lo que juegan las blancas cuando eligen el terreno",
        description=(
            "Aperturas en las que las blancas marcan el carácter de la partida desde la "
            "primera jugada. Se estudian desde el lado que las plantea."
        ),
        position=1,
        openings=[SPANISH],
    ),
    SectionSpec(
        slug="defensas",
        name="Defensas",
        tagline="Cómo responden las negras a 1.e4 y 1.d4",
        description=(
            "Sistemas para las negras. Cada uno concede algo a cambio de otra cosa: "
            "la India de Rey cede el centro para atacarlo después, la Caro-Kann renuncia "
            "a la iniciativa a cambio de una estructura sin debilidades."
        ),
        position=2,
        openings=[KINGS_INDIAN, CARO_KANN],
    ),
]

__all__ = ["SECTIONS", "SPANISH", "KINGS_INDIAN", "CARO_KANN"]
