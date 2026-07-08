# BioCausalCalib — Project Plan & Benchmark Design (v0)

*A benchmark for measuring whether large language models overclaim causal certainty from biomedical evidence.*

**Status:** design draft (v0). This document is the source of truth for the first milestone. It is written to be read by (a) the human domain expert authoring items, (b) Claude assisting with design and analysis, and (c) a coding agent (Codex) implementing the harness.

---

## 1. Summary

BioCausalCalib is a small, high-quality benchmark that tests one thing: **when given a piece of biomedical evidence and a proposed causal claim, does an AI model judge the strength of that claim correctly — or does it overclaim?**

Each item presents an *evidence vignette* plus a *proposed claim*, and asks the model to (1) state the strongest level of causal certainty the evidence supports, (2) identify the key biases, confounders, or missing evidence, and (3) restate the claim at an appropriate level of caution. We grade the model against expert-authored labels, weighting the **identification of specific reasoning gaps** (relatively objective) above the exact certainty label (more subjective).

The v0 deliverable is a benchmark of ~60 items across statistical genetics, omics/functional evidence, evolutionary evidence, RWE/HEOR, and cross-scale reasoning; an evaluation harness; results comparing 3–4 frontier and open models; and a short write-up.

This is the first publishable brick under the longer-term **EvoReasoner** umbrella (evolution-grounded biological reasoning across scales). EvoReasoner is the research program; BioCausalCalib is the first concrete, finishable, publishable result.

---

## 2. Central question & positioning

**Central question:** *Do frontier AI models assign the right level of causal certainty to biomedical evidence, or do they systematically overclaim — and where?*

**Capability vs. calibration.** Existing biomedical AI benchmarks mostly measure *capability*: can the model do the analysis and reach the correct biological answer? Anthropic's BioMysteryBench (99 expert-authored bioinformatics tasks on real data, graded on final-answer correctness) is a capability benchmark, as are CompBioBench, BixBench, and BLADE. BioCausalCalib measures something orthogonal: *calibration* — does the model know how confident it is entitled to be, and does it recognize when evidence does **not** license a causal claim?

Position the project explicitly against capability benchmarks:

> *BioMysteryBench asks whether a model can find the right biological answer. BioCausalCalib asks whether the model knows how strong its causal claim is entitled to be, and where it overclaims.*

There is even a bridge: BioMysteryBench reported that on hard tasks models often produced "brittle" wins and, when uncertain, ran several methods and picked the answer they converged on — sometimes the wrong one. That is an epistemic-reliability failure, which is exactly this project's theme.

**What already exists (and why the wedge is specific):** general causal-reasoning benchmarks are crowded (CLadder, CausalBench, CaLM, CauSciBench, CausalProbe); genetics-specific LLM automation exists (MRAgent automates Mendelian randomization discovery). The open gap is a **calibration/overclaiming benchmark across the biomedical evidence stack**, and in particular one that covers **pharmacoepidemiological observational biases** (confounding by indication, immortal-time bias, healthy-user bias), which the existing causal benchmarks largely do not.

**What this is NOT:** not a medical chatbot, not clinical decision support, not a disease-specific biomarker engine, and not an MR-automation agent. It makes no patient-level recommendations and holds itself to the same standard of caution it is testing.

---

## 3. Why this project (the moat & the gap)

The moat is not "AI for biology" generally. It is a rare combination of expertise — **statistical genetics + RWE/HEOR + causal-inference discipline** — that makes it possible to author *defensible ground truth* about how much causal certainty a given piece of evidence warrants. Very few people can author high-quality items across GWAS/eQTL/MR interpretation **and** observational pharmacoepidemiology bias.

Two practical consequences shape the design:

1. **Weight toward current, defensible expertise.** RWE/HEOR is the current professional strength and the clearest open niche; statistical-genetics *fundamentals* (LD, pleiotropy, the association–causation gap, tissue relevance) are durable and do not require frontier currency; omics is the least current, so its track is kept small and leans more heavily on multi-rater adjudication.
2. **Content validity is the whole game.** Schemas, loaders, scorers, and a CLI are commodity engineering. The differentiating, hard part is the items and their labels. The plan front-loads the labels and the label-defensibility protocol (Section 13), not the software.

