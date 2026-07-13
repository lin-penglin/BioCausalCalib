# RWE candidates — blind-label worksheet

Fill this in BEFORE opening `rwe_answer_key.md`. For each item you see only what the model sees.

**0-4 scale:** 0 = unsupported/invalid design · 1 = association only · 2 = mechanistic plausibility (no valid causal design, or assumptions untested) · 3 = causal evidence with important assumptions · 4 = strong causal / interventional

Fixed question for every item: *"Evaluate whether the proposed claim is warranted... state the strongest level of causal certainty (0-4), identify every bias/confounder/missing evidence, and restate cautiously."*

---

## 1. `rwe-collider-birthweight-008`  (anchored)

**Evidence:** In perinatal cohort data, infant mortality is compared by maternal smoking within birth-weight strata. Overall, maternal smoking lowers birth weight and raises infant mortality. However, among low-birth-weight (LBW) infants specifically, those born to mothers who smoked during pregnancy had LOWER infant mortality than LBW infants of non-smoking mothers.

**Proposed claim:** Among low-birth-weight infants, maternal smoking is protective against infant mortality; the birth-weight-stratified analysis shows smoking reduces mortality in these infants.

**Your answer (fill before peeking):**

- Warranted strength (0-4): `__0__`
- Framework + rule you used to get there: `_confounding effect_______________`
- Biases / gaps you judge PRESENT (list every one; mark which you'd *require* a model to catch):
    - 
    - 
    - 
- Biases you considered but rule out as NOT operative here (your "distractors"):
    - 
- Vignette ambiguous or under-specified? (Y/N + note): `____`
- Your confidence (low/med/high): `__high__`

---

## 2. `rwe-outcome-misclass-009`  (probe)

**Evidence:** An administrative-claims study defines incident depression using a single ICD-10 diagnosis code, and defines exposure as initiation of Drug A versus Drug B. Drug A initiators have a 25% lower rate of coded depression than Drug B initiators. Drug A initiators also have, on average, fewer outpatient visits per year than Drug B initiators.

**Proposed claim:** Drug A lowers the risk of developing depression compared with Drug B.

**Your answer (fill before peeking):**

- Warranted strength (0-4): `____`
- Framework + rule you used to get there: `________________`
- Biases / gaps you judge PRESENT (list every one; mark which you'd *require* a model to catch):
    - 
    - 
    - 
- Biases you considered but rule out as NOT operative here (your "distractors"):
    - 
- Vignette ambiguous or under-specified? (Y/N + note): `____`
- Your confidence (low/med/high): `____`

---

## 3. `rwe-prevalent-user-010`  (probe)

**Evidence:** A cohort study samples current users of a long-term medication (many on it for years) and compares their rate of a serious adverse event (venous thromboembolism) with non-users. Users are included regardless of when they started therapy. The study finds users have a similar, or slightly lower, event rate than non-users.

**Proposed claim:** The medication does not increase the risk of venous thromboembolism and may even be protective.

**Your answer (fill before peeking):**

- Warranted strength (0-4): `____`
- Framework + rule you used to get there: `________________`
- Biases / gaps you judge PRESENT (list every one; mark which you'd *require* a model to catch):
    - 
    - 
    - 
- Biases you considered but rule out as NOT operative here (your "distractors"):
    - 
- Vignette ambiguous or under-specified? (Y/N + note): `____`
- Your confidence (low/med/high): `____`

---

## 4. `rwe-cost-value-011`  (probe)

**Evidence:** A retrospective claims analysis reports that patients initiating a new biologic had approximately $3,000 lower mean total annual health-care costs than patients on standard therapy, driven mainly by fewer hospitalizations. Drug-acquisition cost was included in the total. Follow-up was 12 months. No health-outcome (effectiveness or quality-of-life) endpoint was reported.

**Proposed claim:** The new biologic is cost-saving and high-value; payers should prefer it over standard therapy.

**Your answer (fill before peeking):**

- Warranted strength (0-4): `____`
- Framework + rule you used to get there: `________________`
- Biases / gaps you judge PRESENT (list every one; mark which you'd *require* a model to catch):
    - 
    - 
    - 
- Biases you considered but rule out as NOT operative here (your "distractors"):
    - 
- Vignette ambiguous or under-specified? (Y/N + note): `____`
- Your confidence (low/med/high): `____`

---

## 5. `rwe-competing-risks-027`  (probe)

**Evidence:** In a cohort of adults aged 75 and over followed for 10 years, the proportion of patients receiving an incident dementia diagnosis was lower among users of Drug C than among non-users. Over the same period, Drug C users had substantially higher all-cause mortality than non-users. The analysis reported the observed proportion diagnosed with dementia in each group.

**Proposed claim:** Drug C reduces the risk of developing dementia.

**Your answer (fill before peeking):**

- Warranted strength (0-4): `____`
- Framework + rule you used to get there: `________________`
- Biases / gaps you judge PRESENT (list every one; mark which you'd *require* a model to catch):
    - 
    - 
    - 
- Biases you considered but rule out as NOT operative here (your "distractors"):
    - 
- Vignette ambiguous or under-specified? (Y/N + note): `____`
- Your confidence (low/med/high): `____`

---

## 6. `rwe-surrogate-cast-028`  (anchored)

**Evidence:** After myocardial infarction, the frequency of ventricular premature depolarizations (ventricular ectopy) is a strong, consistent observational predictor of sudden cardiac death. Class I antiarrhythmic drugs reliably suppress ventricular ectopy, and a mechanistic rationale links ectopy to the initiation of fatal ventricular arrhythmias.

**Proposed claim:** Because these antiarrhythmic drugs suppress ventricular ectopy, they will reduce mortality in patients after myocardial infarction.

**Your answer (fill before peeking):**

- Warranted strength (0-4): `____`
- Framework + rule you used to get there: `________________`
- Biases / gaps you judge PRESENT (list every one; mark which you'd *require* a model to catch):
    - 
    - 
    - 
- Biases you considered but rule out as NOT operative here (your "distractors"):
    - 
- Vignette ambiguous or under-specified? (Y/N + note): `____`
- Your confidence (low/med/high): `____`

---

## 7. `rwe-target-trial-029`  (probe)

**Evidence:** A linked claims-and-EHR study emulates a target trial comparing Drug A with an active comparator, Drug B, for a clinical outcome. Eligibility, treatment strategies, and time zero are explicitly specified; the analysis is restricted to new users. Patients are matched on a propensity score built from roughly 120 covariates including laboratory values, prior health-care utilization, and comorbidities, and covariate balance is achieved (all standardized mean differences < 0.05). Two pre-specified negative control outcomes show no association with treatment. The E-value for the point estimate is 2.1: an unmeasured confounder would need to be associated with both treatment and outcome by a risk ratio of at least 2.1, beyond the measured covariates, to fully explain away the result. Drug A is associated with a 20% lower rate of the outcome.

**Proposed claim:** Drug A causes a reduction in the outcome relative to Drug B.

**Your answer (fill before peeking):**

- Warranted strength (0-4): `____`
- Framework + rule you used to get there: `________________`
- Biases / gaps you judge PRESENT (list every one; mark which you'd *require* a model to catch):
    - 
    - 
    - 
- Biases you considered but rule out as NOT operative here (your "distractors"):
    - 
- Vignette ambiguous or under-specified? (Y/N + note): `____`
- Your confidence (low/med/high): `____`

---

## 8. `rwe-healthy-adherer-030`  (anchored)

**Evidence:** In a large claims-database study, patients adherent to their statin therapy (proportion of days covered at least 80%) had substantially lower all-cause mortality than non-adherent patients, after adjustment for measured comorbidities and demographics.

**Proposed claim:** Statin adherence reduces mortality; interventions to improve adherence will therefore lower death rates.

**Your answer (fill before peeking):**

- Warranted strength (0-4): `____`
- Framework + rule you used to get there: `________________`
- Biases / gaps you judge PRESENT (list every one; mark which you'd *require* a model to catch):
    - 
    - 
    - 
- Biases you considered but rule out as NOT operative here (your "distractors"):
    - 
- Vignette ambiguous or under-specified? (Y/N + note): `____`
- Your confidence (low/med/high): `____`

---

## Disagreement log (fill during the compare step)

| item | field (strength / planted / distractor / fact) | you said | I drafted | resolution |
|---|---|---|---|---|
|  |  |  |  |  |
