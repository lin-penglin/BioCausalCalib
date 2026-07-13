import json
from pathlib import Path

import pytest

from biocausalcalib.loader import JsonlValidationError, load_items

ROOT = Path(__file__).resolve().parents[1]
SEED_PATH = ROOT / "data" / "biocausalcalib_v0_seed.jsonl"


def first_seed_payload() -> dict[str, object]:
    return json.loads(SEED_PATH.read_text(encoding="utf-8").splitlines()[0])


def write_jsonl(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload) + "\n", encoding="utf-8")


def test_loader_accepts_seed_items() -> None:
    items = load_items(SEED_PATH)

    assert len(items) == 5
    assert items[0].id == "rwe-hrt-chd-001"
    assert items[-1].id == "gen-drugtarget-mr-005"


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("item_type", "case_study", "item_type"),
        ("evidence_domain", "omics_functional", "evidence_domain"),
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
    payload = first_seed_payload()
    payload[field] = value
    broken_path = tmp_path / "broken.jsonl"
    write_jsonl(broken_path, payload)

    with pytest.raises(JsonlValidationError, match=message):
        load_items(broken_path)


def test_loader_rejects_strength_outside_adjudication_range(tmp_path: Path) -> None:
    payload = first_seed_payload()
    payload["warranted_strength"] = 1
    payload["adjudication_range"] = [2, 3]
    broken_path = tmp_path / "range.jsonl"
    write_jsonl(broken_path, payload)

    with pytest.raises(JsonlValidationError, match="outside"):
        load_items(broken_path)


def test_loader_rejects_unknown_fallacy_type(tmp_path: Path) -> None:
    payload = first_seed_payload()
    payload["planted_fallacies"][0]["type"] = "not_a_real_fallacy"
    broken_path = tmp_path / "fallacy.jsonl"
    write_jsonl(broken_path, payload)

    with pytest.raises(JsonlValidationError, match="unknown fallacy type"):
        load_items(broken_path)


def test_loader_rejects_missing_required_field(tmp_path: Path) -> None:
    payload = first_seed_payload()
    payload.pop("planted_fallacies")
    broken_path = tmp_path / "missing.jsonl"
    write_jsonl(broken_path, payload)

    with pytest.raises(JsonlValidationError, match="planted_fallacies"):
        load_items(broken_path)


def test_loader_rejects_malformed_json(tmp_path: Path) -> None:
    broken_path = tmp_path / "bad-json.jsonl"
    broken_path.write_text('{"id": "bad"\n', encoding="utf-8")

    with pytest.raises(JsonlValidationError, match="malformed JSON"):
        load_items(broken_path)
