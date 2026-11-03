# Prompt log

A record of prompt changes: what went wrong, what I changed, and what happened.
Newest entries at the top.
# Prompt log

A record of prompt changes: what went wrong, what I changed, and what happened.
Newest entries at the top.

---

## 2026-11-01 · score_jobs.py · v1 → v2: band leakage and double counting

**Model:** claude-sonnet-5-5 · **Test jobs:** three KoBold Metals postings (one Adzuna snippet, two with full descriptions)

### What went wrong in v1

| Job | Source | v1 score | Expected by the bands | Problem |
|---|---|---|---|---|
| Commercial & Scientific Analyst/Lead | Full posting | 4 (tier 3) | 1–2 (unrelated role) | **Band leakage:** the ideal-direction company lifted a non-DS, non-geoscience role above its band. The verdict itself said "not a DS/ML or geoscience role". |
| Data Scientist (Global), Senior/Staff | Full posting | 5 (tier 1) | 5–6 | **Double counting:** being above my level set the 5–6 band, then the same fact was counted again as a hard gap, forcing the lower number. |
| Senior Applied Scientist | Adzuna snippet | 5 (tier 1) | 5–6 | Same double counting; confidence correctly marked low (snippet). |

What worked in v1:
- All three postings landed in the right tier, and the two DS roles in the right band.
- Gaps were real and specific (4+ years post-PhD, team leadership, cloud, CI/CD, Bayesian inference), with sensible severities.
- Confidence was correctly low for the Adzuna snippet, with a clear reason.
- Verdicts gave useful advice (e.g. "apply as a stretch; look for a more junior opening").

### Lessons

- **A strong factor leaks into bands that shouldn't consider it.** The model knew the analyst role was off-target but still rewarded the company. Bands need an explicit statement of what may and may not move a job between them.
- **One fact should be counted once.** If a fact decides the band, it must be excluded from the within-band decision, or every job in that band collapses to the lower number and the within-band choice carries no information.

### What I changed (v2)

Added to the system prompt:
1. *"Company, location and domain do not move an unrelated role into a higher band; an unrelated role is 1–2 even at an ideal-direction company."*
2. *"Do not count the level mismatch that set the band as a gap when choosing between the two numbers of a band; choose using the other gaps."*
- *"When confidence is low, choose the lower number of the band."*

### Result (v2)

| Job | v1 | v2 | Why |
|---|---|---|---|
| Commercial & Scientific Analyst/Lead | 4 | **1** | Verdict: "the company does not lift an unrelated role out of the 1–2 band" |
| Data Scientist (Global) | 5 | **6** | Level mismatch excluded; remaining gaps only soft or learnable |
| Senior Applied Scientist | 5 | **5** | Now 5 for a stated reason: low confidence from the snippet |

### Follow-up

- Tier 3 for the analyst role is debatable (the model counted the mining context as "domain helps"). Left as is, since it scores 1 either way.
- Known limitation: the Senior Applied Scientist came from Adzuna as a snippet; if it is also on KoBold's Greenhouse board, it is stored twice under different IDs.
- These three jobs join the hand-labeled set for the scorer eval (`evals/score_eval.py`, Tuesday).

---

## 2026-10-31 · tailor_cv.py · v1 → v2: closing fabrication loopholes

**Model:** claude-opus-5-5 · **Test jobs:** KoBold Metals (Data Scientist, senior), Amazon (Data Scientist I)

### What went wrong in v1

I checked every number, date and claim in both tailored CVs against `master_cv.md` by hand.

| # | Where | Tailored CV said | Master CV said | Verdict |
|---|---|---|---|---|
| 1 | Both CVs, clustering project | "58 element concentrations per analysis" | 32 | True, but missing from master CV |
| 2 | Amazon, COVID project | "Harvard University \| 2020" | No date | True, but missing from master CV |
| 3 | Amazon, summary | "6+ years of turning research questions into…" | No such claim | **Fabricated:** number calculated from dates |
| 4 | Amazon, summary | "technical and non-technical audiences" | Not stated | **Embellished** |

What worked in v1:
- The two CVs were clearly different: geoscience framing for KoBold, general data science framing for Amazon.
- The Bayesian rule held. For KoBold, the model listed "Bayesian inference" as a gap instead of relabeling Monte Carlo sampling as Bayesian.
- "Limited exposure" qualifiers (PyTorch/TensorFlow, R) were kept in both CVs.
- `gaps_not_addressed` was honest and specific (e.g. "4 years post-PhD", "A/B testing", "cloud computing").

### Lessons

- **Two of the four flags were not model errors.** Numbers 1 and 2 were true but were missing from the master CV, so the model drew on information it shouldn't have had a source for. Fix: added both to `master_cv.md`. The master CV must be complete, or true facts look like fabrications.
- **The model found loopholes in rules that looked strict.** "Keep numbers exactly as written" did not stop it from *calculating* a new number (6+ years from 2019–2026). Rules need to name the behavior to block, not just the goal.

### What I changed (v2)

1. Rule 3 now reads: *"Keep numbers exactly as written. Never calculate, combine, or estimate new numbers (e.g. years of experience, totals). Never change a number; if unsure, omit it."*
2. Rule 1 now adds: *"Do not add a date to any item that has none in the master CV."*
3. New final rule (self-check): *"Before answering, verify that every number, date, and named skill in the tailored CV appears in the master CV. Remove anything that doesn't."*
4. Master CV: added the 58 measured elements and the 2020 date for the COVID project.

### Result (v2)

<!-- Fill in after rerunning both jobs -->
- "6+ years": 
- "non-technical audiences": 
- Any new problems: 
- Cost per run (from data/usage.csv): 

### Follow-up

- These four cases become the first test cases for the fabrication checker (`evals/cv_check.py`, Tuesday).
