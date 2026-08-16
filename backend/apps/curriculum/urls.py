from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import OpeningViewSet, SectionViewSet, VariationViewSet

router = DefaultRouter()
router.register("sections", SectionViewSet, basename="section")
router.register("openings", OpeningViewSet, basename="opening")
router.register("variations", VariationViewSet, basename="variation")

urlpatterns = [path("", include(router.urls))]
