# AGENTS.md — working guide for coding agents (Codex, Claude Code)

Governs how automated coding agents work in the BioCausalCalib repository. The authoritative design spec is **`BioCausalCalib_Project_Plan.md`** (v0.2, solo scope). Read it before writing any code.

## What this repo is

BioCausalCalib is a **calibration benchmark**: it measures whether LLMs *overclaim causal certainty* from biomedical evidence. Each item presents an evidence vignette + a proposed claim; the model must judge the warranted causal strength (0–4), identify the biases and evidence gaps, and restate the claim cautiously.

**The key design fact you must understand:** each vignette has fallacies **deliberately planted** in it. The primary metric is *not* whether the model guessed the strength label — it is **whether the model detected the planted fallacies**, scored as precision/recall/F1 against the planted set, with `distractors` as explicit negatives. Ground truth is true *by construction*. Build the scorer around this.

## Golden rules

1. **Content is the source of truth; code serves it.** Items in `data/*.jsonl` are human-authored. Code **must not** create, edit, delete, reorder, or re-label items, and must never change `planted_fallacies`, `distractors`, `warranted_strength`, `adjudication_range`, or `label_derivation`. If a schema change would force a data change, **propose it — do not silently rewrite data.**
2. **Authoring is out of scope for coding agents.** Your scope is the harness: schemas, loader, runner, scorer, judge plumbing, metrics, report, CLI, tests.
3. **Reproducibility.** Scoring must run **offline** from cached raw model outputs. Store every raw response verbatim alongside the parsed object.
4. **Practice the caution the benchmark tests.** Reports and docstrings describe what is *measured*; they never overclaim results.

## Project layout

Agent-owned: `biocausalcalib/` (`schemas.py`, `loader.py`, `runner.py`, `scorer.py`, `judge.py`, `metrics.py`, `report.py`, `cli.py`), `tests/`, `Makefile`, `pyproject.toml`.
Human-owned (do not modify): `data/*.jsonl`, `docs/*`, `prompts/*`, the project plan.
Generated: `results/`.

## Data contract

Each line of `data/*.jsonl` is one item (plan Section 8). Required fields:

`id`, `item_type`, `evidence_domain`, `evidence_vignette`, `proposed_claim`, `question`, `planted_fallacies`, `distractors`, `warranted_strength`, `adjudication_range`, `label_derivation`, `ideal_cautious_answer`, `common_failure_modes`, `resolution`. Optional: `scoring_notes`, `notes`.

**`planted_fallacies`** (the primary ground truth) — list of objects with:
`id`, `type`, `mechanism` (`commission` | `omission`), `planted_as`, `detection_criteria`, `remedy`, `required` (bool).

**`distractors`** (explicit negatives) — list of objects with: `type`, `why_absent`. A model flagging a distractor is a **false positive**.

**`label_derivation`** — object with: `framework`, `rule`, `citation`.

**Model output object:** `predicted_strength` (0–4), `identified_issues` (list[str]), `missing_evidence` (list[str]), `cautious_restatement` (str), `confidence` (0–1).

**Validate on load and fail loudly** on unknown enums, missing required fields, out-of-range values, malformed JSON, or `adjudication_range` not containing `warranted_strength`.

Controlled vocabularies (plan Appendix A):
- `item_type` ∈ {`anchored`, `probe`}
- `evidence_domain` ∈ {`rwe_heor`, `statistical_genetics`} — v0 ships **two tracks only**. (`omics_functional`, `evolution`, `cross_scale` appear only in `parked_items.jsonl`, which is **not** loaded by the benchmark loader.)
- `mechanism` ∈ {`commission`, `omission`}
- `warranted_strength` ∈ int 0–4; `adjudication_range` = `[lo, hi]`, ints, `lo <= warranted_strength <= hi`
- fallacy `type` ∈ the taxonomy in plan Sections 7.1–7.2 (load it as a validated enum)

## Tech & conventions

- Python 3.11+, **Pydantic v2**, **ruff**, **pytest**.
- Minimal deps: `pydantic`, provider SDKs (`anthropic`, `openai`) and/or `httpx`, `python-dotenv`, `click`/`argparse`, optionally `rich`. Implement kappa/ECE directly or with one small stats dep. **No torch/tensorflow/transformers.**
- Provider adapters behind one interface (Claude / OpenAI / open-weight), swappable. Keys from `.env`; **never hardcode or commit keys**.
- Temperature 0 by default; `--runs N` for repeated runs (self-consistency).
- **Mock mode** (`--mock`) returns canned outputs with **no API call**, so tests and `make demo` run offline.
- Full type hints; small testable functions; raw output persisted before parsing.

## Commands

- `make install` / `make test` (no network) / `make lint`
- `python -m biocausalcalib.cli validate <data.jsonl>`
- `python -m biocausalcalib.cli run --model <m> --data <f> --runs N --out <dir>` (supports `--mock`, `--prompt neutral|primed`)
- `python -m biocausalcalib.cli score --outputs <dir> --data <f>`
- `python -m biocausalcalib.cli report --scores <dir>`
- `make demo` — full loop on `data/biocausalcalib_v0_seed.jsonl` in mock mode, offline.

## Scoring semantics (plan Section 9)

**Primary — planted-fallacy detection.** Match the model's `identified_issues` + `missing_evidence` against each planted fallacy's `detection_criteria`, and against `distractors` as negatives. Compute **recall** (required-weighted), **precision** (reduced by distractor hits and fabrications), **F1**, and **recall by fallacy type**. v0 matching: keyword/heuristic + a clean interface hook so `judge.py` (LLM-judge) can replace it later. **Keep the matcher swappable — this is the single most important design seam in the codebase.**

**Secondary — strength calibration.** Exact match; within-1; **inside `adjudication_range` counts as correct**; and the **signed error** (`predicted − warranted`) so overclaiming (positive) is separable from underclaiming (negative). Overclaiming rate is the headline number.

**Also:** cautious-language appropriateness; fabrication penalty (evidence asserted but absent from the vignette).

**Label-free metrics:** self-consistency across `--runs`; cross-model disagreement (spread of `predicted_strength` per item).

**Splits to report:** by track, by fallacy type, and **`anchored` vs `probe`**.

## Definition of done (first milestone)

- `make test` and `make lint` pass.
- `validate data/biocausalcalib_v0_seed.jsonl` reports **5 valid items** and rejects deliberately broken items (bad enum, missing field, out-of-range strength, `warranted_strength` outside `adjudication_range`).
- `run → score → report` produces `results/summary_report.md`.
- `make demo` runs the whole loop offline with no network and no API key.

## What NOT to do

- Don't author, edit, reorder, or relabel items; don't reformat `data/*.jsonl` (one JSON object per line, so diffs stay clean).
- Don't load `parked_items.jsonl` into the benchmark — it is a different, incomplete schema.
- Don't call the network in tests.
- Don't "fix" a label you disagree with — report it.
- Don't expand scope beyond the harness (no web UI, no leaderboard, no retrieval).
- Don't add heavy dependencies.
