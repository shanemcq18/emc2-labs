#!/usr/bin/env python3
"""Wrap task-like Markdown sections in MyST exercise admonitions."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TASK_HEADING_RE = re.compile(r"^(#{2,6})\s+((?:Task\b|Challenge\b).*)$")
ANY_HEADING_RE = re.compile(r"^(#{1,6})\s+")


def convert_text(text: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    open_level: int | None = None

    for line in lines:
        heading = ANY_HEADING_RE.match(line)
        if open_level is not None and heading and len(heading.group(1)) <= open_level:
            if output and output[-1] != "":
                output.append("")
            output.append(":::")
            output.append("")
            open_level = None

        task_heading = TASK_HEADING_RE.match(line)
        if task_heading:
            open_level = len(task_heading.group(1))
            output.append(f":::{{admonition}} {task_heading.group(2).strip()}")
            output.append(":class: exercise")
            output.append("")
            continue

        output.append(line)

    if open_level is not None:
        if output and output[-1] != "":
            output.append("")
        output.append(":::")

    return "\n".join(output).rstrip() + "\n"


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
