# Overclaim / failure-mode taxonomy — canonical `overclaim_types` registry

This file is the **canonical controlled vocabulary** for the `overclaim_types` field in
benchmark items. The narrative rationale for the taxonomy lives in **Project Plan §7**; this
document is the machine-usable token list (one line per tag) that item labels must draw from,
and the place where tags coined during authoring are formally registered.

> Status: v0. `overclaim_types` is currently typed as an unconstrained `list[str]` in
> `schemas.py`. This registry is intended to back an (optional, later) controlled-vocabulary
> check in `loader.py`. Until then it is the authoring source of truth.

---

## §7.1 Statistical genetics

- `GWAS_to_causality` — treating a GWAS association as proof the locus/gene causes the trait; ignores LD and that the lead SNP tags a region.
- `eQTL_to_causal_gene` — assuming an eQTL for a gene at a GWAS locus makes that gene causal; ignores that colocalization is required and multiple genes may be regulated.
- `colocalization_missing` — inferring a shared causal variant between GWAS and eQTL without formal colocalization; LD can create spurious overlap.
- `MR_assumption_ignored` — treating an MR estimate as causal proof without checking the IV assumptions (relevance, independence/exchangeability, exclusion restriction).
- `pleiotropy_ignored` — ignoring horizontal pleiotropy as an alternative explanation for a genetic/MR association.
- `weak_instrument_bias` — using low-strength instruments, biasing MR (toward the confounded observational estimate under sample overlap; toward the null in two-sample non-overlapping designs).
- `winners_curse` — using the discovery sample for both instrument selection and effect estimation, inflating SNP–exposure estimates.
- `ancestry_generalization` — assuming a GWAS/PRS finding transfers across ancestries.
- `PRS_individual_prediction` — reading a polygenic score's population-level association as accurate individual-level prediction or clinical actionability.
- `reverse_causation` — assuming exposure→outcome when outcome→exposure is plausible.

## §7.2 Omics / functional / evolution

- `differential_expression_to_causation` — treating differential expression as evidence a gene causes the phenotype; it may be a downstream consequence.
- `expression_to_mechanism` — inferring a mechanism from expression alone.
- `cell_composition_confounding` — bulk expression differences driven by shifts in cell-type proportions rather than per-cell regulation.
- `single_cell_marker_overinterpretation` — reading a marker's presence in a cluster as a functional/causal cell state without validation.
- `pathway_enrichment_overclaim` — treating an enriched pathway as a causal driver; enrichment is descriptive and annotation-biased.
- `conservation_to_disease_causality` — assuming an evolutionarily conserved gene/site is therefore causal for a specific disease.
- `perturbation_overgeneralization` — extrapolating an in-vitro/cell-line/genetic perturbation to organism/clinical causality.
- `animal_model_translation` — assuming a model-organism phenotype (or drug effect) transfers to humans.

## §7.2b Evolution / comparative genomics — **proposed new subsection**

Plan §7.2 folds evolution into omics and supplies only one evolution tag
(`conservation_to_disease_causality`). Authoring the evolution track (items 024–026) required six
more. Proposed as a dedicated subsection; all six are **provisional pending sign-off**.

- `conservation_to_disease_causality` — assuming a conserved gene/site is therefore causal for a specific disease. *(existing; §7.2)*
- `conservation_to_essentiality` — assuming a conserved element is necessary in vivo, or that deleting it yields an overt phenotype; constraint implies selection on *some* function, not demonstrated necessity.
- `phylogenetic_nonindependence` — treating species as independent observations in a cross-species comparison; shared ancestry makes related species resemble one another, inflating false positives (requires independent contrasts / PGLS).
- `comparative_genomics_overreach` — inferring function or causality from a cross-species genomic comparison (gene-family size, presence/absence, copy number) without phylogenetic control or perturbation.
- `selection_scan_overinterpretation` — treating a selection-scan signal as identifying the selected gene; demography mimics selection, and hitchhiking sweeps a whole region rather than a gene.
- `adaptive_storytelling` — attributing a selection signal to a specific phenotype ("selected *for* X") on the basis of a nearby gene annotation; a post-hoc just-so story, not evidence.
- `ecological_fallacy` — inferring an individual-level association or causal effect from a population-level correlation. *(cross-cuts to RWE/HEOR; usable outside the evolution track)*

## §7.3 RWE / HEOR

