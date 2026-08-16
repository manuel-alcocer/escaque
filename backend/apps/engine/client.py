"""Talk UCI to the Stockfish container over a plain TCP socket.

The engine runs as its own container (see docker/stockfish). `socat` gives every
incoming connection a fresh Stockfish process, so a connection is opened per
request and closed straight after: no shared state to leak between users, and no
half-dead engine to nurse back to life.

Nothing here is on the critical path. Exercises are checked against their stored
line by apps.exercises.services, so the site keeps working when the engine is
down; the analysis panel just reports it is unavailable.
"""

from __future__ import annotations

import logging
import socket
from dataclasses import dataclass, field

import chess
from django.conf import settings

logger = logging.getLogger(__name__)


class EngineUnavailable(RuntimeError):
    """The engine could not be reached or did not answer in time."""


@dataclass
class Line:
    """One principal variation returned by the engine."""

    rank: int
    depth: int
    score_cp: int | None
    mate_in: int | None
    moves_uci: list[str] = field(default_factory=list)
    moves_san: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "rank": self.rank,
            "depth": self.depth,
            "score_cp": self.score_cp,
            "mate_in": self.mate_in,
            "moves_uci": self.moves_uci,
            "moves_san": self.moves_san,
        }


@dataclass
class Analysis:
    fen: str
    best_move_uci: str
    best_move_san: str
    depth: int
    lines: list[Line] = field(default_factory=list)
    engine_name: str = ""

    def as_dict(self) -> dict:
        return {
            "fen": self.fen,
            "best_move_uci": self.best_move_uci,
            "best_move_san": self.best_move_san,
            "depth": self.depth,
            "engine": self.engine_name,
            "lines": [line.as_dict() for line in self.lines],
        }


class _Connection:
    """Line-oriented wrapper around the socket, because UCI is a line protocol."""

    def __init__(self, host: str, port: int, timeout: float):
        self._buffer = b""
        try:
            self._socket = socket.create_connection((host, port), timeout=timeout)
        except OSError as exc:
            raise EngineUnavailable(f"Cannot reach the engine at {host}:{port}.") from exc
        self._socket.settimeout(timeout)

    def send(self, command: str) -> None:
        try:
            self._socket.sendall(f"{command}\n".encode())
        except OSError as exc:
            raise EngineUnavailable("The engine closed the connection.") from exc

    def read_line(self) -> str:
        while b"\n" not in self._buffer:
            try:
                chunk = self._socket.recv(4096)
            except TimeoutError as exc:
                raise EngineUnavailable("The engine did not answer in time.") from exc
            except OSError as exc:
                raise EngineUnavailable("The engine closed the connection.") from exc
            if not chunk:
                raise EngineUnavailable("The engine closed the connection.")
            self._buffer += chunk
        line, self._buffer = self._buffer.split(b"\n", 1)
        return line.decode(errors="replace").strip()

    def read_until(self, prefix: str, *, collect: bool = False) -> list[str]:
        collected = []
        while True:
            line = self.read_line()
            if collect and line:
                collected.append(line)
            if line.startswith(prefix):
                if not collect:
                    collected.append(line)
                return collected

    def close(self) -> None:
        try:
            self.send("quit")
        except EngineUnavailable:
            pass
        try:
            self._socket.close()
        except OSError:
            pass

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        self.close()


