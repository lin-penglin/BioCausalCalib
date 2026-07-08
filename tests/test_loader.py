import json
from pathlib import Path

import pytest

from biocausalcalib.loader import JsonlValidationError, load_items

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PATH = ROOT / "data" / "sample_items.jsonl"


def first_sample_payload() -> dict[str, object]:
    return json.loads(SAMPLE_PATH.read_text(encoding="utf-8").splitlines()[0])


def write_jsonl(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload) + "\n", encoding="utf-8")


def test_loader_accepts_sample_items() -> None:
    items = load_items(SAMPLE_PATH)

    assert len(items) == 7
    assert items[0].id == "rwe-hrt-chd-001"
    assert items[-1].id == "xscale-variant-to-treatment-007"


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("item_type", "case_study", "item_type"),
        ("warranted_strength", 5, "warranted_strength"),
        ("adjudication_range", [3, 1], "adjudication_range"),
    ],
)
def test_loader_rejects_bad_values(
    tmp_path: Path,
    field: str,
    value: object,
    message: str,
) -> None:
    payload = first_sample_payload()
    payload[field] = value
    broken_path = tmp_path / "broken.jsonl"
    write_jsonl(broken_path, payload)

    with pytest.raises(JsonlValidationError, match=message):
        load_items(broken_path)


def test_loader_rejects_missing_required_field(tmp_path: Path) -> None:
    payload = first_sample_payload()
    payload.pop("question")
    broken_path = tmp_path / "missing.jsonl"
    write_jsonl(broken_path, payload)

    with pytest.raises(JsonlValidationError, match="question"):
        load_items(broken_path)


def test_loader_rejects_malformed_json(tmp_path: Path) -> None:
    broken_path = tmp_path / "bad-json.jsonl"
    broken_path.write_text('{"id": "bad"\n', encoding="utf-8")

    with pytest.raises(JsonlValidationError, match="malformed JSON"):
        load_items(broken_path)