---

## 4. Design principles (non-negotiable)

- **Content validity over software.** A defensible label is worth more than a feature. If a label cannot be defended, cut the item.
- **Anchor to resolved cases where possible.** Prefer items whose "correct" answer is grounded in an outcome the field later settled (see Section 8), rather than invented de novo.
- **Score the reasoning, not just the number.** Whether the model flagged the specific bias/gap is more objective than whether it output "2" vs "3." Weight accordingly.
- **Small and rigorous beats large and shaky.** 60 defensible items with reported inter-rater agreement beat 500 auto-generated ones.
- **Report uncertainty about our own labels.** Where a defensible expert range exists, record it (`adjudication_range`) instead of pretending to a false precision.
- **Practice the caution we test.** No overclaiming about the benchmark itself in the write-up.

---

## 5. Task format

For each item the model receives exactly three fields: the **evidence vignette**, the **proposed claim**, and the **question** (a fixed instruction). It never sees the label.

The model returns a structured judgment (Section 11): a predicted certainty level (0–4), a list of identified issues (biases/confounders), a list of missing evidence, a one-paragraph cautious restatement, and a confidence score. v0 grades this structured output against a rubric; a later version can add an LLM-judge validated against human scores.

---

## 6. Warranted Causal Strength scale (0–4)

A five-level ladder (deliberately coarse — five, not ten). It combines Pearl-style rungs with an evidence-triangulation view.

| Level | Label | What justifies it | Language warranted |
|---|---|---|---|
| 0 | Unsupported / speculative | No empirical link beyond hypothesis or conjecture. | "hypothesized", "speculative" |
| 1 | Association only | Robust statistical association (GWAS hit, observational correlation, differential expression) with no design ruling out confounding or reverse causation. | "is associated with", "correlates with" |
| 2 | Mechanistic plausibility | Association **plus** a plausible mechanism or convergent correlative evidence (e.g., eQTL + expression + pathway) — but no causal-inference design. Explicitly **not** causal. | "may contribute to", "is consistent with a role in", "supports the hypothesis" |
| 3 | Causal evidence with important assumptions | A causal-inference design supports the effect but rests on assumptions that may be violated (MR with plausibly valid instruments + sensitivity analyses; a single perturbation experiment; a well-designed adjusted observational study). | "provides evidence for a causal effect, contingent on [assumptions]", "genetic evidence supports causality" |
| 4 | Strong causal / interventional | Converging causal evidence including interventional data (RCT; robust triangulation across MR + perturbation + trial). | "causes", "is an established causal factor", "is a validated target" |

**Assignment rule of thumb:** identify the strongest *design* present (correlation → mechanism → causal-inference design → interventional), then downgrade for unaddressed threats (confounding, pleiotropy, wrong tissue, species translation, immortal time, etc.).

---

## 7. Overclaim / failure-mode taxonomy

This taxonomy is the intellectual core of the benchmark. Each item is tagged with the overclaim types it is designed to elicit. Definitions are deliberately crisp.

### 7.1 Statistical genetics
- **GWAS_to_causality** — treating a GWAS association as proof the locus/gene causes the trait; ignores LD, the associational nature of GWAS, and that the lead SNP tags a region.
- **eQTL_to_causal_gene** — assuming an eQTL for a gene at a GWAS locus makes that gene causal; ignores that colocalization is required and multiple genes may be regulated.
- **colocalization_missing** — inferring a shared causal variant between GWAS and eQTL without formal colocalization; LD can create spurious overlap.
- **MR_assumption_ignored** — treating an MR estimate as causal proof without checking the instrumental-variable assumptions (relevance, independence/exchangeability, exclusion restriction).
- **pleiotropy_ignored** — ignoring horizontal pleiotropy as an alternative explanation for a genetic/MR association.
- **weak_instrument_bias** — using low-strength instruments, biasing MR toward the confounded observational estimate.
- **winners_curse** — using the discovery sample for both instrument selection and effect estimation, inflating estimates.
- **ancestry_generalization** — assuming a GWAS/PRS finding transfers across ancestries.
- **PRS_individual_prediction** — reading a polygenic score's population-level association as accurate individual-level prediction or clinical actionability.
- **reverse_causation** — assuming exposure→outcome when outcome→exposure is plausible.

