"""Compile the seed specs onto a real board and write them to the database.

    python manage.py seed_curriculum
    python manage.py seed_curriculum --check     # compile only, touch nothing
    python manage.py seed_curriculum --prune     # also delete content no longer declared

Re-running is safe: rows are matched by slug (content) and reference (exercises),
so an edit updates in place and user attempts keep pointing at the same exercise.
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.curriculum.models import Opening, Section, TheoryBlock, Variation
from apps.curriculum.seed import SECTIONS
from apps.curriculum.seed.schema import (
    OpeningSpec,
    SeedError,
    VariationSpec,
    build_drills,
    compile_exercise,
    compile_line,
)
from apps.exercises.models import Exercise


class Command(BaseCommand):
    help = "Load the openings, variations, theory and exercises into the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--check",
            action="store_true",
            help="Compile every line and report, without writing anything.",
        )
        parser.add_argument(
            "--prune",
            action="store_true",
            help="Delete database content that the seed no longer declares.",
        )

    def handle(self, *args, **options):
        try:
            compiled = self._compile()
        except SeedError as exc:
            raise CommandError(str(exc)) from exc

        totals = compiled["totals"]
        self.stdout.write(
            f"Compiled {totals['sections']} sections, {totals['openings']} openings, "
            f"{totals['variations']} variations, {totals['theory']} theory blocks and "
            f"{totals['exercises']} exercises."
        )

        if options["check"]:
            self.stdout.write(self.style.SUCCESS("Every line is legal. Nothing was written."))
            return

        with transaction.atomic():
            written = self._write(compiled["sections"], prune=options["prune"])

        self.stdout.write(
            self.style.SUCCESS(
                f"Saved {written['openings']} openings, {written['variations']} variations, "
                f"{written['theory']} theory blocks and {written['exercises']} exercises."
            )
        )
        if options["prune"] and written["pruned"]:
            self.stdout.write(f"Removed {written['pruned']} rows no longer in the seed.")

    # -- compilation -------------------------------------------------------

    def _compile(self) -> dict:
        sections = []
        totals = {"sections": 0, "openings": 0, "variations": 0, "theory": 0, "exercises": 0}
        seen_references: set[str] = set()

        for section_spec in SECTIONS:
            totals["sections"] += 1
            openings = []
            for opening_spec in section_spec.openings:
                totals["openings"] += 1
                openings.append(
                    self._compile_opening(opening_spec, totals, seen_references)
                )
            sections.append({"spec": section_spec, "openings": openings})

        return {"sections": sections, "totals": totals}

    def _compile_opening(
        self, spec: OpeningSpec, totals: dict, seen_references: set[str]
    ) -> dict:
        line = compile_line(spec.line, where=f"opening '{spec.slug}'")
        variations = []
        seen_slugs: set[str] = set()

        for position, variation_spec in enumerate(spec.variations, start=1):
            if variation_spec.slug in seen_slugs:
                raise SeedError(
                    f"opening '{spec.slug}': duplicate variation slug '{variation_spec.slug}'."
                )
            seen_slugs.add(variation_spec.slug)
            totals["variations"] += 1
            compiled = self._compile_variation(
                variation_spec, spec, position, totals, seen_references
            )
            variations.append(compiled)

        for compiled in variations:
            parent_slug = compiled["spec"].parent
            if parent_slug and parent_slug not in seen_slugs:
                raise SeedError(
                    f"variation '{compiled['spec'].slug}': parent '{parent_slug}' does not "
                    f"exist in opening '{spec.slug}'."
                )

        return {"spec": spec, "line": line, "variations": variations}

    def _compile_variation(
        self,
        spec: VariationSpec,
        opening: OpeningSpec,
        position: int,
        totals: dict,
        seen_references: set[str],
    ) -> dict:
        line = compile_line(spec.line, where=f"variation '{spec.slug}'")

        theory = []
        for block_position, block in enumerate(spec.theory, start=1):
            totals["theory"] += 1
            block_line = (
                compile_line(block.line, where=f"theory '{block.title}'")
                if block.line
                else line
            )
            theory.append(
                {
                    "kind": block.kind,
                    "title": block.title,
                    "body": block.body,
                    "fen": block_line.fen,
                    "moves_san": block_line.san,
                    "moves_uci": block_line.uci,
                    "highlight_squares": block.highlight,
                    "orientation": block.orientation or opening.colour,
                    "position": block_position,
                }
            )

        exercises = []
        specs = build_drills(spec, opening.colour) + list(spec.exercises)
        for exercise_position, exercise_spec in enumerate(specs, start=1):
            if exercise_spec.ref in seen_references:
                raise SeedError(f"duplicate exercise reference '{exercise_spec.ref}'.")
            seen_references.add(exercise_spec.ref)
            totals["exercises"] += 1
            row = compile_exercise(exercise_spec, opening_colour=opening.colour)
            row["position"] = exercise_position
            exercises.append(row)

        return {
            "spec": spec,
            "line": line,
            "position": position,
            "theory": theory,
            "exercises": exercises,
        }

    # -- persistence -------------------------------------------------------

    def _write(self, sections: list[dict], *, prune: bool) -> dict:
        written = {"openings": 0, "variations": 0, "theory": 0, "exercises": 0, "pruned": 0}
        live_opening_slugs: set[str] = set()
        live_exercise_refs: set[str] = set()

        for section_data in sections:
            spec = section_data["spec"]
            section, _ = Section.objects.update_or_create(
                slug=spec.slug,
                defaults={
                    "name": spec.name,
                    "tagline": spec.tagline,
                    "description": spec.description,
                    "position": spec.position,
                },
            )

            for opening_position, opening_data in enumerate(section_data["openings"], start=1):
                opening_spec: OpeningSpec = opening_data["spec"]
                live_opening_slugs.add(opening_spec.slug)
                opening, _ = Opening.objects.update_or_create(
                    slug=opening_spec.slug,
                    defaults={
                        "section": section,
                        "name": opening_spec.name,
                        "alternative_names": opening_spec.alternative_names,
                        "eco_range": opening_spec.eco_range,
                        "colour": opening_spec.colour,
                        "tagline": opening_spec.tagline,
                        "summary": opening_spec.summary,
                        "description": opening_spec.description,
                        "moves_san": opening_data["line"].san,
                        "moves_uci": opening_data["line"].uci,
                        "fen": opening_data["line"].fen,
                        "first_played": opening_spec.first_played,
                        "position": opening_position,
                    },
                )
                written["openings"] += 1

                variations_by_slug: dict[str, Variation] = {}
                for variation_data in opening_data["variations"]:
                    variation_spec: VariationSpec = variation_data["spec"]
                    variation, _ = Variation.objects.update_or_create(
                        opening=opening,
                        slug=variation_spec.slug,
                        defaults={
                            "name": variation_spec.name,
                            "eco": variation_spec.eco,
                            "tagline": variation_spec.tagline,
                            "idea": variation_spec.idea,
                            "description": variation_spec.description,
                            "moves_san": variation_data["line"].san,
                            "moves_uci": variation_data["line"].uci,
                            "fen": variation_data["line"].fen,
                            "is_main_line": variation_spec.is_main_line,
                            "difficulty": variation_spec.difficulty,
                            "position": variation_data["position"],
                        },
                    )
                    variations_by_slug[variation_spec.slug] = variation
                    written["variations"] += 1

                    # Theory blocks have no natural key, so they are rebuilt wholesale.
                    variation.theory_blocks.all().delete()
                    TheoryBlock.objects.bulk_create(
                        [TheoryBlock(variation=variation, **block) for block in variation_data["theory"]]
                    )
                    written["theory"] += len(variation_data["theory"])

                    for row in variation_data["exercises"]:
                        reference = row.pop("reference")
                        live_exercise_refs.add(reference)
                        Exercise.objects.update_or_create(
                            reference=reference,
                            defaults={"variation": variation, "is_active": True, **row},
                        )
                        written["exercises"] += 1
                        row["reference"] = reference

                # Parents are linked once every variation of the opening exists.
                for variation_data in opening_data["variations"]:
                    parent_slug = variation_data["spec"].parent
                    variation = variations_by_slug[variation_data["spec"].slug]
                    parent = variations_by_slug.get(parent_slug) if parent_slug else None
                    if variation.parent_id != (parent.id if parent else None):
                        variation.parent = parent
                        variation.save(update_fields=["parent"])

        if prune:
            stale_exercises = Exercise.objects.exclude(reference__in=live_exercise_refs)
            written["pruned"] += stale_exercises.count()
            stale_exercises.delete()

            stale_openings = Opening.objects.exclude(slug__in=live_opening_slugs)
            written["pruned"] += stale_openings.count()
            stale_openings.delete()

        return written
