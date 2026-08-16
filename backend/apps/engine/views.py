import logging

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from .client import EngineUnavailable, StockfishClient

logger = logging.getLogger(__name__)


class AnalyseSerializer(serializers.Serializer):
    fen = serializers.CharField(max_length=100)
    movetime = serializers.IntegerField(min_value=50, max_value=10_000, required=False)
    depth = serializers.IntegerField(min_value=1, max_value=30, required=False)
    multipv = serializers.IntegerField(min_value=1, max_value=5, default=1)


class EngineThrottleMixin:
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "engine"


class AnalyseView(EngineThrottleMixin, APIView):
    """Evaluate a position. Used by the analysis panel after an exercise ends."""

    def post(self, request):
        payload = AnalyseSerializer(data=request.data)
        payload.is_valid(raise_exception=True)
        data = payload.validated_data

        client = StockfishClient()
        try:
            analysis = client.analyse(
                data["fen"],
                movetime_ms=data.get("movetime"),
                depth=data.get("depth"),
                multipv=data["multipv"],
            )
        except ValueError as exc:
            return Response(
                {"detail": f"That is not a position the engine can read: {exc}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except EngineUnavailable as exc:
            logger.warning("Engine unavailable: %s", exc)
            return Response(
                {"detail": str(exc), "available": False},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(analysis.as_dict())


class PlayView(EngineThrottleMixin, APIView):
    """Ask the engine for a single move, so a user can play a line out against it."""

    def post(self, request):
        payload = AnalyseSerializer(data=request.data)
        payload.is_valid(raise_exception=True)
        data = payload.validated_data

        try:
            analysis = StockfishClient().analyse(
                data["fen"], movetime_ms=data.get("movetime", 300)
            )
        except ValueError as exc:
            return Response(
                {"detail": f"That is not a position the engine can read: {exc}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except EngineUnavailable as exc:
            return Response(
                {"detail": str(exc), "available": False},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        if not analysis.best_move_uci:
            return Response({"detail": "The game is over in this position.", "move": None})

        return Response(
            {
                "move": analysis.best_move_uci,
                "san": analysis.best_move_san,
                "score_cp": analysis.lines[0].score_cp if analysis.lines else None,
                "mate_in": analysis.lines[0].mate_in if analysis.lines else None,
            }
        )


class EngineStatusView(APIView):
    """Tell the interface whether the analysis features are worth offering."""

    def get(self, _request):
        try:
            return Response(StockfishClient().ping())
        except EngineUnavailable as exc:
            return Response(
                {"available": False, "detail": str(exc)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
