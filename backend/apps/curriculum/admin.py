from django.contrib import admin

from .models import Opening, Section, TheoryBlock, Variation


class OpeningInline(admin.TabularInline):
    model = Opening
    extra = 0
    fields = ("name", "slug", "eco_range", "colour", "position")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "position")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [OpeningInline]


class TheoryBlockInline(admin.StackedInline):
    model = TheoryBlock
    extra = 0


@admin.register(Opening)
class OpeningAdmin(admin.ModelAdmin):
    list_display = ("name", "section", "eco_range", "colour", "position")
    list_filter = ("section", "colour")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ("name", "opening", "eco", "is_main_line", "difficulty", "position")
    list_filter = ("opening", "is_main_line", "difficulty")
    search_fields = ("name", "slug", "eco")
    inlines = [TheoryBlockInline]


@admin.register(TheoryBlock)
class TheoryBlockAdmin(admin.ModelAdmin):
    list_display = ("title", "variation", "kind", "position")
    list_filter = ("kind",)
    search_fields = ("title", "body")