### 7.2 Omics / functional / evolution
- **differential_expression_to_causation** — treating differential expression as evidence a gene causes the phenotype; it may be a downstream consequence.
- **expression_to_mechanism** — inferring a mechanism from expression alone.
- **cell_composition_confounding** — bulk expression differences driven by shifts in cell-type proportions rather than per-cell regulation.
- **single_cell_marker_overinterpretation** — reading a marker's presence in a cluster as a functional/causal cell state without validation.
- **pathway_enrichment_overclaim** — treating an enriched pathway as a causal driver; enrichment is descriptive and annotation-biased.
- **conservation_to_disease_causality** — assuming an evolutionarily conserved gene/site is therefore causal for a specific disease; constraint implies selection on *some* function, not relevance to a given phenotype.
- **perturbation_overgeneralization** — extrapolating an in-vitro/cell-line perturbation to organism/clinical causality.
- **animal_model_translation** — assuming a model-organism phenotype transfers to humans.

### 7.3 RWE / HEOR
- **observational_treatment_effect** — interpreting an observational treatment–outcome association as a causal treatment effect.
- **confounding_by_indication** — sicker (or healthier) patients are selectively treated, confounding the comparison.
- **healthy_user_bias** — adherent or preventive-service users are systematically healthier; their better outcomes are misattributed to treatment.
- **immortal_time_bias** — misclassified/guaranteed person-time biases in favor of the treated/exposed group.
- **selection_bias / collider** — conditioning on a collider induces spurious associations.
- **outcome_misclassification** — differential or non-differential outcome misclassification in claims/EHR data.
- **prevalent_user_bias** — studying prevalent rather than new users, missing early events and depleting susceptibles.
- **competing_risks_ignored** — ignoring competing events (e.g., death) when estimating cause-specific outcomes.
- **surrogate_to_outcome** — treating a surrogate-endpoint change as a clinical benefit.
- **cost_to_value_overclaim** — treating a cost or resource-use difference as evidence of value without a full economic model.

### 7.4 Cross-scale
- **cross_scale_compounding** — failing to account for the compounding of uncertainty when chaining links across biological levels (variant → expression → pathway → phenotype → clinical actionability). Overall confidence should be *lower* than any single link.

### 7.5 Underclaim / over-hedging (the opposite failure)
- **refuses_to_commit** — hedges even when strong interventional evidence warrants a causal statement.
- **false_balance** — treats well-established causal evidence as merely "one hypothesis."
- **generic_hedging** — adds boilerplate caveats without engaging the specific evidence.

---

## 8. Anchored vs. Probe items (contamination handling)

A real risk: famous resolved cases (HRT/WHI, HDL/CHD) are in model training data, so a model might recite the answer without reasoning. We handle this by using **two item types**, tagged in the schema:

- **`anchored`** — grounded in a real-world outcome the field later resolved (with a citation in `resolution`). Purpose: **validate the certainty scale** against something semi-objective ("the model asserted strong causality for a hypothesis that randomized evidence later refuted").
- **`probe`** — constructed vignettes that isolate a single failure mode, with expert-consensus labels and varied surface details. Purpose: **test reasoning, not recall** — whether the model applies the same caution to a *novel* eQTL or differential-expression claim it has never seen.

Report results split by type. The generalization signal lives in the `probe` items; the `anchored` items keep the labels honest.

---

## 9. Evidence domains & v0 item distribution

