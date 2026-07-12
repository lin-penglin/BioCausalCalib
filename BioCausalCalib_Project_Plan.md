# BioCausalCalib — Project Plan & Benchmark Design (v0, solo scope)

*A benchmark for measuring whether large language models overclaim causal certainty from biomedical evidence.*

**Status:** design v0.2. Supersedes the earlier five-track, 60-item, second-rater-dependent draft. This version is scoped to be **completed by one person, alone, with defensible ground truth.**

Source of truth for the repo. Read this before writing code (see `AGENTS.md`) or authoring items.

---

## 1. Summary

BioCausalCalib measures one thing: **when an AI model is given biomedical evidence and a proposed causal claim, does it overclaim?**

Each item is a short **evidence vignette** plus a **proposed claim**. The model must state the strongest level of causal certainty the evidence supports (0–4), identify the biases and evidence gaps that undermine the claim, and restate the claim cautiously. We score its judgment against expert-authored labels.

**v0 is deliberately small and hard to attack:** ~34 items across two tracks (RWE/HEOR and statistical genetics), where the primary metric is *objective by construction* and the labels are *derived from published evidence frameworks* rather than from one person's opinion.

BioCausalCalib is the first publishable component of the longer-term **EvoReasoner** program (evolution-grounded biological reasoning across scales). EvoReasoner is the research program; this is the first finishable brick.

---

## 2. Central question & positioning

**Central question:** *Do frontier AI models assign the right level of causal certainty to biomedical evidence, or do they systematically overclaim — and where?*

**Capability vs. calibration.** Most biomedical AI benchmarks measure *capability*: can the model do the analysis and reach the right biological answer? Anthropic's BioMysteryBench (99 expert-authored bioinformatics tasks graded on final-answer correctness) is a capability benchmark, as are BixBench and BLADE. BioCausalCalib measures something orthogonal — *calibration*: does the model know how confident it is entitled to be, and does it recognize when evidence does **not** license a causal claim?

> BioMysteryBench asks whether a model can find the right biological answer. BioCausalCalib asks whether the model knows *how strong* its causal claim is entitled to be, and where it overclaims.

There is a bridge worth citing: BioMysteryBench reported that on hard tasks models produced "brittle" wins, and when uncertain would run several methods and pick the answer they converged on — sometimes the wrong one. That is an epistemic-reliability failure. It is this project's subject.

**The open gap.** General causal-reasoning benchmarks are crowded (CLadder, CausalBench, CaLM, CauSciBench). Genetics-specific LLM automation exists (MRAgent). What does not exist is a calibration benchmark covering **pharmacoepidemiological observational biases** — confounding by indication, immortal-time bias, healthy-user bias — alongside genetic-evidence interpretation. That is the wedge.

**What this is NOT:** not a medical chatbot, not clinical decision support, not an MR-automation agent. It makes no patient-level recommendations, and its write-up holds itself to the same standard of caution it measures.

---

## 3. How a solo project gets defensible ground truth

The obvious attack on any expert-authored benchmark is: *"How do you know your labels are right, and not just your opinion?"* With one author and no second rater, that attack is fatal unless the design answers it structurally. Three moves do:

### Move 1 — Plant the flaw; don't rate the evidence

We are not *finding* vignettes in the wild and judging them. We are **constructing** them. If the vignette is written so that survival is measured from diagnosis while treatment can only be received by survivors, then **immortal-time bias is present as a fact of construction, not as a matter of opinion.**

So the primary metric is not "did the model guess my strength label?" but:

> **Did the model detect the flaw that was deliberately planted?**

This is ground truth by construction — the same logic as injecting a known bug to test a linter. It requires the author to *know a bias well enough to build it*, not to adjudicate subtle gradations of evidence quality. Detection is scored as a standard **precision / recall / F1** problem against the planted set.

### Move 2 — Derive labels from published frameworks, not from opinion

The 0–4 strength label is still useful, but it is never asserted bare. Every item carries a `label_derivation` field naming the framework and the rule applied:

