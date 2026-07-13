# RWE candidates — answer key (my drafted labels)

Open ONLY after you have filled `rwe_blind_worksheet.md`.

**0-4 scale:** 0 = unsupported/invalid design · 1 = association only · 2 = mechanistic plausibility (no valid causal design, or assumptions untested) · 3 = causal evidence with important assumptions · 4 = strong causal / interventional

---

## 1. `rwe-collider-birthweight-008`  (anchored) — strength **1**, adjudication range [0, 1]

**Planted fallacies** (the ground truth a model should detect):
- **[REQUIRED] `collider`** (commission) — Model identifies birth weight as a collider and states that stratifying/conditioning on it opens a spurious, non-causal association between smoking and mortality.
- **[REQUIRED] `selection_bias`** (commission) — Model recognizes the within-stratum comparison is induced by selection on a post-exposure variable, not a real protective subgroup effect, and that the marginal effect is the valid estimand.

**Distractors** (deliberately NOT present — flagging one is a false positive):
- `confounding_by_indication` — No treatment is allocated by prognosis; the exposure is maternal smoking and the operative flaw is collider-stratification, not confounding by indication.
- `immortal_time_bias` — There is no time-varying treatment or misaligned follow-up window; the outcome is infant mortality assessed within birth-weight strata.

**Label derivation** — *Causal DAG / collider-stratification*: Conditioning on a collider (birth weight, a common effect of the exposure and of other causes of the outcome) induces a non-causal association; the stratified estimate identifies no causal effect. A within-stratum statistical association exists but is artifactual, so the protective claim warrants at most strength 1 and arguably 0.
  · citation: Hernandez-Diaz S, Schisterman EF, Hernan MA, Am J Epidemiol 2006; VanderWeele TJ (collider bias).

**Scoring / edge notes:** Mechanism nuance: the consensus explanation is collider-stratification bias plus unmeasured common causes of low birth weight; a model naming either mechanism should be credited. FACT-CHECK the citations.

**Anchored resolution (fact-check this):** The paradox is explained by collider-stratification (selection) bias induced by conditioning on birth weight; maternal smoking is not protective.
  · citation: Hernandez-Diaz S, Schisterman EF, Hernan MA. The birth weight 'paradox' uncovered? Am J Epidemiol. 2006;164(11):1115-1120. See also Wilcox AJ. Int J Epidemiol. 2001;30(6):1233-1241.

---

## 2. `rwe-outcome-misclass-009`  (probe) — strength **1**, adjudication range [0, 1]

**Planted fallacies** (the ground truth a model should detect):
- **[REQUIRED] `outcome_misclassification`** (commission) — Model identifies that the outcome misclassification is differential by exposure (fewer visits -> fewer diagnoses for Drug A) and that this can create a spurious lower coded rate; a strong answer adds that differential misclassification can bias in EITHER direction (the toward-the-null heuristic does not apply).
- **[REQUIRED] `observational_treatment_effect`** (commission) — Model states an observational claims comparison cannot establish a causal effect regardless of adjustment.
- **[optional] `confounding_by_indication`** (commission) — Model notes treatment allocation is non-random (confounding by indication) even apart from the outcome problem.

**Distractors** (deliberately NOT present — flagging one is a false positive):
- `immortal_time_bias` — Exposure is defined at initiation (new-user); there is no guaranteed event-free window credited to treatment.
- `competing_risks_ignored` — Incident depression is the outcome; no competing-event structure (e.g., death precluding diagnosis) is described.

**Label derivation** — *GRADE + measurement-bias analysis*: Observational claims comparison begins at low certainty. Differential outcome misclassification is a serious measurement-bias threat that can bias in either direction, and confounding by indication persists, so the evidence supports at most an association and arguably not even that (the 'effect' may be an ascertainment artifact): strength 0-1.
  · citation: GRADE Handbook; Lash TL, Fox MP, Fink AK, Applying Quantitative Bias Analysis, Springer 2009.

**Scoring / edge notes:** The either-direction point (f1) is the discriminating expert insight; confirm whether it should be required for full credit or credited as a bonus. The old-schema draft coined a 'detection_bias' tag; here it is folded into outcome_misclassification per plan Section 7.1 (which covers differential misclassification).

---

## 3. `rwe-prevalent-user-010`  (probe) — strength **1**, adjudication range [0, 1]

**Planted fallacies** (the ground truth a model should detect):
- **[REQUIRED] `prevalent_user_bias`** (commission) — Model identifies prevalent-user/survivor bias and depletion of susceptibles: the surviving cohort is selectively tolerant/low-risk and early on-treatment events are unobserved, biasing toward a null or protective result.
- **[REQUIRED] `observational_treatment_effect`** (commission) — Model states the observational comparison cannot support a causal safety/benefit conclusion.
- **[optional] `residual_confounding`** (omission) — Model notes that adjusting for post-baseline / drug-affected covariates in prevalent users adds bias.

**Distractors** (deliberately NOT present — flagging one is a false positive):
- `immortal_time_bias` — The described flaw is prevalent (not incident) user sampling; there is no guaranteed survival window between a time zero and treatment.
- `outcome_misclassification` — Venous thromboembolism is a reasonably ascertained hard outcome; misclassification is not the operative threat here.

