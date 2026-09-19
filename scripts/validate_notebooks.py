#!/usr/bin/env python3
"""Validate the public notebooks without executing data-dependent cells."""

from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "notebooks"


def python_source(cell_source: str) -> str:
    lines = []
    for line in cell_source.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("!", "%")):
            continue
        lines.append(line)
    return "\n".join(lines)


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    with path.open("r", encoding="utf-8") as handle:
        notebook = json.load(handle)

    if notebook.get("nbformat") != 4:
        errors.append("expected nbformat 4")

    for index, cell in enumerate(notebook.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        if cell.get("outputs"):
            errors.append(f"cell {index} contains stored output")
        if cell.get("execution_count") is not None:
            errors.append(f"cell {index} has an execution count")

        source = python_source("".join(cell.get("source", [])))
        try:
            ast.parse(source, filename=f"{path.name}:cell-{index}")
        except SyntaxError as exc:
            errors.append(f"cell {index} syntax error: {exc.msg}")

    return errors


def main() -> None:
    failures = []
    for path in sorted(NOTEBOOK_DIR.glob("*.ipynb")):
        errors = validate(path)
        if errors:
            failures.extend(f"{path.name}: {error}" for error in errors)
        else:
            print(f"OK: {path.relative_to(ROOT)}")

    if failures:
        raise SystemExit("\n".join(failures))


if __name__ == "__main__":
    main()
