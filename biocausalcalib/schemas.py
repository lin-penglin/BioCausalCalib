"""Pydantic schemas for BioCausalCalib benchmark items and model outputs.

Contract: ``BioCausalCalib_Project_Plan.md`` (v0.2, planted-fallacy method) and ``AGENTS.md``.

Each vignette has fallacies deliberately **planted**. ``planted_fallacies`` is the primary
ground truth (scored by detection); ``distractors`` are explicit negatives (flagging one is a
false positive). The 0-4 ``warranted_strength`` is a secondary label whose derivation is
recorded in ``label_derivation``.
"""

from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, conint, model_validator

ItemType = Literal["anchored", "probe"]
EvidenceDomain = Literal["rwe_heor", "statistical_genetics"]  # v0 ships two tracks only
Mechanism = Literal["commission", "omission"]

# Fallacy-type controlled vocabulary — plan Sections 7.1 (RWE/HEOR) and 7.2 (genetics),
# loaded as a validated enum per AGENTS.md. Parked-track types are intentionally absent.
FALLACY_TYPES: frozenset[str] = frozenset(
    {
        # 7.1 RWE / HEOR
        "confounding_by_indication",
        "healthy_user_bias",
        "immortal_time_bias",
        "selection_bias",
        "collider",
        "outcome_misclassification",
        "prevalent_user_bias",
        "competing_risks_ignored",
        "surrogate_to_outcome",
        "residual_confounding",
        "observational_treatment_effect",
        "population_to_individual_recommendation",
        "cost_to_value_overclaim",
        # 7.2 statistical genetics
        "GWAS_to_causality",
        "colocalization_missing",
        "eQTL_to_causal_gene",
        "tissue_mismatch",
        "MR_assumption_ignored",
        "pleiotropy_ignored",
        "weak_instrument_bias",
        "winners_curse",
        "ancestry_generalization",
        "PRS_individual_prediction",
        "lifelong_exposure_vs_intervention",
        "target_validation_overclaim",
        "reverse_causation",
        "cross_scale_compounding",
    }
)

Strength = conint(strict=True, ge=0, le=4)


class StrictModel(BaseModel):
    """Base model that rejects fields outside the benchmark contract."""

    model_config = ConfigDict(extra="forbid")


class PlantedFallacy(StrictModel):
    id: str
    type: str
    mechanism: Mechanism
    planted_as: str
    detection_criteria: str
    remedy: str
    required: bool

    @model_validator(mode="after")
    def _known_type(self) -> Self:
        if self.type not in FALLACY_TYPES:
            raise ValueError(f"unknown fallacy type: {self.type!r}")
        return self


class Distractor(StrictModel):
    type: str
    why_absent: str

    @model_validator(mode="after")
    def _known_type(self) -> Self:
        if self.type not in FALLACY_TYPES:
            raise ValueError(f"unknown distractor type: {self.type!r}")
        return self


class LabelDerivation(StrictModel):
    framework: str
    rule: str
    citation: str


class Resolution(StrictModel):
    resolved: bool
    description: str
    citation: str


class Item(StrictModel):
    id: str
    item_type: ItemType
    evidence_domain: EvidenceDomain
    evidence_vignette: str
    proposed_claim: str
    question: str
    planted_fallacies: list[PlantedFallacy]
    distractors: list[Distractor]
    warranted_strength: Strength
    adjudication_range: tuple[Strength, Strength]
    label_derivation: LabelDerivation
    ideal_cautious_answer: str
    common_failure_modes: list[str]
    resolution: Resolution
    scoring_notes: str | None = None
    notes: str | None = None

    @model_validator(mode="after")
    def _check_invariants(self) -> Self:
        if not self.planted_fallacies:
            raise ValueError("planted_fallacies must not be empty")

        fallacy_ids = [pf.id for pf in self.planted_fallacies]
        if len(fallacy_ids) != len(set(fallacy_ids)):
            raise ValueError("planted_fallacies ids must be unique within an item")

        lo, hi = self.adjudication_range
        if lo > hi:
            raise ValueError("adjudication_range must satisfy lo <= hi")
        if not (lo <= self.warranted_strength <= hi):
            raise ValueError(
                f"warranted_strength {self.warranted_strength} is outside "
                f"adjudication_range [{lo}, {hi}]"
            )
        return self


class ModelOutput(StrictModel):
    predicted_strength: Strength
    identified_issues: list[str]
    missing_evidence: list[str]
    cautious_restatement: str
    confidence: float = Field(ge=0, le=1)
