#!/usr/bin/env python3
"""Convert the EMC2 lab subset of RST into MyST Markdown.

This is intentionally conservative: it preserves Sphinx-only constructs as
MyST directives when a direct Markdown equivalent would lose information.
"""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


UNDERLINE_CHARS = set("=-~^\"`:#*+")


def leading_spaces(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def is_underline(line: str) -> bool:
    stripped = line.strip()
    return (
        len(stripped) >= 3
        and len(set(stripped)) == 1
        and stripped[0] in UNDERLINE_CHARS
    )


def dedent_block(lines: list[str]) -> list[str]:
    nonblank = [leading_spaces(line) for line in lines if line.strip()]
    if not nonblank:
        return ["" for _ in lines]
    amount = min(nonblank)
    return [line[amount:] if len(line) >= amount else "" for line in lines]


def collect_indented(lines: list[str], start: int, parent_indent: int) -> tuple[list[str], int]:
    block: list[str] = []
    i = start
    while i < len(lines):
        line = lines[i]
        if line.strip() and leading_spaces(line) <= parent_indent:
            break
        block.append(line)
        i += 1
    return dedent_block(block), i


def collect_quote_block(lines: list[str], start: int, block_indent: int) -> tuple[list[str], int]:
    block: list[str] = []
    i = start
    while i < len(lines):
        line = lines[i]
        if line.strip() and leading_spaces(line) < block_indent:
            break
        block.append(line)
        i += 1
    return [line[block_indent:] if len(line) >= block_indent else "" for line in block], i


def split_options(lines: list[str]) -> tuple[list[str], list[str]]:
    options: list[str] = []
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped:
            options.append("")
            i += 1
            continue
        if re.match(r"^:[A-Za-z0-9_-]+:(\s|$)", stripped):
            options.append(stripped)
            i += 1
            continue
        break
    while options and not options[-1]:
        options.pop()
    return options, lines[i:]


def protect_math_spans(text: str) -> tuple[str, list[str]]:
    spans: list[str] = []

    def replace(match: re.Match[str]) -> str:
        spans.append(match.group(0))
        return f"\u0000MATH{len(spans) - 1}\u0000"

    return re.sub(r"\$[^$\n]+\$", replace, text), spans


def restore_math_spans(text: str, spans: list[str]) -> str:
    for i, span in enumerate(spans):
        text = text.replace(f"\u0000MATH{i}\u0000", span)
    return text


def protect_code_spans(text: str) -> tuple[str, list[str]]:
    spans: list[str] = []

    def replace(match: re.Match[str]) -> str:
        spans.append(match.group(0))
        return f"\u0000CODE{len(spans) - 1}\u0000"

    return re.sub(r"`[^`\n]+`", replace, text), spans


def restore_code_spans(text: str, spans: list[str]) -> str:
    for i, span in enumerate(spans):
        text = text.replace(f"\u0000CODE{i}\u0000", span)
    return text


def convert_inline(text: str, targets: dict[str, str]) -> str:
    text = text.replace(":math:numref:", ":numref:")
    text = re.sub(r":math:`([^`]+)`", lambda m: f"${m.group(1)}$", text)
    text = re.sub(r":(doc|ref|numref):`([^`]+)`", lambda m: f"{{{m.group(1)}}}`{m.group(2)}`", text)
    def replace_inline_link(match: re.Match[str]) -> str:
        label = match.group(1)
        url = match.group(2)
        if url.endswith(".html") and not re.match(r"^[a-z]+://", url):
            url = f"{url[:-5]}.md"
        return f"[{label}]({url})"

    text = re.sub(r"`([^`<>]+)\s+<([^<>]+)>`_", replace_inline_link, text)
    text = re.sub(r"`<([^<>]+)>`_", lambda m: f"<{m.group(1)}>", text)

    def replace_ref(match: re.Match[str]) -> str:
        label = match.group(1)
        url = targets.get(label)
        return f"[{label}]({url})" if url else match.group(0)

    text = re.sub(r"`([^`]+)`_", replace_ref, text)
    text = re.sub(r"``([^`]+)``", lambda m: f"`{m.group(1)}`", text)

    protected, math_spans = protect_math_spans(text)
    protected, code_spans = protect_code_spans(protected)
    protected = re.sub(r"\\([,.;:!?])", r"\1", protected)
    protected = re.sub(r"\\([A-Za-z])", r"\1", protected)
    protected = protected.replace(r"\ ", " ")
    protected = restore_code_spans(protected, code_spans)
    return restore_math_spans(protected, math_spans)


def code_language(options: list[str], argument: str) -> str:
    if argument:
        return argument.strip()
    for option in options:
        if option.startswith(":class:") and "console" in option:
            return "console"
    return ""


def infer_code_language(lines: list[str]) -> str:
    joined = "\n".join(lines)
    if ">>>" in joined or re.search(r"\b(import|def|class|return|print)\b", joined):
        return "python"
    return "text"


def convert_directive(
    name: str,
    argument: str,
    block: list[str],
    targets: dict[str, str],
    heading_levels: dict[tuple[str, str], int],
) -> list[str]:
    lower = name.lower()
    options, body = split_options(block)
    body = body[1:] if body and not body[0].strip() else body
    output: list[str] = []

    if lower in {"note", "warning", "hint", "important"}:
        output.append(f":::{{{lower}}}")
        converted = convert_lines(body, targets, heading_levels)
        output.extend(converted)
        output.append(":::")
        return output

    if lower == "admonition":
        title = convert_inline(argument.strip(), targets)
        output.append(f":::{{admonition}} {title}".rstrip())
        output.extend(convert_lines(body, targets, heading_levels))
        output.append(":::")
        return output

    if lower in {"code", "code-block"}:
        lang = code_language(options, argument)
        while body and not body[-1].strip():
            body.pop()
        output.append(f"```{lang}".rstrip())
        output.extend(body)
        output.append("```")
        return output

    if lower == "math":
        if argument.strip():
            body = [argument.strip(), *body]
        while body and not body[-1].strip():
            body.pop()
        label = None
        remaining_options = []
        for option in options:
            if option.startswith(":label:"):
                label = option.removeprefix(":label:").strip()
            else:
                remaining_options.append(option)
        if label:
            output.append(f"({label})=")
        output.append("```{math}")
        output.extend(remaining_options)
        if remaining_options and body:
            output.append("")
        output.extend(body)
        output.append("```")
        return output

    if lower == "raw":
        output.append(f"```{{raw}} {argument.strip()}".rstrip())
        output.extend(body)
        output.append("```")
        return output

    if lower in {"image", "figure", "toctree", "list-table", "csv-table"}:
        if lower == "toctree" and not any(line.strip() for line in body):
            return []
        first_line = f"```{{{lower}}}"
        if argument.strip():
            first_line += f" {argument.strip()}"
        output.append(first_line)
        output.extend(options)
        if options and body:
            output.append("")
        if lower in {"figure", "list-table", "csv-table"}:
            output.extend([convert_inline(line, targets) for line in body])
        elif lower == "toctree":
            output.extend(body)
        else:
            output.extend(body)
        output.append("```")
        return output

    output.append(f"```{{{lower}}} {argument.strip()}".rstrip())
    output.extend(options)
    if options and body:
        output.append("")
    output.extend(body)
    output.append("```")
    return output


def collect_doctest(lines: list[str], start: int) -> tuple[list[str], int]:
    block: list[str] = []
    i = start
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            break
        if is_underline(line):
            break
        if re.match(r"^\s*\.\. [A-Za-z0-9_-]+::", line):
            break
        block.append(stripped)
        i += 1
    return block, i


def literal_block_after(lines: list[str], start: int, parent_indent: int) -> tuple[list[str], int]:
    i = start
    spacer: list[str] = []
    while i < len(lines) and not lines[i].strip():
        spacer.append(lines[i])
        i += 1
    if i >= len(lines) or leading_spaces(lines[i]) <= parent_indent:
        return [], start
    block, end = collect_indented(lines, i, parent_indent)
    return spacer + block, end


def heading_level(key: tuple[str, str], heading_levels: dict[tuple[str, str], int]) -> int:
    if key not in heading_levels:
        heading_levels[key] = len(heading_levels) + 1
    return min(heading_levels[key], 6)


def convert_lines(
    lines: list[str],
    targets: dict[str, str],
    heading_levels: dict[tuple[str, str], int],
) -> list[str]:
    output: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        indent = leading_spaces(line)

        if not stripped:
            output.append("")
            i += 1
            continue

        if i + 2 < len(lines) and is_underline(line) and lines[i + 1].strip() and lines[i + 2].strip() == stripped:
            level = heading_level((stripped[0], "over"), heading_levels)
            output.append(f"{'#' * level} {convert_inline(lines[i + 1].strip(), targets)}")
            i += 3
            continue

        if i + 1 < len(lines) and lines[i + 1].strip() and is_underline(lines[i + 1]):
            level = heading_level((lines[i + 1].strip()[0], "under"), heading_levels)
            output.append(f"{'#' * level} {convert_inline(stripped, targets)}")
            i += 2
            continue

        directive = re.match(r"^(\s*)\.\. ([A-Za-z0-9_-]+)::\s*(.*)$", line)
        if directive:
            block, end = collect_indented(lines, i + 1, indent)
            output.extend(
                convert_directive(
                    directive.group(2),
                    directive.group(3),
                    block,
                    targets,
                    heading_levels,
                )
            )
            i = end
            continue

        target = re.match(r"^\s*\.\. _([^:]+):\s*(.*)$", line)
        if target:
            label = target.group(1).strip()
            url = target.group(2).strip()
            if not url:
                output.append(f"({label})=")
            i += 1
            continue

        if stripped.startswith(".. "):
            i += 1
            while i < len(lines) and (not lines[i].strip() or leading_spaces(lines[i]) > indent):
                i += 1
            continue

        if stripped.startswith(">>>"):
            block, end = collect_doctest(lines, i)
            output.append("```python")
            output.extend(block)
            output.append("```")
            i = end
            continue

        if stripped.endswith("::"):
            block, end = literal_block_after(lines, i + 1, indent)
            if block:
                text = stripped[:-1] if stripped != "::" else ""
                if text:
                    output.append(convert_inline(text, targets))
                    output.append("")
                lang = infer_code_language(block)
                output.append(f"```{lang}")
                output.extend([line for line in block if line.strip()])
                output.append("```")
                i = end
                continue

        if indent > 0:
            block, end = collect_quote_block(lines, i, indent)
            converted = convert_lines(block, targets, heading_levels)
            for converted_line in converted:
                output.append(f"> {converted_line}" if converted_line else ">")
            i = end
            continue

        output.append(convert_inline(line.rstrip(), targets))
        i += 1

    while output and output[-1] == "":
        output.pop()
    return output


def collect_targets(text: str) -> dict[str, str]:
    targets: dict[str, str] = {}
    for match in re.finditer(r"^\s*\.\. _([^:]+):\s*(\S+)\s*$", text, re.MULTILINE):
        targets[match.group(1).strip()] = match.group(2).strip()
    return targets


def convert_text(text: str) -> str:
    text = text.expandtabs(4)
    lines = text.splitlines()
    targets = collect_targets(text)
    return "\n".join(convert_lines(lines, targets, {})) + "\n"


def convert_file(path: Path, keep_rst: bool, text: str | None = None) -> Path:
    if text is None:
        text = path.read_text()
    markdown = convert_text(text)
    output_path = path.with_suffix(".md")
    output_path.write_text(markdown)
    if not keep_rst and path.exists():
        path.unlink()
    return output_path


def git_repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    )
    return Path(result.stdout.strip())