| Framework | Used for |
|---|---|
| **GRADE** | Certainty of evidence; explicit downgrading (risk of bias, indirectness, imprecision) and upgrading (large effect, dose–response) rules. Observational evidence starts low. |
| **Target trial emulation** (Hernán & Robins) | Whether an observational analysis is causally interpretable — especially time-zero alignment. |
| **STROBE-MR** | Which assumptions an MR analysis must address and report. |
| **ACMG/AMP** | Variant-pathogenicity evidence ladder (for the parked evolution track). |

The label is now a **derivation a reviewer can check**, not a vote. "Under GRADE, observational evidence begins at low certainty; serious risk of bias from healthy-user selection applies; the large-effect upgrade is blocked because plausible residual confounding runs in the direction of the observed effect — therefore level 1." That is stronger than one colleague's opinion.

### Move 3 — Report metrics that need no labels at all

Two headline findings require zero ground truth:

- **Self-consistency:** the same model, the same item, k runs — does it give the same answer? A model that overclaims in 2 of 5 runs is unreliable regardless of who is right.
- **Cross-model disagreement:** do four models agree on the warranted strength? Wide disagreement on an item is itself a result.

These are free, fully objective, and genuinely interesting.

**On the second rater.** Independent adjudication is still the gold standard. It is not achievable now, and blocking on it would kill the project. So: **v0 ships single-rater, with the limitation stated plainly**, and external co-labeling becomes an open-source invitation (`CONTRIBUTING.md`: co-label 10 items, get acknowledged). Inter-rater kappa is reported in v1.1 when a collaborator appears. This is how open benchmarks normally grow, and it is disclosed rather than hidden.

---

## 4. Scope: two tracks, ~34 items

A benchmark with shaky labels in a domain the author cannot defend cold is *worse than one that omits the domain*. Omics, single-cell, and evolution are therefore **parked** (retained in `data/parked_items.jsonl` for EvoReasoner v1+, not shipped in v0).

| Track | Items | Rationale |
|---|---|---|
| **RWE / HEOR** | 20 | Current professional expertise; the clearest open niche in the eval landscape. |
| **Statistical genetics** | 14 | Durable epistemics (LD, colocalization, pleiotropy, ancestry transfer) that do not require method-frontier currency. |
| **Total** | **34** | |

**RWE/HEOR breakdown (20):** confounding by indication ×4, immortal-time bias ×3, healthy-user bias ×2, selection/collider bias ×3, outcome misclassification ×2, prevalent-user bias ×2, competing risks ×1, surrogate→outcome ×1, cost→value overclaim ×2.

**Statistical genetics breakdown (14):** GWAS→causality ×3, eQTL/colocalization ×4, MR/IV assumptions ×4, PRS/ancestry ×3. Cross-scale *compounding* is tested **within** the genetics track (genetic evidence → therapeutic claim), so no omics or animal-model judgment is required.

---

## 5. Task format

The model sees exactly three fields: **evidence vignette**, **proposed claim**, **question** (fixed). It never sees the labels, the planted fallacies, or the distractors.

It returns a structured judgment (Section 8).

---

## 6. Warranted Causal Strength scale (0–4)

| Level | Label | Justified by | Warranted language |
|---|---|---|---|
| 0 | Unsupported / invalid | No valid empirical link — hypothesis only, or a design so flawed it supports no inference. | "hypothesized", "the design does not support inference" |
| 1 | Association only | Robust association, no design ruling out confounding or reverse causation. | "is associated with" |
| 2 | Mechanistic plausibility | Association + plausible mechanism or convergent correlative evidence; **no valid causal design**, or a causal design whose assumptions are untested. | "may contribute to", "is consistent with", "supports the hypothesis" |
| 3 | Causal evidence with important assumptions | A causal-inference design supports the effect, with assumptions addressed but potentially violable (MR with multiple instruments + sensitivity analyses; well-executed target-trial emulation). | "provides evidence for a causal effect, contingent on [assumptions]" |
| 4 | Strong causal / interventional | Converging causal evidence including interventional data (RCT; triangulation across MR + perturbation + trial). | "causes", "is an established causal factor" |

