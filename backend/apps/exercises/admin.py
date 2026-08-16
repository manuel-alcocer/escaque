from django.contrib import admin

from .models import Attempt, Exercise, ExerciseProgress


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("reference", "kind", "difficulty", "variation", "is_active")
    list_filter = ("kind", "difficulty", "is_active", "variation__opening")
    search_fields = ("reference", "prompt", "fen")
    autocomplete_fields = ("variation",)
    readonly_fields = ("created_at",)


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user", "exercise", "status", "duration_ms", "gave_up")
    list_filter = ("status", "gave_up", "created_at")
    search_fields = ("user__username", "exercise__reference")
    readonly_fields = [field.name for field in Attempt._meta.fields]

    def has_add_permission(self, request):
        return False


@admin.register(ExerciseProgress)
class ExerciseProgressAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "exercise",
        "status",
        "attempts_count",
        "solved_count",
        "failed_count",
        "needs_review",
    )
    list_filter = ("status", "needs_review")
    search_fields = ("user__username", "exercise__reference")