Recommended distribution for the first 60 items (tunable to authoring confidence — the point is that RWE/HEOR is co-lead, not an afterthought, and cross-scale gets real weight because it is where overclaiming is expected to be worst):

| Domain | Items | Notes |
|---|---|---|
| RWE / HEOR | 18 | Strongest current expertise + clearest open niche. Confounding by indication, immortal time, healthy-user, selection, misclassification, cost→value. |
| Statistical genetics | 18 | GWAS (4), eQTL/coloc (5), MR/IV (5), PRS/ancestry (4). Durable epistemics. |
| Omics / functional | 10 | Differential expression (4), single-cell (3), pathway (3). Smallest current expertise → lean on adjudication. |
| Evolution | 4 | Conservation → causality; comparative-genomics overreach. |
| Cross-scale | 10 | Chains spanning ≥3 levels; expected highest overclaim rates. |
| **Total** | **60** | |

---

## 10. Item schema

Items are stored as JSONL (one object per line). See `data/sample_items.jsonl` for 7 fully worked examples.

```json
{
  "id": "gen-eqtl-causalgene-003",
  "item_type": "probe",                     // "anchored" | "probe"
  "evidence_domain": "statistical_genetics", // see Appendix A
  "biological_levels": ["variant", "gene", "transcript", "tissue", "clinical_outcome"],
  "evidence_vignette": "…the factual setup shown to the model…",
  "proposed_claim": "…the claim to be judged…",
  "question": "Evaluate whether the proposed claim is warranted…",
  "warranted_strength": 2,                   // 0–4, the reference label
  "adjudication_range": [1, 2],              // defensible expert range (optional)
  "overclaim_types": ["eQTL_to_causal_gene", "colocalization_missing", "tissue_mismatch"],
  "expected_reasoning_points": [
    {"id": "r1", "point": "Linkage disequilibrium: the lead SNP tags many variants…", "required": true},
    {"id": "r2", "point": "Colocalization not demonstrated…", "required": true}
  ],
  "ideal_cautious_answer": "…a model answer at the correct level of caution…",
  "common_failure_modes": ["Declares the gene causal", "Declares a validated target"],
  "resolution": {                            // populated for anchored items
    "resolved": false,
    "description": "…the real-world outcome, for anchored items…",
    "citation": "…reference…"
  },
  "notes": "…design notes for annotators…"
}
```

`expected_reasoning_points` is the scoring backbone: `required: true` points must be hit; `required: false` points are credited but not mandatory.

---

## 11. Model-output schema (what we ask the model to return)

The prompt instructs the model to return JSON only:

```json
{
  "predicted_strength": 2,            // 0–4
  "identified_issues": ["whole-blood eQTL may be the wrong tissue", "no colocalization shown"],
  "missing_evidence": ["colocalization analysis", "direction-of-effect (MR)", "perturbational validation"],
  "cautious_restatement": "The evidence supports a plausible regulatory hypothesis implicating the gene, but does not establish it as causal or a validated target.",
  "confidence": 0.7
}
```

The runner stores raw model output verbatim alongside the parsed object, so scoring is reproducible and auditable.

---

## 12. Scoring & metrics

Per item, compute component scores (report them separately, and as a weighted composite):

- **Gap identification (weight ~0.5, the dominant term).** Recall over `expected_reasoning_points`, with `required` points weighted more. Matching model `identified_issues` / `missing_evidence` to expected points is done by a rubric (v0: human or keyword-assisted; v1: validated LLM-judge).
- **Strength calibration (weight ~0.3).** Report both exact match and within-1 of `warranted_strength`; treat a prediction inside `adjudication_range` as correct. Also record the **signed error** (predicted − warranted) to separate **overclaiming** (positive) from **underclaiming** (negative). Overclaiming is the headline metric.
- **Cautious-language appropriateness (weight ~0.15).** Does `cautious_restatement` use language matching the warranted level (no "proves/causes" at low levels; no excessive hedging at high levels)?
- **Fabrication penalty (multiplicative/subtractive).** Penalize inventing evidence not in the vignette (e.g., claiming colocalization was performed).