**Assignment procedure:** (1) identify the strongest *design* present; (2) apply the relevant framework's downgrading rules for unaddressed threats; (3) record the derivation in `label_derivation`; (4) if a defensible range exists, record `adjudication_range` rather than feigning precision.

---

## 7. Planted-fallacy taxonomy (v0, two tracks)

Each planted fallacy is either a **commission** (a flaw actively built into the design) or an **omission** (a required piece of evidence deliberately withheld). Both are facts of construction.

### 7.1 RWE / HEOR
- **confounding_by_indication** — treatment allocation driven by prognosis/severity.
- **healthy_user_bias** — exposure is self-selected by healthier, more health-engaged people.
- **immortal_time_bias** — follow-up starts before treatment assignment, so a guaranteed event-free window is credited to treatment.
- **selection_bias / collider** — conditioning on a collider induces a spurious association.
- **outcome_misclassification** — differential or non-differential misclassification in claims/EHR data.
- **prevalent_user_bias** — prevalent rather than new users; early events missed, susceptibles depleted.
- **competing_risks_ignored** — competing events (e.g., death) ignored in cause-specific estimation.
- **surrogate_to_outcome** — a surrogate/biomarker change treated as clinical benefit.
- **residual_confounding** — adjustment for measured covariates treated as sufficient.
- **observational_treatment_effect** — an observational association read as a causal treatment effect.
- **population_to_individual_recommendation** — a population-level association read as an individual prescribing recommendation.
- **cost_to_value_overclaim** — a cost or resource-use difference read as evidence of value without a full economic model.

### 7.2 Statistical genetics
- **GWAS_to_causality** — a lead SNP treated as causal; ignores LD and the need for fine-mapping.
- **colocalization_missing** — a shared top SNP treated as a shared causal variant without formal colocalization.
- **eQTL_to_causal_gene** — an eQTL gene assumed causal; ignores multi-gene regulation.
- **tissue_mismatch** — an eQTL in one tissue (e.g., whole blood) assumed to operate in the disease-relevant tissue.
- **MR_assumption_ignored** — IV assumptions (relevance, independence, exclusion restriction) assumed rather than interrogated.
- **pleiotropy_ignored** — horizontal pleiotropy not considered as an alternative explanation.
- **weak_instrument_bias** — low-strength instruments bias MR toward the confounded estimate.
- **winners_curse** — instrument selection and effect estimation in the same sample.
- **ancestry_generalization** — findings/instruments assumed to transfer across ancestries with different LD structure.
- **PRS_individual_prediction** — a population-level PRS association read as accurate individual prediction or clinical actionability.
- **lifelong_exposure_vs_intervention** — an MR estimate of lifelong exposure differences read as predicting a drug effect.
- **target_validation_overclaim** — "therapeutic target" claimed without direction-of-effect, perturbational, and clinical evidence.
- **reverse_causation** — direction of effect assumed rather than established.
- **cross_scale_compounding** — chained links each carrying an untested assumption; overall confidence must be *lower* than any single link.

### 7.3 Distractors (the opposite failure)
Each item lists **distractors**: biases that are clearly *not* present or *not operative*. Flagging one is a **false positive**. This makes over-hedging measurable — a model that sprays fallacy labels indiscriminately scores badly on precision even if its recall is high. (E.g., a genetics item lists `immortal_time_bias` and `healthy_user_bias` as distractors.)

---

## 8. Schemas

### Item (JSONL, one object per line) — see `data/biocausalcalib_v0_seed.jsonl`

