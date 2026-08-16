from rest_framework import serializers

from .models import Opening, Section, TheoryBlock, Variation


class TheoryBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheoryBlock
        fields = (
            "id",
            "kind",
            "title",
            "body",
            "fen",
            "moves_san",
            "moves_uci",
            "highlight_squares",
            "orientation",
            "position",
        )


class VariationStatsMixin(serializers.Serializer):
    """Exercise counts for the signed-in user, injected by the view's annotations."""

    exercise_count = serializers.SerializerMethodField()
    solved_count = serializers.SerializerMethodField()
    failed_count = serializers.SerializerMethodField()

    def get_exercise_count(self, obj) -> int:
        return getattr(obj, "exercise_total", 0) or 0

    def get_solved_count(self, obj) -> int:
        return getattr(obj, "exercise_solved", 0) or 0

    def get_failed_count(self, obj) -> int:
        return getattr(obj, "exercise_failed", 0) or 0


class VariationListSerializer(VariationStatsMixin, serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = (
            "id",
            "slug",
            "name",
            "eco",
            "tagline",
            "moves_san",
            "moves_uci",
            "fen",
            "is_main_line",
            "difficulty",
            "position",
            "parent",
            "exercise_count",
            "solved_count",
            "failed_count",
        )


class VariationDetailSerializer(VariationListSerializer):
    theory_blocks = TheoryBlockSerializer(many=True, read_only=True)
    opening_slug = serializers.CharField(source="opening.slug", read_only=True)
    opening_name = serializers.CharField(source="opening.name", read_only=True)
    opening_colour = serializers.CharField(source="opening.colour", read_only=True)

    class Meta(VariationListSerializer.Meta):
        fields = VariationListSerializer.Meta.fields + (
            "idea",
            "description",
            "theory_blocks",
            "opening_slug",
            "opening_name",
            "opening_colour",
        )


class OpeningListSerializer(serializers.ModelSerializer):
    section_slug = serializers.CharField(source="section.slug", read_only=True)
    variation_count = serializers.IntegerField(read_only=True, default=0)
    exercise_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Opening
        fields = (
            "id",
            "slug",
            "name",
            "alternative_names",
            "eco_range",
            "colour",
            "tagline",
            "summary",
            "moves_san",
            "moves_uci",
            "fen",
            "first_played",
            "position",
            "section_slug",
            "variation_count",
            "exercise_count",
        )


class OpeningDetailSerializer(OpeningListSerializer):
    variations = serializers.SerializerMethodField()

    class Meta(OpeningListSerializer.Meta):
        fields = OpeningListSerializer.Meta.fields + ("description", "variations")

    def get_variations(self, obj):
        variations = self.context.get("variations", [])
        return VariationListSerializer(variations, many=True, context=self.context).data


class SectionSerializer(serializers.ModelSerializer):
    openings = OpeningListSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ("id", "slug", "name", "tagline", "description", "position", "openings")
