from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def healthz(_request):
    """Liveness probe for Kubernetes."""
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("healthz", healthz),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/", include("apps.curriculum.urls")),
    path("api/", include("apps.exercises.urls")),
    path("api/engine/", include("apps.engine.urls")),
]