```json
{
  "id": "rwe-immortal-time-002",
  "item_type": "probe",                       // "anchored" | "probe"
  "evidence_domain": "rwe_heor",              // "rwe_heor" | "statistical_genetics"
  "evidence_vignette": "…shown to the model…",
  "proposed_claim": "…shown to the model…",
  "question": "…fixed instruction, shown to the model…",

  "planted_fallacies": [                      // PRIMARY GROUND TRUTH
    {
      "id": "f1",
      "type": "immortal_time_bias",
      "mechanism": "commission",              // "commission" | "omission"
      "planted_as": "Follow-up starts at diagnosis, but a patient can only enter the treated group by surviving to receive treatment.",
      "detection_criteria": "Model identifies guaranteed/immortal survival time inflating the apparent benefit.",
      "remedy": "Landmark analysis or time-varying exposure modelling.",
      "required": true
    }
  ],
  "distractors": [
    {"type": "healthy_user_bias", "why_absent": "Allocation is clinician-driven by prognosis, not patient self-selection."}
  ],

  "warranted_strength": 0,                    // SECONDARY label, 0–4
  "adjudication_range": [0, 1],
  "label_derivation": {
    "framework": "Target trial emulation",
    "rule": "Time zero is not aligned with treatment assignment, so the comparison is not a valid emulation and supports no causal inference.",
    "citation": "Hernán & Robins, Am J Epidemiol 2016; Suissa 2008."
  },

  "ideal_cautious_answer": "…",
  "common_failure_modes": ["…"],
  "resolution": {"resolved": false, "description": "…", "citation": "…"},
  "scoring_notes": "Accept 0 or 1: raters may differ on whether a bias-generated difference counts as an association.",
  "notes": "…"
}
```

`scoring_notes` is where known edge cases are encoded — including cases where a sophisticated model answer should be **credited, not penalized** (see the HRT timing-hypothesis and HDL/REVEAL notes in the seed items).

### Model output (JSON only)

```json
{
  "predicted_strength": 1,
  "identified_issues": ["immortal time: survival counted from diagnosis but treatment requires survival"],
  "missing_evidence": ["landmark or time-varying-exposure analysis"],
  "cautious_restatement": "The comparison is confounded by design; no causal conclusion is supported.",
  "confidence": 0.8
}
```

Raw model output is always stored verbatim alongside the parsed object.

---

## 9. Scoring & metrics

**Primary — planted-fallacy detection (objective).** Match the model's `identified_issues` + `missing_evidence` against `planted_fallacies` using each fallacy's `detection_criteria`, and against `distractors` as explicit negatives. Report:
- **Recall** over planted fallacies (required-weighted), **precision** (penalized by distractor hits and fabrications), and **F1**.
- Recall broken down **by fallacy type** — this is the error analysis that produces the paper's headline.

**Secondary — strength calibration.** Exact match; within-1; and **inside `adjudication_range` counts as correct**. Record the **signed error** (predicted − warranted) so **overclaiming** (positive) is separable from **underclaiming** (negative). *Overclaiming rate is the headline number.*

**Cautious-language appropriateness.** Does `cautious_restatement` use language matching the warranted level (no "proves/causes" at 0–2; no empty hedging at 4)?

**Fabrication penalty.** Penalize evidence invented but not present in the vignette (e.g., asserting colocalization was performed).

**Label-free metrics.**
- **Self-consistency:** agreement across k runs (same model, same item).
- **Cross-model disagreement:** spread of `predicted_strength` across models, per item.

**Reported splits:** by track; by fallacy type; **`anchored` vs `probe`** (the contamination check — the generalization signal lives in `probe` items).

---

## 10. The AI-competence layer (Week 4 — do not cut)

This is what makes the project *research* rather than a well-organized spreadsheet, and it is where the AI/ML skill is demonstrated.

1. **LLM-judge validation.** Hand-score ~20 model outputs. Build an LLM-judge to do the same. **Report judge-vs-human agreement (kappa / correlation).** Auto-grading open-ended reasoning is an unsolved problem; a validated judge is a genuine methods contribution, and it is what makes the benchmark scale.
2. **Calibration analysis.** Reliability curves and expected calibration error (ECE) on the model's `confidence` field. The finding to hunt for: **are models most confident exactly where they overclaim?**
3. **Reasoning-effort ablation.** Same items, extended reasoning on vs. off. If extended reasoning does *not* reduce overclaiming, that is a genuinely interesting negative result.
4. **Mitigation arm.** Neutral prompt vs. caution-primed prompt (supply the 0–4 scale and the fallacy taxonomy in-context). Report the delta. *"I measured a failure mode and reduced it by N points"* is a much stronger result than measurement alone — and the distractor metric guards against the trivial "fix" of hedging everything.