class StockfishClient:
    def __init__(self, config: dict | None = None):
        config = config or settings.STOCKFISH
        self.host = config["HOST"]
        self.port = int(config["PORT"])
        self.timeout = float(config["TIMEOUT"])
        self.default_movetime = int(config["DEFAULT_MOVETIME"])
        self.max_movetime = int(config["MAX_MOVETIME"])

    def ping(self) -> dict:
        """Check the engine answers, and report which one it is."""
        with _Connection(self.host, self.port, self.timeout) as connection:
            connection.send("uci")
            header = connection.read_until("uciok", collect=True)
            name = next(
                (
                    line.removeprefix("id name ").strip()
                    for line in header
                    if line.startswith("id name ")
                ),
                "unknown",
            )
            connection.send("isready")
            connection.read_until("readyok")
            return {"available": True, "engine": name, "host": self.host, "port": self.port}

    def analyse(
        self,
        fen: str,
        *,
        movetime_ms: int | None = None,
        multipv: int = 1,
        depth: int | None = None,
    ) -> Analysis:
        board = chess.Board(fen)  # Raises ValueError on a malformed FEN.
        movetime = min(int(movetime_ms or self.default_movetime), self.max_movetime)
        multipv = max(1, min(int(multipv), 5))

        # A socket timeout shorter than the thinking time would kill our own request.
        timeout = max(self.timeout, movetime / 1000 + 5)

        with _Connection(self.host, self.port, timeout) as connection:
            connection.send("uci")
            header = connection.read_until("uciok", collect=True)
            engine_name = next(
                (
                    line.removeprefix("id name ").strip()
                    for line in header
                    if line.startswith("id name ")
                ),
                "Stockfish",
            )
            connection.send(f"setoption name MultiPV value {multipv}")
            connection.send("isready")
            connection.read_until("readyok")
            connection.send("ucinewgame")
            connection.send(f"position fen {board.fen()}")
            connection.send(
                f"go depth {int(depth)}" if depth else f"go movetime {movetime}"
            )

            info_lines: dict[int, dict] = {}
            best_move = ""
            while True:
                line = connection.read_line()
                if line.startswith("info "):
                    parsed = _parse_info(line)
                    if parsed:
                        info_lines[parsed["multipv"]] = parsed
                elif line.startswith("bestmove"):
                    parts = line.split()
                    best_move = parts[1] if len(parts) > 1 else ""
                    break

        lines = [
            _build_line(board, rank, info)
            for rank, info in sorted(info_lines.items())
            if info.get("pv")
        ]
        depth_reached = max((info["depth"] for info in info_lines.values()), default=0)

        return Analysis(
            fen=board.fen(),
            best_move_uci=best_move if best_move not in {"(none)", ""} else "",
            best_move_san=_safe_san(board, best_move),
            depth=depth_reached,
            lines=lines,
            engine_name=engine_name,
        )

    def best_move(self, fen: str, *, movetime_ms: int | None = None) -> str:
        return self.analyse(fen, movetime_ms=movetime_ms).best_move_uci


def _parse_info(line: str) -> dict | None:
    tokens = line.split()
    info = {"multipv": 1, "depth": 0, "score_cp": None, "mate_in": None, "pv": []}
    index = 1
    while index < len(tokens):
        token = tokens[index]
        if token == "depth" and index + 1 < len(tokens):
            info["depth"] = _as_int(tokens[index + 1])
            index += 2
        elif token == "multipv" and index + 1 < len(tokens):
            info["multipv"] = _as_int(tokens[index + 1]) or 1
            index += 2
        elif token == "score" and index + 2 < len(tokens):
            kind, value = tokens[index + 1], _as_int(tokens[index + 2])
            if kind == "cp":
                info["score_cp"] = value
            elif kind == "mate":
                info["mate_in"] = value
            index += 3
        elif token == "pv":
            info["pv"] = tokens[index + 1 :]
            break
        else:
            index += 1
    return info if info["pv"] or info["depth"] else None


def _as_int(value: str) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _build_line(board: chess.Board, rank: int, info: dict) -> Line:
    """Turn a UCI principal variation into readable SAN without mutating `board`."""
    replay = board.copy(stack=False)
    san_moves = []
    uci_moves = []
    for uci in info["pv"]:
        try:
            move = chess.Move.from_uci(uci)
        except ValueError:
            break
        if move not in replay.legal_moves:
            break
        san_moves.append(replay.san(move))
        uci_moves.append(uci)
        replay.push(move)

    return Line(
        rank=rank,
        depth=info["depth"] or 0,
        score_cp=info["score_cp"],
        mate_in=info["mate_in"],
        moves_uci=uci_moves,
        moves_san=san_moves,
    )


def _safe_san(board: chess.Board, uci: str) -> str:
    if not uci or uci == "(none)":
        return ""
    try:
        move = chess.Move.from_uci(uci)
        return board.san(move) if move in board.legal_moves else ""
    except ValueError:
        return ""