**Label derivation** — *GRADE + new-user design principles*: A prevalent-user cohort violates new-user design principles: survivors are selected and early events are missing, biasing toward null/protective. Observational evidence starts low and this is a serious risk of bias, so a null/protective result supports no causal safety conclusion: strength 0-1.
  · citation: Ray WA, Am J Epidemiol 2003 (new-user designs); GRADE Handbook.

**Scoring / edge notes:** FACT-CHECK the Ray 2003 citation.

---

## 4. `rwe-cost-value-011`  (probe) — strength **1**, adjudication range [1, 2]

**Planted fallacies** (the ground truth a model should detect):
- **[REQUIRED] `cost_to_value_overclaim`** (commission) — Model states that value means health outcomes gained per unit cost and that a cost difference alone cannot establish value or cost-effectiveness; a full economic evaluation is required.
- **[REQUIRED] `observational_treatment_effect`** (commission) — Model notes the cost comparison is observational and confounded (channeling/selection), so the $3,000 difference may not be caused by the drug.
- **[optional] `confounding_by_indication`** (commission) — Model identifies channeling/confounding by indication as a specific driver of the cost difference.

**Distractors** (deliberately NOT present — flagging one is a false positive):
- `immortal_time_bias` — No misaligned time zero or guaranteed survival window is described; the comparison is of accrued 12-month costs.
- `competing_risks_ignored` — The endpoint is accrued cost, not a cause-specific time-to-event with a competing event.

**Label derivation** — *Health-economic evaluation standards*: A resource-use/cost difference is not a value or cost-effectiveness claim: value requires health outcomes per unit cost within a full economic model, anchored to a causal effectiveness estimate. The cost association is confounded and the outcomes side is absent, so the evidence supports at most a hypothesis-generating association (strength 1; a well-adjusted cost association might be argued to 2).
  · citation: Sanders GD et al. (Second Panel on Cost-Effectiveness in Health and Medicine), JAMA 2016.

**Scoring / edge notes:** Two layered overclaims: causal (drug caused lower cost) and value (cost = value). f1 (value needs outcomes) is the star.

---

## 5. `rwe-competing-risks-027`  (probe) — strength **1**, adjudication range [0, 1]

**Planted fallacies** (the ground truth a model should detect):
- **[REQUIRED] `competing_risks_ignored`** (commission) — Model identifies death as a competing event that reduces dementia ascertainment in the higher-mortality arm, so a lower observed proportion is compatible with no protective effect (or a harmful one).
- **[REQUIRED] `observational_treatment_effect`** (commission) — Model states the observed proportion difference does not establish a causal effect.
- **[optional] `confounding_by_indication`** (commission) — Model notes confounding by indication given the higher baseline mortality of Drug C users.

**Distractors** (deliberately NOT present — flagging one is a false positive):
- `immortal_time_bias` — Exposure groups are not defined by surviving to a treatment time; the operative flaw is competing risks, not immortal time.
- `healthy_user_bias` — Drug C users are sicker, not healthier, and allocation is clinical; self-selection into a healthy behavior is not the mechanism.

**Label derivation** — *Competing-risks estimand framework*: With death as a competing event and higher mortality in the exposed, the naive proportion diagnosed is not a valid estimate of dementia risk; a cumulative-incidence analysis with an explicit estimand is required. As reported, no causal conclusion is supported: strength 0-1.
  · citation: Austin PC, Lee DS, Fine JP. Circulation 2016 (competing risks).

**Scoring / edge notes:** Direction nuance (bonus, not required): the naive proportion UNDERstates dementia in the high-mortality arm, whereas 1-minus-Kaplan-Meier (censoring deaths) OVERstates cumulative incidence. A model raising either correctly is demonstrating sophistication. VERIFY these directions.

---

## 6. `rwe-surrogate-cast-028`  (anchored) — strength **2**, adjudication range [1, 2]

**Planted fallacies** (the ground truth a model should detect):
- **[REQUIRED] `surrogate_to_outcome`** (commission) — Model distinguishes a predictive surrogate from a validated surrogate for treatment effect, and notes that suppressing the marker need not reduce mortality and may act through off-target pathways.
- **[REQUIRED] `observational_treatment_effect`** (commission) — Model notes the surrogate-outcome association is observational/confounded, so removing the marker need not remove the underlying risk.

**Distractors** (deliberately NOT present — flagging one is a false positive):
- `immortal_time_bias` — No time-varying exposure or misaligned time zero is described; the flaw is surrogate-to-outcome reasoning.
- `healthy_user_bias` — This concerns a drug's mechanism and a surrogate endpoint, not patient self-selection into a preventive behavior.

**Label derivation** — *Surrogate-endpoint validation (Prentice) + GRADE indirectness*: A surrogate that predicts an outcome is not validated as a surrogate for treatment effect; relying on it introduces serious indirectness. Combined with a plausible mechanism the pre-trial evidence reaches mechanistic plausibility (2) but not causal benefit; a mortality-endpoint RCT is required. The anchor shows that rung-2 mechanistic plausibility can still be wrong.
  · citation: Prentice RL, Stat Med 1989; CAST Investigators, N Engl J Med 1989.