---

## 11. Anchored vs. probe items (contamination)

- **`anchored`** — built on a case the field later resolved, with a citation (HRT/CHD reversed by WHI; HDL/CHD unsupported by MR and HDL-raising trials). Purpose: **validate the scale** against something semi-objective.
- **`probe`** — constructed to isolate specific fallacies, with varied surface details. Purpose: **test whether caution generalizes** rather than being recalled from training data.

Results are always reported split by type.

---

## 12. Model set & running protocol

- **Models:** ≥1 Claude, ≥1 GPT, ≥1 open-weight, plus a reasoning/non-reasoning variant for the ablation.
- **Blinding:** model sees vignette + claim + question only.
- **Reliability:** k = 5 runs per item, temperature 0–0.2.
- **Reproducibility:** fixed prompt (`prompts/model_prompt_v0.md`); raw outputs cached; scoring runs offline from cache with no API calls.

---

## 13. Seed items (5, in `data/biocausalcalib_v0_seed.jsonl`)

| id | track | type | strength | planted fallacies (required) |
|---|---|---|---|---|
| `rwe-hrt-chd-001` | RWE | anchored | 1 | healthy-user bias; observational→causal (+2 optional) |
| `rwe-immortal-time-002` | RWE | probe | 0 [0–1] | immortal time; confounding by indication |
| `gen-eqtl-causalgene-003` | genetics | probe | 2 [1–2] | colocalization missing; LD/GWAS→causality; tissue mismatch; target-validation overclaim |
| `gen-mr-hdl-chd-004` | genetics | anchored | 1 [0–1] | observational→causal; surrogate→outcome |
| `gen-drugtarget-mr-005` | genetics | probe | 2 [2–3] | MR assumptions; pleiotropy; colocalization; tissue; ancestry; lifelong-exposure≠drug; compounding |

Parked (not in v0): `omics-de-driver-005`, `evo-conservation-006`, `xscale-mouse-ko-007` → `data/parked_items.jsonl`.

**Two edge cases the author must verify before these are final** (encoded in `scoring_notes`):
- **HRT:** does the WHI age-stratification / "timing hypothesis" mean a model raising it is being *more* sophisticated rather than overclaiming?
- **HDL:** does REVEAL/anacetrapib's modest event reduction (plausibly via apoB/LDL, not HDL) complicate the clean "HDL is only a marker" framing?

These two decisions set the precedent for every anchored item that follows.

---

## 14. Repo structure

```
biocausalcalib/
  BioCausalCalib_Project_Plan.md   # this document — source of truth
  AGENTS.md                        # rules for coding agents
  README.md
  CONTRIBUTING.md                  # co-labeling invitation (the path to inter-rater kappa)
  data/
    biocausalcalib_v0_seed.jsonl   # 5 worked items
    biocausalcalib_v0.jsonl        # grows to ~34
    parked_items.jsonl             # deferred tracks
  prompts/
    model_prompt_v0.md             # neutral prompt
    model_prompt_primed.md         # caution-primed prompt (mitigation arm)
    judge_prompt_v0.md             # LLM-judge
  biocausalcalib/
    schemas.py  loader.py  runner.py  scorer.py  judge.py  metrics.py  report.py  cli.py
  docs/
    label_guide.md  failure_modes.md  limitations.md
  results/
  tests/
```

---

## 15. Five-week roadmap (solo)

