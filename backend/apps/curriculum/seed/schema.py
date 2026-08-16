"""Declarative content specs and the compiler that turns them into board data.

Content is written the way a player would write it: a list of SAN moves from the
starting position. `compile_*` replays every list on a real board, so the FEN, the
UCI list and the side to move are derived rather than typed, and a wrong move
raises `SeedError` with the exact spot it broke.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import chess

STARTING_FEN = chess.STARTING_FEN


class SeedError(ValueError):
    """A line in the seed data does not survive contact with a chessboard."""


@dataclass
class TheorySpec:
    title: str
    body: str
    kind: str = "idea"
    # Position to show under the text. Defaults to the variation's own position.
    line: list[str] | None = None
    highlight: list[str] = field(default_factory=list)
    orientation: str = ""


@dataclass
class ExerciseSpec:
    """One exercise.

    `setup` is how the position was reached; `answer` alternates user move,
    opponent reply, user move... always starting with the user. `also` maps the
    index of a user move (0 for the first) to extra moves accepted as correct.
    """

    ref: str
    prompt: str
    setup: list[str]
    answer: list[str]
    kind: str = "theory"
    difficulty: int = 2
    explanation: str = ""
    hint: str = ""
    themes: list[str] = field(default_factory=list)
    also: dict[int, list[str]] = field(default_factory=dict)
    orientation: str = ""
    # Sanity checks run at seed time: "mate" or "check".
    expect: str = ""


@dataclass
class VariationSpec:
    slug: str
    name: str
    line: list[str]
    eco: str = ""
    tagline: str = ""
    idea: str = ""
    description: str = ""
    is_main_line: bool = False
    difficulty: int = 2
    parent: str = ""
    theory: list[TheorySpec] = field(default_factory=list)
    exercises: list[ExerciseSpec] = field(default_factory=list)
    # Ply indexes of `line` the user has to find, turned into one exercise each.
    drill_plies: list[int] = field(default_factory=list)
    drill_difficulty: int = 2


@dataclass
class OpeningSpec:
    slug: str
    name: str
    line: list[str]
    eco_range: str = ""
    colour: str = "white"
    tagline: str = ""
    summary: str = ""
    description: str = ""
    first_played: str = ""
    alternative_names: list[str] = field(default_factory=list)
    variations: list[VariationSpec] = field(default_factory=list)


@dataclass
class SectionSpec:
    slug: str
    name: str
    tagline: str = ""
    description: str = ""
    position: int = 0
    openings: list[OpeningSpec] = field(default_factory=list)


# --- compilation ----------------------------------------------------------


@dataclass
class CompiledLine:
    san: list[str]
    uci: list[str]
    fen: str
    turn: str


def compile_line(moves: list[str], *, where: str) -> CompiledLine:
    """Replay SAN moves from the start position and report what they produce."""

    board = chess.Board()
    san_moves: list[str] = []
    uci_moves: list[str] = []

    for index, san in enumerate(moves):
        try:
            move = board.parse_san(san)
        except (ValueError, AssertionError) as exc:
            played = " ".join(san_moves) or "(start)"
            raise SeedError(
                f"{where}: move {index + 1} '{san}' is illegal after {played}."
            ) from exc
        san_moves.append(board.san(move))
        uci_moves.append(move.uci())
        board.push(move)

    return CompiledLine(
        san=san_moves,
        uci=uci_moves,
        fen=board.fen(),
        turn="white" if board.turn == chess.WHITE else "black",
    )


def compile_exercise(spec: ExerciseSpec, *, opening_colour: str) -> dict:
    """Turn an ExerciseSpec into the row stored in the database."""

    where = f"exercise '{spec.ref}'"
    setup = compile_line(spec.setup, where=f"{where} setup")

    board = chess.Board(setup.fen)
    solution: list[dict] = []
    user_move_index = 0

    for index, san in enumerate(spec.answer):
        by = "user" if index % 2 == 0 else "opponent"
        try:
            move = board.parse_san(san)
        except (ValueError, AssertionError) as exc:
            raise SeedError(
                f"{where}: answer move {index + 1} '{san}' is illegal in {board.fen()}."
            ) from exc

        ply = {"uci": move.uci(), "san": board.san(move), "by": by}

        if by == "user":
            alternatives = spec.also.get(user_move_index, [])
            if alternatives:
                ply["also"] = [
                    _validate_alternative(board, alt, where) for alt in alternatives
                ]
            user_move_index += 1

        solution.append(ply)
        board.push(move)

    if not solution:
        raise SeedError(f"{where}: the answer is empty.")
    if solution[0]["by"] != "user":
        raise SeedError(f"{where}: the answer must start with the user's move.")

    _check_expectation(spec, board, where)

    side_to_move = setup.turn
    orientation = spec.orientation or side_to_move or opening_colour

    return {
        "reference": spec.ref,
        "kind": spec.kind,
        "difficulty": spec.difficulty,
        "prompt": spec.prompt,
        "explanation": spec.explanation,
        "fen": setup.fen,
        "orientation": orientation,
        "side_to_move": side_to_move,
        "setup_moves_san": setup.san,
        "solution": solution,
        "hint": spec.hint,
        "themes": spec.themes,
    }


def _validate_alternative(board: chess.Board, san: str, where: str) -> str:
    try:
        move = board.parse_san(san)
    except (ValueError, AssertionError) as exc:
        raise SeedError(
            f"{where}: alternative '{san}' is illegal in {board.fen()}."
        ) from exc
    return move.uci()


def _check_expectation(spec: ExerciseSpec, board: chess.Board, where: str) -> None:
    if spec.expect == "mate" and not board.is_checkmate():
        raise SeedError(f"{where}: the line was declared mate but the position is not mate.")
    if spec.expect == "check" and not board.is_check():
        raise SeedError(f"{where}: the line was declared check but the king is not in check.")


def build_drills(variation: VariationSpec, opening_colour: str) -> list[ExerciseSpec]:
    """Generate one 'find the move' exercise per requested ply of the main line.

    This is where the bulk of the exercise count comes from, and it is safe by
    construction: the answer is the move the line actually plays.
    """

    drills: list[ExerciseSpec] = []
    board = chess.Board()
    san_history: list[str] = []

    for index, san in enumerate(variation.line):
        if index in variation.drill_plies:
            mover = "white" if board.turn == chess.WHITE else "black"
            move_number = board.fullmove_number
            drills.append(
                ExerciseSpec(
                    ref=f"{variation.slug}-drill-{index:02d}",
                    prompt=_drill_prompt(variation, san_history, move_number, mover),
                    setup=list(san_history),
                    answer=[san],
                    kind="theory",
                    difficulty=variation.drill_difficulty,
                    explanation=(
                        f"La continuación principal es {move_number}"
                        f"{'.' if mover == 'white' else '...'} {san}."
                    ),
                    hint=_drill_hint(san),
                    themes=["línea principal", variation.name],
                    orientation=mover,
                )
            )
        try:
            move = board.parse_san(san)
        except (ValueError, AssertionError) as exc:
            played = " ".join(san_history) or "(start)"
            raise SeedError(
                f"variation '{variation.slug}': move {index + 1} '{san}' is illegal "
                f"after {played}."
            ) from exc
        san_history.append(board.san(move))
        board.push(move)

    missing = [ply for ply in variation.drill_plies if ply >= len(variation.line)]
    if missing:
        raise SeedError(
            f"variation '{variation.slug}': drill plies {missing} are past the end of the line."
        )

    return drills


def _drill_prompt(
    variation: VariationSpec, history: list[str], move_number: int, mover: str
) -> str:
    side = "las blancas" if mover == "white" else "las negras"
    if not history:
        return f"{variation.name}: juega la primera jugada de la línea."
    return (
        f"{variation.name}. Juegan {side} en la jugada {move_number}: "
        "encuentra la continuación teórica."
    )


def _drill_hint(san: str) -> str:
    piece = {
        "K": "el rey",
        "Q": "la dama",
        "R": "una torre",
        "B": "un alfil",
        "N": "un caballo",
    }.get(san[0], "un peón")
    if san in {"O-O", "O-O-O"}:
        return "Es un enroque."
    return f"Mueve {piece}."
