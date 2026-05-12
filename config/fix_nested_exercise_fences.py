#!/usr/bin/env python3
"""Use longer fences for exercise admonitions containing nested colon fences."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


EXERCISE_RE = re.compile(r"^:{3,}\{admonition\}\s+(Task\b.*|Challenge\b.*)$")
COLON_DIRECTIVE_RE = re.compile(r"^:{3,}\{")
BACKTICK_FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^(#{1,6})\s+")


def protected_backtick_lines(lines: list[str]) -> list[bool]:
    """Return True for lines inside fenced code blocks."""
    protected: list[bool] = []
    in_fence = False
    fence_marker = ""

    for line in lines:
        match = BACKTICK_FENCE_RE.match(line)
        protected.append(in_fence)
        if match and not in_fence:
            in_fence = True
            fence_marker = match.group(1)[0]
        elif match and in_fence and match.group(1).startswith(fence_marker * 3):
            in_fence = False

    return protected


def is_exercise_start(lines: list[str], protected: list[bool], index: int) -> bool:
    return (
        not protected[index]
        and EXERCISE_RE.match(lines[index]) is not None
        and index + 1 < len(lines)
        and lines[index + 1].strip() == ":class: exercise"
    )


def next_heading_index(lines: list[str], protected: list[bool], start: int) -> int:
    for i in range(start + 1, len(lines)):
        if not protected[i] and HEADING_RE.match(lines[i]):
            return i
    return len(lines)


def exercise_has_nested_fence(lines: list[str], start: int, end: int) -> bool:
    return any(COLON_DIRECTIVE_RE.match(line.strip()) for line in lines[start + 2 : end])


def last_plain_close_before(lines: list[str], start: int, end: int) -> int | None:
    for i in range(end - 1, start, -1):
        if lines[i].strip() in {":::", "::::"}:
            return i
    return None


def first_plain_close_between(lines: list[str], start: int, end: int) -> int | None:
    for i in range(start, end):
        if lines[i].strip() in {":::", "::::", ":::::"}:
            return i
    return None


def convert_text(text: str) -> str:
    lines = text.splitlines()
    protected = protected_backtick_lines(lines)
    exercise_starts = [
        i for i in range(len(lines)) if is_exercise_start(lines, protected, i)
    ]

    for position in range(len(exercise_starts) - 1, -1, -1):
        i = exercise_starts[position]
        next_exercise = (
            exercise_starts[position + 1]
            if position + 1 < len(exercise_starts)
            else len(lines)
        )
        end_boundary = min(next_exercise, next_heading_index(lines, protected, i))

        close = last_plain_close_before(lines, i, end_boundary)
        if close is None:
            stale_close = first_plain_close_between(lines, end_boundary, next_exercise)
            if stale_close is not None:
                lines.pop(stale_close)
            lines.insert(end_boundary, ":::")
            close = end_boundary

        for inner_close in range(i + 1, close):
            if lines[inner_close].strip() in {":::", "::::", ":::::"}:
                lines[inner_close] = ":::"

        needs_long_fence = exercise_has_nested_fence(lines, i, close)
        title = re.sub(r"^:{3,}", "", lines[i])
        if needs_long_fence:
            lines[i] = f"::::{title}"
            lines[close] = "::::"
        else:
            lines[i] = f":::{title}"
            lines[close] = ":::"

    return "\n".join(lines).rstrip() + "\n"


def convert_file(path: Path) -> bool:
    original = path.read_text()
    converted = convert_text(original)
    if converted == original:
        return False
    path.write_text(converted)
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    files: list[Path] = []
    for path in args.paths:
        if path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
        elif path.suffix == ".md":
            files.append(path)

    for file in files:
        if convert_file(file):
            print(file)


if __name__ == "__main__":
    main()