**Headline results to report:** overall overclaiming rate; overclaiming rate by domain and by overclaim type; gap-identification recall by domain; reliability (see Section 14); and an `anchored` vs `probe` split.

---

## 13. Label-defensibility protocol (the crux)

This section is what makes BioCausalCalib research rather than a well-organized opinion. The obvious challenge is: *how do you know a "warranted_strength = 2" label is correct and not just the author's view?* Two mechanisms:

1. **Anchoring (Section 8).** For `anchored` items, the label is tied to a documented resolution, not invented.
2. **Independent multi-rater adjudication.** At least two domain experts independently assign `warranted_strength` and the `expected_reasoning_points` for the full set (or, at minimum, a random ≥20-item subset). Compute:
   - **Cohen's/weighted kappa** on `warranted_strength`.
   - **Set overlap (Jaccard)** on `expected_reasoning_points`.
   Resolve disagreements by discussion. Items with persistent disagreement are marked **contested** and either dropped or reported separately. **Report the agreement statistics in the write-up** — this single number buys more credibility than doubling the item count.

Practical note: getting even one additional pharmacoepi or statistical-genetics colleague to review ~15 items before scaling is the highest-leverage de-risking step in the whole project. Converging AI opinions are not a substitute for it.

---

## 14. Model set & running protocol

- **Models:** at least one Claude model, one GPT model, and one open-weight model (e.g., a current Llama/Qwen/DeepSeek). Optionally include a reasoning vs. non-reasoning variant to see whether extended reasoning reduces overclaiming.
- **Blinding:** the model receives only vignette + claim + question; never the label or expected points.
- **Reliability:** run each item k = 3–5 times at low temperature (0–0.2). Report both accuracy and **consistency** (do repeated runs agree?), mirroring BioMysteryBench's reliability lens — a model that is right once in five is not reliable.
- **Determinism of scoring:** fixed prompt template (`prompts/model_prompt_v0.md`); store raw outputs; scoring is a separate, unit-tested step so results are reproducible from cached outputs without re-calling any API.

---

## 15. Worked example items (7)

Full machine-readable versions are in `data/sample_items.jsonl`. Summaries below (label = warranted strength):

1. **`rwe-hrt-chd-001` — HRT and coronary heart disease (anchored, label 1).** Observational cohorts found ~40–50% lower CHD in HRT users. Claim: HRT reduces CHD and should be prescribed for prevention. The association is a textbook healthy-user/confounding-by-indication artifact; the WHI RCT later reversed it. Must flag: healthy-user bias, residual confounding, need for an RCT.

2. **`rwe-immortal-time-002` — "responders live longer" (probe, label 1).** Cancer patients who received second-line therapy had longer survival from diagnosis. The comparison is biased by immortal time (patients must survive to be treated). Must flag: immortal-time bias and the landmark/time-varying fix.

3. **`gen-eqtl-causalgene-003` — eQTL → causal gene (probe, label 2, range 1–2).** A GWAS SNP is a whole-blood eQTL for Gene X, which is also up in inflamed tissue. Claim: Gene X is the causal gene and a target. Supports a regulatory *hypothesis* only. Must flag: LD/fine-mapping, missing colocalization, tissue relevance, and that "target" needs perturbation + clinical evidence.

4. **`gen-mr-hdl-chd-004` — HDL and CHD (anchored, label 1).** Higher HDL is strongly associated with lower CHD. Claim: raising HDL will reduce CHD. MR with HDL-specific instruments and HDL-raising RCTs both indicate no causal effect — HDL is a marker. Must flag: confounding, association≠causation, pleiotropy.

5. **`omics-de-driver-005` — differential expression → driver (probe, label 1, range 1–2).** Gene Y is strongly upregulated in tumor vs. normal and sits in a proliferation pathway. Claim: Gene Y drives growth and is a target. DE is correlational and may be a consequence; bulk comparisons are composition-confounded. Must flag: reverse causation/consequence, cell-composition confounding, need for perturbation.

