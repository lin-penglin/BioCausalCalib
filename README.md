# BioCausalCalib

> A benchmark for measuring whether large language models **overclaim causal certainty** from biomedical evidence.

**Status:** v0, in progress (design + seed items). See [`BioCausalCalib_Project_Plan.md`](./BioCausalCalib_Project_Plan.md) for the full design.

---

## The question

> Do frontier AI models assign the right level of causal certainty to biomedical evidence, or do they systematically overclaim — and where?

## What it measures: capability vs. calibration

Most biomedical AI benchmarks measure *capability* — can a model do the analysis and reach the correct biological answer? BioCausalCalib measures something orthogonal — *calibration*: does a model know how confident it is entitled to be, and does it recognize when evidence does **not** license a causal claim?

> BioMysteryBench (Anthropic, 2026 — a 99-question expert-authored bioinformatics benchmark graded on final-answer correctness) asks whether a model can find the right biological answer. BioCausalCalib asks whether the model knows *how strong* its causal claim is entitled to be, and where it overclaims.

This is the first publishable component of the longer-term **EvoReasoner** program (evolution-grounded biological reasoning across scales).

## How it works

Each item gives the model three fields — an **evidence vignette**, a **proposed claim**, and a fixed **question** — and asks it to return a structured judgment:

```json
{
  "predicted_strength": 2,
  "identified_issues": ["whole-blood eQTL may be the wrong tissue", "no colocalization shown"],
  "missing_evidence": ["colocalization", "direction-of-effect (MR)", "perturbational validation"],
  "cautious_restatement": "The evidence supports a plausible regulatory hypothesis, not a validated target.",
  "confidence": 0.7
}
```

We grade the judgment against expert-authored labels, **weighting the identification of specific reasoning gaps above the exact certainty number** (Section 12 of the plan). Items come in two types:

- **`anchored`** — grounded in a real-world outcome the field later resolved (e.g., HRT/CHD reversed by the WHI trial). These validate the certainty scale against something semi-objective.
- **`probe`** — constructed to isolate a single failure mode, with varied surface details. These test whether cautious reasoning *generalizes* rather than being recalled.

## The warranted-causal-strength scale (0–4)

| Level | Label | Justified by |
|---|---|---|
| 0 | Unsupported / speculative | Hypothesis or conjecture only |
| 1 | Association only | Robust association, no design ruling out confounding/reverse causation |
| 2 | Mechanistic plausibility | Association + plausible mechanism / convergent correlative evidence (not causal) |
| 3 | Causal evidence with important assumptions | A causal-inference design (MR, perturbation, adjusted observational) resting on violable assumptions |
| 4 | Strong causal / interventional | Converging causal evidence including interventional data (RCT / triangulation) |

Full definitions and the overclaim taxonomy are in [`docs/label_guide.md`](./docs/label_guide.md) and [`docs/failure_modes.md`](./docs/failure_modes.md).

## Quickstart

```bash
make install                       # install package + dev deps (Python 3.11+)
cp .env.example .env               # add API keys for the models you want to test

# Run the whole loop offline on the 7 seed items (mock mode, no keys needed):
make demo

# Validate a benchmark file:
python -m biocausalcalib.cli validate data/sample_items.jsonl

# Run a real model, then score and report:
python -m biocausalcalib.cli run    --model claude --data data/sample_items.jsonl --runs 3 --out results/run1
python -m biocausalcalib.cli score  --outputs results/run1 --data data/sample_items.jsonl
python -m biocausalcalib.cli report --scores results/run1
```

## Repository layout

```
biocausalcalib/
  BioCausalCalib_Project_Plan.md   # full design spec (source of truth)
  AGENTS.md                        # working guide for coding agents
  README.md
  data/
    biocausalcalib_v0.jsonl        # the full benchmark (grows to ~60 items)
    sample_items.jsonl             # 7 fully worked seed items
  prompts/                         # model prompt + scoring rubric
  biocausalcalib/                  # schemas, loader, runner, scorer, metrics, report, cli
  docs/                            # label_guide, failure_modes, limitations
  results/                         # generated outputs
  tests/
```

## Coverage (v0 target: ~60 items)

| Domain | Items |
|---|---|
| RWE / HEOR | 18 |
| Statistical genetics | 18 |
| Omics / functional | 10 |
| Evolution | 4 |
| Cross-scale | 10 |

## Contributing items

Items are expert-authored — this is where the benchmark's value lives. A new item must:

1. Match the JSONL schema (plan Section 10).
2. Include a `warranted_strength` with a written rationale, and an `adjudication_range` if the label is contestable.
3. Give precise `expected_reasoning_points` (the biases/gaps a correct answer must name) — the scorer depends on these.
4. For `anchored` items, cite the real-world resolution in `resolution`.
5. Ideally carry a second domain-expert's label; agreement is tracked and reported.

See the label-defensibility protocol (plan Section 13). Labels must be defensible, not merely opinion.

## Limitations

Labels are expert judgments (mitigated by anchoring and reported inter-rater agreement); per-cell sample sizes are small (report patterns, not over-precise sub-cell statistics); famous anchored cases risk training-data contamination (mitigated by probe items and reported by item-type split). This is not medical advice and makes no patient-level recommendations. See [`docs/limitations.md`](./docs/limitations.md).

## Citation

```bibtex
@misc{biocausalcalib,
  title  = {BioCausalCalib: Measuring Causal Overclaiming in Biomedical AI Reasoning},
  year   = {2026},
  note   = {https://github.com/<org>/biocausalcalib}
}
```

## License

See [`LICENSE`](./LICENSE).
