"""JSONL loading and validation for BioCausalCalib benchmark items."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from biocausalcalib.schemas import Item


class JsonlValidationError(ValueError):
    """Raised when a JSONL benchmark file cannot be parsed or validated."""

    def __init__(self, path: Path, line_number: int, message: str) -> None:
        self.path = path
        self.line_number = line_number
        self.message = message
        super().__init__(f"{path}:{line_number}: {message}")


def load_items(path: str | Path) -> list[Item]:
    """Load and validate benchmark items from a JSONL file."""

    item_path = Path(path)
    items: list[Item] = []

    with item_path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                raise JsonlValidationError(
                    item_path,
                    line_number,
                    "blank lines are not valid JSONL items",
                )

            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                raise JsonlValidationError(
                    item_path,
                    line_number,
                    f"malformed JSON: {exc.msg}",
                ) from exc

            try:
                items.append(Item.model_validate(payload))
            except ValidationError as exc:
                raise JsonlValidationError(
                    item_path,
                    line_number,
                    f"schema validation failed: {_format_validation_error(exc)}",
                ) from exc

    return items


def _format_validation_error(exc: ValidationError) -> str:
    parts: list[str] = []
    for error in exc.errors():
        location = ".".join(str(part) for part in error["loc"]) or "<root>"
        parts.append(f"{location}: {error['msg']}")
    return "; ".join(parts)
