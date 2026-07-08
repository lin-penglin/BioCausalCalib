"""Pydantic schemas for BioCausalCalib benchmark items and model outputs."""

from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, conint, model_validator

ItemType = Literal["anchored", "probe"]
EvidenceDomain = Literal[
    "statistical_genetics",
    "omics_functional",
    "rwe_heor",
    "evolution",
    "cross_scale",
]
BiologicalLevel = Literal[
    "sequence",
    "variant",
    "gene",
    "transcript",
    "protein",
    "pathway",
    "cell_state",
    "tissue",
    "organ_system",
    "organism_phenotype",
    "population_outcome",
    "evolutionary_fitness",
    "clinical_outcome",
    "real_world_outcome",
]

Strength = conint(strict=True, ge=0, le=4)


class StrictModel(BaseModel):
    """Base model that rejects fields outside the benchmark contract."""

    model_config = ConfigDict(extra="forbid")


class ExpectedPoint(StrictModel):
    id: str
    point: str
    required: bool


class Resolution(StrictModel):
    resolved: bool
    description: str
    citation: str


class Item(StrictModel):
    id: str
    item_type: ItemType
    evidence_domain: EvidenceDomain
    biological_levels: list[BiologicalLevel]
    evidence_vignette: str
    proposed_claim: str
    question: str
    warranted_strength: Strength
    adjudication_range: tuple[Strength, Strength] | None = None
    overclaim_types: list[str]
    expected_reasoning_points: list[ExpectedPoint]
    ideal_cautious_answer: str
    common_failure_modes: list[str]
    resolution: Resolution
    notes: str | None = None

    @model_validator(mode="after")
    def validate_adjudication_range_order(self) -> Self:
        if self.adjudication_range is None:
            return self

        lo, hi = self.adjudication_range
        if lo > hi:
            raise ValueError("adjudication_range must satisfy lo <= hi")
        return self


class ModelOutput(StrictModel):
    predicted_strength: Strength
    identified_issues: list[str]
    missing_evidence: list[str]
    cautious_restatement: str
    confidence: float = Field(ge=0, le=1)