**Scoring / edge notes:** Deliberately labelled 2 (not 1): the pre-trial evidence combined a robust marker-outcome association WITH a plausible mechanism = mechanistic plausibility. FACT-CHECK the CAST citations.

**Anchored resolution (fact-check this):** The Cardiac Arrhythmia Suppression Trial (CAST) randomized post-MI patients with asymptomatic ventricular ectopy to encainide, flecainide, or placebo; the drugs suppressed ectopy but increased mortality and arrhythmic death, and those arms were stopped early.
  · citation: CAST Investigators. N Engl J Med. 1989;321(6):406-412. Echt DS et al. N Engl J Med. 1991;324(12):781-788.

---

## 7. `rwe-target-trial-029`  (probe) — strength **3**, adjudication range [2, 3]

**Planted fallacies** (the ground truth a model should detect):
- **[REQUIRED] `residual_confounding`** (omission) — Model correctly identifies residual/unmeasured confounding as the remaining assumption AND interprets the E-value properly (it bounds but does not exclude confounding) - treating it as a contingency on a level-3 causal claim, not as a fatal flaw that reduces the study to 'association'.

**Distractors** (deliberately NOT present — flagging one is a false positive):
- `immortal_time_bias` — An explicit, aligned time zero is specified, which removes immortal-time bias by construction.
- `prevalent_user_bias` — The analysis is restricted to new users, so prevalent-user/survivor bias does not apply.
- `healthy_user_bias` — An active-comparator design (Drug A vs Drug B, both treatments) removes the healthy-user contrast between treated and untreated.
- `confounding_by_indication` — The active-comparator new-user design, 120-covariate balance, and null negative-control outcomes specifically target and empirically probe confounding by indication; treating it as an unaddressed flaw ignores the design.

**Label derivation** — *Target trial emulation + E-value (VanderWeele-Ding)*: A new-user active-comparator target-trial emulation with covariate balance, null negative controls, and E-value 2.1 removes immortal-time and prevalent-user bias and mitigates confounding by indication; the remaining assumption is no substantial unmeasured confounding. This is causal evidence contingent on stated assumptions (level 3) - not association-only, and not interventional-grade (which needs randomization or triangulation).
  · citation: Hernan MA & Robins JM, Am J Epidemiol 2016; VanderWeele TJ & Ding P, Ann Intern Med 2017; Lipsitch M et al., Epidemiology 2010 (negative controls).

**Scoring / edge notes:** POSITIVE CONTROL. The distractors are the main scoring lever: a model that flags immortal-time / prevalent-user / healthy-user as present flaws is over-claiming flaws (false positives) and typically under-claiming strength. Reward affirming ~level 3 with residual confounding named as the contingency and the E-value read correctly. VERIFY the E-value definition as worded.

---

## 8. `rwe-healthy-adherer-030`  (anchored) — strength **1**, adjudication range [0, 1]

**Planted fallacies** (the ground truth a model should detect):
- **[REQUIRED] `healthy_user_bias`** (commission) — Model identifies healthy-adherer / self-selection bias: adherence marks overall prognosis and engagement with care, not just drug taking.
- **[REQUIRED] `residual_confounding`** (omission) — Model notes the confounders are largely unmeasured in claims, so covariate adjustment does not remove the bias.
- **[REQUIRED] `observational_treatment_effect`** (commission) — Model states the association cannot establish that adherence causally lowers mortality, and that the interventional claim is a further leap.

**Distractors** (deliberately NOT present — flagging one is a false positive):
- `immortal_time_bias` — The operative flaw is confounding by health-seeking behaviour, not a guaranteed survival window; adherence here is a self-selection contrast.
- `confounding_by_indication` — This is patient self-selection into adherence, not prescriber allocation of treatment by indication.

**Label derivation** — *GRADE (risk of bias) + negative-control reasoning*: Observational adherence-outcome comparison begins at low certainty with serious risk of bias from healthy-adherer self-selection, which measured-covariate adjustment does not remove. The adherence-to-placebo negative control - the same mortality association appears for placebo, which cannot cause survival - demonstrates the association is confounded, not causal: strength 0-1.
  · citation: Coronary Drug Project Research Group, N Engl J Med 1980; Simpson SH et al., BMJ 2006; GRADE Handbook.

**Scoring / edge notes:** The placebo-adherence anchor is unusually clean (placebo cannot cause survival). FACT-CHECK the Coronary Drug Project 1980 and Simpson 2006 citations. Exact percentages deliberately kept out of the vignette.

**Anchored resolution (fact-check this):** Adherence to PLACEBO is associated with lower mortality in randomized trials (Coronary Drug Project; reproduced by a later meta-analysis); because placebo cannot cause survival, the adherence-outcome association is attributed to healthy-adherer confounding.
  · citation: Coronary Drug Project Research Group. N Engl J Med. 1980;303(18):1038-1041. Simpson SH et al. BMJ. 2006;333(7557):15.

---
