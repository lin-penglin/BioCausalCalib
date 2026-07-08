# AGENTS.md — working guide for coding agents (Codex, Claude Code)

This file governs how automated coding agents work in the BioCausalCalib repository. Read it before writing any code. The authoritative design spec is **`BioCausalCalib_Project_Plan.md`** (or `docs/benchmark_design.md` if it has been split). Read that first.

## What this repo is

BioCausalCalib is a **calibration benchmark**: it measures whether large language models *overclaim causal certainty* when given biomedical evidence. Each item presents an evidence vignette plus a proposed claim; a model must judge the strongest level of causal certainty the evidence supports (a 0–4 scale), identify the specific biases/confounders/missing evidence, and restate the claim cautiously. The harness runs models on the items and scores their judgments against expert-authored labels.

## Golden rules (read first)

1. **Content is the source of truth; code serves it.** Benchmark items and their labels live in `data/*.jsonl` and are owned by human domain experts. Code **must not** create, edit, delete, reorder, or re-label items, and must not change any `warranted_strength`, `expected_reasoning_points`, `overclaim_types`, or `adjudication_range`. If a schema change would force a data change, **propose it in an issue/summary — do not silently rewrite data.**
2. **Authoring vs. harness separation.** Your scope is the *harness*: schemas, loader, runner, scorer, metrics, report, CLI, tests. **Item authoring is out of scope for coding agents.**
3. **Reproducibility.** Scoring must be fully reproducible from stored raw model outputs with **no network access**. Store every model's raw response verbatim next to the parsed object.
4. **Practice the caution the benchmark tests.** Code comments, reports, and docstrings describe what is *measured*; they never assert causal conclusions or overclaim results.

## Project layout

Code (agent-owned): `biocausalcalib/` (`schemas.py`, `loader.py`, `runner.py`, `scorer.py`, `metrics.py`, `report.py`, `cli.py`), `tests/`, `Makefile`, `pyproject.toml`.

Content (human-owned, do not modify): `data/*.jsonl`, `docs/*`, `prompts/*`, and the project plan.

Outputs (generated): `results/`.

## The data contract (do not break)

Each line of `data/*.jsonl` is one item with the fields defined in the plan (Section 10). Required fields: `id`, `item_type`, `evidence_domain`, `biological_levels`, `evidence_vignette`, `proposed_claim`, `question`, `warranted_strength`, `overclaim_types`, `expected_reasoning_points`, `ideal_cautious_answer`, `common_failure_modes`, `resolution`. Optional: `adjudication_range`, `notes`.

The model-output object (Section 11) has: `predicted_strength` (0–4), `identified_issues` (list), `missing_evidence` (list), `cautious_restatement` (str), `confidence` (0–1).

**Validate on load and fail loudly** on unknown enum values, missing required fields, out-of-range strengths, or malformed JSON.

Controlled vocabularies to validate against (Appendix A of the plan):
- `item_type` ∈ {`anchored`, `probe`}
- `evidence_domain` ∈ {`statistical_genetics`, `omics_functional`, `rwe_heor`, `evolution`, `cross_scale`}
- `warranted_strength` ∈ integers 0–4; `adjudication_range` = two ints in 0–4 with `lo <= hi`
- `biological_levels` ⊆ {`sequence`, `variant`, `gene`, `transcript`, `protein`, `pathway`, `cell_state`, `tissue`, `organ_system`, `organism_phenotype`, `population_outcome`, `evolutionary_fitness`, `clinical_outcome`, `real_world_outcome`}

## Tech & conventions

- **Python 3.11+.** **Pydantic v2** for all schemas. **ruff** for lint/format. **pytest** for tests.
- **Keep dependencies minimal.** Allowed: `pydantic`, official provider SDKs (`anthropic`, `openai`) and/or `httpx`, `python-dotenv`, `click` or stdlib `argparse`, and optionally `rich`. Implement Cohen's/weighted kappa directly or use a single small stats dep — do **not** add heavy ML frameworks (no torch/tensorflow/transformers).
- **Provider adapters behind one interface** so models are swappable (`Claude`, `OpenAI`, `OpenWeight`). Read API keys from environment via `.env` (documented in `.env.example`); **never hardcode or commit keys.**
- **Determinism:** default temperature 0; support repeated runs via `--runs N` (default 1) for reliability measurement.
- **Mock mode:** the runner must support a `--dry-run`/`--mock` mode that returns canned outputs **without any API call**, so tests and `make demo` run offline.
- Full type hints; small, testable functions; raw model output always persisted before parsing.

## Commands (implement in the Makefile / CLI)

- `make install` — install the package and dev deps.
- `make test` — run pytest (no network).
- `make lint` — run ruff.
- `python -m biocausalcalib.cli validate <data.jsonl>` — validate a benchmark file; report item count and any errors.
- `python -m biocausalcalib.cli run --model <m> --data <data.jsonl> --runs N --out <dir>` — run a model (or mock), persist raw + parsed outputs.
- `python -m biocausalcalib.cli score --outputs <dir> --data <data.jsonl>` — score stored outputs.
- `python -m biocausalcalib.cli report --scores <dir>` — write `results/summary_report.md`.
- `make demo` — run the full loop on `data/sample_items.jsonl` in mock mode (offline) and emit a report.

## Scoring semantics (implement per plan Section 12)

Per item, compute and report component scores plus a weighted composite:
- **Gap identification (~0.5, dominant):** recall over `expected_reasoning_points`, weighting `required: true` points more. Match the model's `identified_issues` + `missing_evidence` to expected points via a documented rubric (v0: keyword/heuristic + human review; leave a clean hook for an LLM-judge later).
- **Strength calibration (~0.3):** report exact match **and** within-1 of `warranted_strength`; a prediction inside `adjudication_range` counts as correct. Record the **signed error** (predicted − warranted) so overclaiming (positive) is separable from underclaiming (negative).
- **Cautious-language appropriateness (~0.15):** does `cautious_restatement` match the warranted level?
- **Fabrication penalty:** penalize evidence invented but not present in the vignette.

Aggregate reporting must include: overall **overclaiming rate**; overclaiming rate **by domain** and **by overclaim type**; gap-identification recall by domain; **reliability** across `--runs`; and an **`anchored` vs `probe`** split.

## Definition of done (first milestone)

- `make test` and `make lint` pass.
- `validate data/sample_items.jsonl` reports **7 valid items** and rejects a deliberately broken item (bad enum / missing field / bad range).
- `run` produces stored raw + parsed outputs; `score` + `report` produce `results/summary_report.md`.
- `make demo` runs the whole loop offline (mock mode) with no network and no API key.

## What NOT to do

- Don't author, edit, reorder, or relabel items; don't reformat `data/*.jsonl` (keep one-JSON-object-per-line so diffs stay clean).
- Don't call external networks in tests.
- Don't "fix" a label you disagree with — record it in your summary/an issue instead.
- Don't expand scope beyond the harness (no web UI, no leaderboard, no retrieval yet).
- Don't add heavy dependencies.