6. **`evo-conservation-006` — conservation → causality (probe, label 1).** Gene Z is deeply conserved; one patient with a neurodevelopmental disorder carries a rare missense variant. Claim: because Z is conserved, the variant causes the disorder. Conservation implies selection on *some* function, not relevance to this phenotype; one patient is anecdotal. Must flag: constraint≠pathogenicity, need for segregation/de novo/case-control + functional data (ACMG framing).

7. **`xscale-variant-to-treatment-007` — full chain (probe, label 2, range 1–2).** GWAS variant → blood eQTL for Gene A → insulin pathway → mouse KO phenotype. Claim: therefore inhibiting Gene A's protein will treat patients. A coherent hypothesis whose links each carry unproven assumptions that compound. Must flag: colocalization gap, tissue relevance, mouse≠human, KO≠pharmacological inhibition, cross-scale compounding, and that a treatment claim needs human MR + trials.

---

## 16. Repo structure

```
biocausalcalib/
  README.md
  AGENTS.md                      # instructions for the coding agent (Codex)
  LICENSE
  pyproject.toml
  Makefile                       # install, test, lint, run, score, report, demo
  .gitignore
  .env.example                   # API keys (never committed)

  data/
    biocausalcalib_v0.jsonl      # the full benchmark (grows to ~60 items)
    sample_items.jsonl           # the 7 worked examples (seed)

  prompts/
    model_prompt_v0.md           # the fixed prompt sent to models under test
    scoring_rubric.md            # how a grader matches issues to expected points

  biocausalcalib/
    __init__.py
    schemas.py                   # Pydantic models: Item, ExpectedPoint, Resolution, ModelOutput
    loader.py                    # load + validate JSONL, controlled-vocab checks
    runner.py                    # provider adapters (Claude / OpenAI / open-weight), k-run support
    scorer.py                    # component scores + composite
    metrics.py                   # aggregate overclaim rate, recall, reliability, splits
    report.py                    # markdown report generation
    cli.py                       # `run`, `score`, `report`, `demo`

  docs/
    benchmark_design.md          # (this document, or a trimmed version)
    label_guide.md               # the 0–4 scale + assignment rules (Section 6)
    failure_modes.md             # the overclaim taxonomy (Section 7)
    limitations.md               # Section 19

  results/
    example_model_outputs/
    summary_report.md

  tests/
    test_schemas.py
    test_loader.py
    test_scorer.py
    test_metrics.py
```

---

## 17. Four-week roadmap

Each week has a definition of done (DoD). "Author" = human expert + Claude; "Build" = Codex.

**Week 1 — Foundations.**
- Finalize the label guide (Section 6), failure-mode taxonomy (Section 7), and item schema (Section 10).
- Author the first **15 items** (≈5 RWE, 5 genetics, 3 omics, 2 cross-scale) as the format-proving set.
- Build repo skeleton: `pyproject.toml`, package layout, `schemas.py` (Pydantic), `loader.py` with controlled-vocab validation, `tests/test_schemas.py`, `tests/test_loader.py`.
- **DoD:** `make test` passes; `loader.py` loads and validates `sample_items.jsonl`; one colleague has reviewed the 15 items and rough agreement is recorded.

**Week 2 — Scale content + harness.**
- Author to ~**40 items**.
- Build `runner.py` (provider adapters, JSON-only prompting, k-run support), `prompts/model_prompt_v0.md`, `scorer.py`, `metrics.py`, and CLI `run`/`score`/`report`.
- Dry-run one model on the 15 seed items end-to-end.
- **DoD:** `biocausalcalib run --model <m> --data sample_items.jsonl` produces stored outputs; `score` + `report` produce a readable summary.