def git_head_rst_files(paths: list[Path]) -> list[Path]:
    root = git_repo_root()
    files: list[Path] = []
    for path in paths:
        rel = path if not path.is_absolute() else path.relative_to(root)
        result = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", "HEAD", "--", str(rel)],
            check=True,
            capture_output=True,
            text=True,
        )
        for line in result.stdout.splitlines():
            if line.endswith(".rst"):
                files.append(root / line)
    return sorted(dict.fromkeys(files))


def git_head_text(path: Path) -> str:
    root = git_repo_root()
    rel = path if not path.is_absolute() else path.relative_to(root)
    result = subprocess.run(
        ["git", "show", f"HEAD:{rel}"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--keep-rst", action="store_true")
    parser.add_argument("--from-git-head", action="store_true")
    args = parser.parse_args()

    if args.from_git_head:
        rst_files = git_head_rst_files(args.paths)
    else:
        rst_files: list[Path] = []
        for path in args.paths:
            if path.is_dir():
                rst_files.extend(sorted(path.rglob("*.rst")))
            elif path.suffix == ".rst":
                rst_files.append(path)

    for rst_file in rst_files:
        text = git_head_text(rst_file) if args.from_git_head else None
        output_path = convert_file(rst_file, args.keep_rst, text)
        print(f"{rst_file} -> {output_path}")


if __name__ == "__main__":
    main()