**W1 — Foundations.** Verify the two anchored edge cases (HRT timing; HDL/REVEAL). Blind-label the 5 seed items (assign your own label *before* reading the drafted one; log disagreements). Write `label_guide.md` with the framework derivation rules. Author to **12 items**. *Codex: schemas + loader + `validate` CLI + tests.*
**DoD:** `make test` passes; `validate` accepts the seed file and rejects a deliberately broken item.

**W2 — Scale + harness.** Author to **25 items**. *Codex: runner (provider adapters, mock mode, k-runs), scorer (detection P/R/F1 + strength + fabrication), metrics, report, CLI.* Dry-run one model end-to-end.
**DoD:** `run → score → report` works on the seed file; `make demo` runs offline.

**W3 — Full set + full run.** Reach **34 items**. Finalize every label with a written `label_derivation`. Run 3–4 models × k=5.
**DoD:** complete cached outputs + scored results in `results/`.

**W4 — The AI layer.** Judge validation (hand-score 20 → build judge → report agreement). Calibration curves + ECE. Reasoning-effort ablation. Mitigation arm.
**DoD:** four analyses, four figures.

**W5 — Write-up + release.** Error analysis by track and fallacy type; anchored-vs-probe split; limitations; preprint + repo release; `CONTRIBUTING.md` co-labeling invitation.

**Weekly rhythm:** ~4–6 h/week. Review drafted items (blind-label first), unblock Codex, decide contested labels. **If in a given week you wrote code but labeled no items, that was a bad week** — the code is not the bottleneck and never was.

**If time gets tight, cut in this order:** mitigation arm → ablation → drop to 25 items. **Never cut judge validation or the distractor metric** — those are what separate this from an opinion.

---

## 16. Division of labor

**Author (non-delegable):** vignette construction and fallacy planting; framework-derived labels; verifying anchored resolutions; hand-scoring the judge-validation sample; the analysis and framing.

**Claude:** draft item candidates for review; critique labels; propose framework derivations; review Codex's implementation against this spec; help write the paper.

**Codex:** the harness only — schemas, loader, runner, scorer, judge plumbing, metrics, report, CLI, tests. **Codex must never create, edit, or relabel an item.**

---

## 17. Limitations & ethics

- **Single-rater labels (v0).** Mitigated by (a) planted-fallacy ground truth by construction, (b) framework-derived rather than opinion-derived strength labels, (c) `adjudication_range` for contestable labels, (d) label-free metrics (self-consistency, cross-model disagreement). **Stated plainly, not hidden.** External co-labeling is invited; inter-rater kappa is reported in v1.1.
- **Two tracks only.** Omics/single-cell/evolution are parked rather than shipped with labels the author cannot defend. Narrow and defensible beats broad and shaky.
- **Small N per cell.** Report patterns, not over-precise sub-cell statistics.
- **Contamination.** Anchored items may be recalled rather than reasoned; probe items and the anchored/probe split address this.
- **Constructed vignettes.** Planted fallacies give clean ground truth but may be more legible than real-world evidence; noted explicitly as a validity trade-off.
- **Not medical advice.** No patient-level recommendations.
- **Self-consistency.** The write-up applies the caution it measures.

---

## 18. Beyond v0

- Inter-rater kappa once a co-labeler joins (v1.1).
- Revive the **parked tracks** (omics, single-cell, evolution) with collaborators who can defend those labels.
- Retrieval + citation verification; a public leaderboard; the cross-scale EvoReasoner vision.

EvoReasoner remains the long-term program: AI systems that reason reliably across biological scales while remaining transparent, cautious, and reproducible. BioCausalCalib is the first evidence that such reasoning can be **measured**.

---

## Appendix A — controlled vocabularies (v0)

- `item_type`: `anchored`, `probe`
- `evidence_domain`: `rwe_heor`, `statistical_genetics`  *(parked: `omics_functional`, `evolution`, `cross_scale`)*
- `mechanism`: `commission`, `omission`
- `warranted_strength`: integer 0–4; `adjudication_range`: `[lo, hi]`, `lo ≤ warranted_strength ≤ hi`
- `fallacy type`: the union of the taxonomies in Sections 7.1 and 7.2.