**Week 3 — Full run + adjudication.**
- Reach **60 items**. Second-rater adjudication on the full set; compute kappa and Jaccard; finalize labels; mark/handle contested items.
- Run all 3–4 models with k repeats; generate results tables and by-domain / by-failure-mode / anchored-vs-probe breakdowns.
- **DoD:** complete results in `results/`; agreement statistics computed.

**Week 4 — Analysis + write-up.**
- Error analysis (expect highest overclaiming on eQTL→gene, differential-expression→causation, observational→causal, and cross-scale). Write the report/preprint and a polished `README.md`. Release the repo and data on GitHub (optionally Hugging Face).
- **DoD:** reproducible `make demo` (load → run or use cached outputs → score → report); a results summary; and a written findings document.

---

## 18. Division of labor: human + Claude + Codex

**Human expert + Claude (the moat — do not delegate to a coding agent):**
- Author evidence vignettes, claims, warranted-strength labels, and expected reasoning points.
- Run and interpret inter-rater adjudication.
- Write the analysis and framing.

**Codex (deterministic, testable engineering — implement from this spec):**
- Pydantic schemas, loader/validation, provider adapters in `runner.py`, `scorer.py`/`metrics.py`, CLI, `report.py`, and the test suite.

**Claude (design + review + writing):**
- Help design taxonomies and draft/critique items; review Codex's implementation against this spec; assist with analysis and the write-up.

**Guidance to encode in `AGENTS.md`:**
- The taxonomy, labels, and items in `data/` and `docs/` are the **source of truth**. Code must never silently change a label or a warranted strength.
- All scoring must be reproducible and unit-tested; store raw model outputs verbatim.
- Keep **authoring** (human-owned content) and **harness** (agent-owned code) cleanly separated.
- No network calls in tests; scoring must run from cached outputs.

---

## 19. Limitations & ethics

- **Labels are expert judgments.** Mitigated by resolved-case anchoring and by reporting inter-rater agreement; `adjudication_range` records defensible ranges rather than false precision.
- **Small N per cell.** Report qualitative patterns per domain; do not over-interpret sub-cell statistics.
- **Contamination.** Famous anchored cases may be recalled rather than reasoned; the `probe` items and varied surface details test generalization, and results are reported split by item type.
- **Not medical advice.** No patient-level recommendations; the benchmark tests reasoning about evidence, not clinical decisions.
- **Self-consistency.** The write-up applies the same caution it measures — no overclaiming about what the benchmark shows.

---

## 20. Beyond v0 (toward EvoReasoner)

Once v0 is released, staged increments — each a shippable result:
- Validated **LLM-judge** auto-scoring (calibrated against human scores).
- **Retrieval + citation verification** (does the model support claims with real, correctly-characterized references?).
- More items and a public **leaderboard**.
- An expanded **evolutionary-evidence** axis and a dedicated **cross-scale** track (the EvoReasoner vision).
- An **OMOP/RWE reasoning** module drawing directly on HEOR practice.

EvoReasoner remains the long-term program: AI systems that reason reliably across biological scales while remaining transparent, cautious, and reproducible. BioCausalCalib is the first evidence that such reasoning can be *measured*.

---

## Appendix A — controlled vocabularies

**Biological levels:** `sequence`, `variant`, `gene`, `transcript`, `protein`, `pathway`, `cell_state`, `tissue`, `organ_system`, `organism_phenotype`, `population_outcome`, `evolutionary_fitness`, `clinical_outcome`, `real_world_outcome`.

**Evidence domains (v0):** `statistical_genetics`, `omics_functional`, `rwe_heor`, `evolution`, `cross_scale`.

**Evidence types (for later tagging):** `evolutionary_conservation`, `comparative_genomics`, `functional_annotation`, `gwas`, `eqtl`, `pqtl`, `sqtl`, `mendelian_randomization`, `colocalization`, `transcriptomics`, `single_cell`, `perturbation`, `animal_model`, `clinical_trial`, `observational_study`, `real_world_evidence`, `heor`, `expert_review`, `unsupported_hypothesis`.
