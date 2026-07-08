import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from biocausalcalib.schemas import Item, ModelOutput

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PATH = ROOT / "data" / "sample_items.jsonl"


def first_sample_payload() -> dict[str, object]:
    return json.loads(SAMPLE_PATH.read_text(encoding="utf-8").splitlines()[0])


def test_item_round_trips_valid_sample_item() -> None:
    item = Item.model_validate(first_sample_payload())

    round_tripped = Item.model_validate_json(item.model_dump_json())

    assert round_tripped == item
    assert round_tripped.id == "rwe-hrt-chd-001"


def test_item_rejects_invalid_adjudication_range_order() -> None:
    payload = first_sample_payload()
    payload["adjudication_range"] = [2, 1]

    with pytest.raises(ValidationError, match="adjudication_range"):
        Item.model_validate(payload)


def test_model_output_accepts_valid_response_shape() -> None:
    output = ModelOutput.model_validate(
        {
            "predicted_strength": 2,
            "identified_issues": ["no colocalization shown"],
            "missing_evidence": ["perturbational validation"],
            "cautious_restatement": "The evidence supports a plausible hypothesis only.",
            "confidence": 0.7,
        }
    )

    assert output.predicted_strength == 2
    assert output.confidence == 0.7


def test_model_output_rejects_out_of_range_confidence() -> None:
    with pytest.raises(ValidationError, match="confidence"):
        ModelOutput.model_validate(
            {
                "predicted_strength": 2,
                "identified_issues": [],
                "missing_evidence": [],
                "cautious_restatement": "The claim is not established.",
                "confidence": 1.5,
            }
        )
