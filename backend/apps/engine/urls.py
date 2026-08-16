from django.urls import path

from .views import AnalyseView, EngineStatusView, PlayView

urlpatterns = [
    path("analyse/", AnalyseView.as_view(), name="engine-analyse"),
    path("play/", PlayView.as_view(), name="engine-play"),
    path("status/", EngineStatusView.as_view(), name="engine-status"),
]