- `observational_treatment_effect` — interpreting an observational treatment–outcome association as a causal treatment effect.
- `confounding_by_indication` — sicker (or healthier) patients are selectively treated, confounding the comparison.
- `healthy_user_bias` — adherent or preventive-service users are systematically healthier; their better outcomes are misattributed to treatment.
- `immortal_time_bias` — misclassified/guaranteed person-time biases in favor of the treated/exposed group.
- `outcome_misclassification` — differential or non-differential error in the *measurement* of the outcome in claims/EHR data.
- `prevalent_user_bias` — studying prevalent rather than new users, missing early events and depleting susceptibles.
- `competing_risks_ignored` — ignoring competing events (e.g., death) when estimating cause-specific outcomes.
- `surrogate_to_outcome` — treating a surrogate-endpoint change as a clinical benefit.
- `cost_to_value_overclaim` — treating a cost or resource-use difference as evidence of value without a full economic model.

## §7.4 Cross-scale

- `cross_scale_compounding` — failing to account for compounding uncertainty when chaining links across biological levels; overall confidence should be *lower* than any single link.

## §7.5 Underclaim / over-hedging (the opposite failure)

- `refuses_to_commit` — hedges even when strong interventional evidence warrants a causal statement.
- `false_balance` — treats well-established causal evidence as merely "one hypothesis."
- `generic_hedging` — adds boilerplate caveats without engaging the specific evidence.

---

## v0 additions — canonicalized

Tags coined during authoring and now promoted to the canonical vocabulary.

- `collider_bias` — conditioning on (stratifying/adjusting for) a common effect of exposure and outcome, inducing a spurious association. *Split out from the plan's fused `selection_bias / collider` for precision.* (Items: `rwe-collider-birthweight-008`.)
- `selection_bias` — broader umbrella: any bias from non-random inclusion into, or conditioning within, the analysis sample (includes collider and prevalent-user/survivor selection). Use `collider_bias` when the mechanism is specifically conditioning on a common effect. (Items: 008, `rwe-prevalent-user-010`.)
- `detection_bias` — differential *opportunity* to observe/record an outcome (surveillance/ascertainment), distinct from `outcome_misclassification` (error in the outcome measurement itself); the two often co-occur. (Items: `rwe-outcome-misclass-009`.)
- `tissue_mismatch` — an eQTL/expression signal measured in a tissue or cell type not relevant to the disease. *Already present in the seed set* (items `gen-eqtl-causalgene-003`, `xscale-variant-to-treatment-007`); registered here for completeness.

## Provisional — pending author sign-off

Coined during authoring of draft items 016–026; **not yet approved**. Rename/merge as you prefer.
These have accumulated across two batches and want a single sign-off pass.

*From the omics / cross-scale batch (016–023):*

- `trajectory_causal_direction` — reading a single-cell pseudotime/trajectory ordering as a real temporal or causal sequence. (Item: `omics-sc-pseudotime-019`.) *Candidate merge target:* could fold under `single_cell_marker_overinterpretation` if you'd rather not add a token.
- `genetic_to_therapeutic_overclaim` — treating a genetically/MR-validated causal target as proof a drug against it will be efficacious (ignores lifelong-genetic vs pharmacological differences, safety, tractability). (Item: `xscale-pqtl-mr-drug-020`.)

*From the evolution batch (024–026) — see proposed §7.2b above for definitions:*

- `conservation_to_essentiality` (item 024)
- `phylogenetic_nonindependence` (item 025) — the star concept of 025; nothing else in the benchmark tests it.
- `comparative_genomics_overreach` (item 025)
- `selection_scan_overinterpretation` (item 026)
- `adaptive_storytelling` (item 026)
- `ecological_fallacy` (item 026) — *note:* this one is not evolution-specific and would be equally at home in §7.3 RWE/HEOR.

*From the RWE / genetics batch (027–034):*

- `nearest_gene_fallacy` (item 031) — assigning causality at a GWAS locus to the gene nearest the lead SNP; regulatory variants frequently act at long range on distal genes. *Candidate merge target:* could fold under `GWAS_to_causality`, but it names a distinct, commonly-made inference.

## To reconcile

- `unsupported_hypothesis` — used as an `overclaim_type` in seed item `evo-conservation-006`, but in Appendix A it is listed as an *evidence type*, not an overclaim tag. Decide whether to (a) keep it as a valid overclaim token meaning "asserted with no empirical support," or (b) drop it from `overclaim_types` and rely on `warranted_strength = 0`.

---

## Scale-application note — predictive vs causal claims

The 0–4 warranted-strength ladder (Plan §6) is defined for **causal** certainty. A small number of
items test **predictive** overclaiming instead (notably `PRS_individual_prediction`). Decision (v0,
locked): these are scored on the **same 0–4 scale under a "predictive-warrant" reading** — no separate
scale or scoring path — where the levels map as: 0 = no signal → 1 = robust population-level
association / modest individual prediction → 2 = validated prediction with important caveats → 3–4 =
strong, calibrated, clinically-actionable prediction. For `gen-prs-individual-012`,
`warranted_strength = 1` means "robust population-level prediction signal, not the individual accuracy
or clinical actionability the claim asserts." Report predictive-claim items so they can be inspected
separately if a reviewer wants to.
