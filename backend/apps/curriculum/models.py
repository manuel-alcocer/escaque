"""Theory content: sections, openings, variations and the prose that explains them.

The move lists are stored twice on purpose. SAN is what a human reads on a score
sheet and what the interface prints; UCI is what the board widget and Stockfish
consume. Both are produced from the same validated game in the seed command, so
they can never drift apart.
"""

from django.db import models

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class Section(models.Model):
    """A top-level area of the site: openings, defences, tactics, endgames..."""

    slug = models.SlugField(max_length=60, unique=True)
    name = models.CharField(max_length=80)
    tagline = models.CharField(max_length=160, blank=True)
    description = models.TextField(blank=True)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("position", "name")

    def __str__(self):
        return self.name


class Opening(models.Model):
    """A named opening or defence, e.g. the Ruy Lopez."""

    class Colour(models.TextChoices):
        WHITE = "white", "Played by White"
        BLACK = "black", "Played by Black"

    section = models.ForeignKey(Section, related_name="openings", on_delete=models.CASCADE)
    slug = models.SlugField(max_length=80, unique=True)
    name = models.CharField(max_length=120)
    alternative_names = models.JSONField(
        default=list, blank=True, help_text="Other names the opening goes by."
    )
    eco_range = models.CharField(max_length=20, blank=True, help_text="e.g. C60-C99")
    colour = models.CharField(max_length=5, choices=Colour.choices, default=Colour.WHITE)
    tagline = models.CharField(max_length=200, blank=True)
    summary = models.TextField(blank=True, help_text="Two or three sentences, plain text.")
    description = models.TextField(blank=True, help_text="Long form theory, Markdown.")
    moves_san = models.JSONField(default=list, help_text="Defining moves from the start position.")
    moves_uci = models.JSONField(default=list)
    fen = models.CharField(max_length=100, default=STARTING_FEN)
    first_played = models.CharField(max_length=60, blank=True)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("section__position", "position", "name")

    def __str__(self):
        return self.name

    @property
    def orientation(self) -> str:
        return self.colour


class Variation(models.Model):
    """A line inside an opening. Sub-variations point at their parent."""

    opening = models.ForeignKey(Opening, related_name="variations", on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    slug = models.SlugField(max_length=100)
    name = models.CharField(max_length=140)
    eco = models.CharField(max_length=10, blank=True)
    tagline = models.CharField(max_length=200, blank=True)
    idea = models.TextField(blank=True, help_text="What both sides are actually trying to do.")
    description = models.TextField(blank=True, help_text="Long form theory, Markdown.")
    moves_san = models.JSONField(default=list, help_text="Full move list from the start position.")
    moves_uci = models.JSONField(default=list)
    fen = models.CharField(max_length=100, default=STARTING_FEN)
    is_main_line = models.BooleanField(default=False)
    difficulty = models.PositiveSmallIntegerField(
        default=2, help_text="1 easy .. 5 hard, drives the recommended order."
    )
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("opening__position", "position", "name")
        constraints = [
            models.UniqueConstraint(fields=("opening", "slug"), name="unique_variation_slug"),
        ]

    def __str__(self):
        return f"{self.opening.name} — {self.name}"

    @property
    def move_number_start(self) -> int:
        return len(self.moves_san) // 2 + 1


class TheoryBlock(models.Model):
    """A chunk of explanation attached to a variation, optionally with a diagram."""

    class Kind(models.TextChoices):
        IDEA = "idea", "Key idea"
        PLAN = "plan", "Typical plan"
        STRUCTURE = "structure", "Pawn structure"
        TRAP = "trap", "Trap to know"
        WARNING = "warning", "Common mistake"
        GAME = "game", "Model game"

    variation = models.ForeignKey(
        Variation, related_name="theory_blocks", on_delete=models.CASCADE
    )
    kind = models.CharField(max_length=12, choices=Kind.choices, default=Kind.IDEA)
    title = models.CharField(max_length=160)
    body = models.TextField(help_text="Markdown.")
    fen = models.CharField(max_length=100, blank=True, help_text="Diagram, optional.")
    moves_san = models.JSONField(default=list, blank=True)
    moves_uci = models.JSONField(default=list, blank=True)
    highlight_squares = models.JSONField(
        default=list, blank=True, help_text="Squares to mark on the diagram, e.g. ['d5', 'f5']."
    )
    orientation = models.CharField(
        max_length=5,
        choices=[("white", "White"), ("black", "Black")],
        default="white",
    )
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("position", "id")

    def __str__(self):
        return self.title
