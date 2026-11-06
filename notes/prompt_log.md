# Prompt log

A record of prompt changes: what went wrong, what I changed, and what happened.
Newest entries at the top.

---

## 2026-11-05 · score_jobs.py · v2 → v3: role type, location and job-type rules, measured with an eval

**Model:** claude-sonnet-5-5 · **Eval:** `evals/score_eval.py` on 20 hand-labeled jobs (`evals/labels.csv`): 17 with a score label, 3 deal-breakers

### How the problems were found

I compared 20 digest entries with their full postings and labeled each job myself (score, or deal-breaker, plus a one-line reason). `score_eval.py` then measured the v2 scorer against those labels, before any prompt change.

### What went wrong in v2

| Problem | Example | Effect |
|---|---|---|
| **Title and company lifted the band** | Lila "Research Scientist, Computational Condensed Matter Physics" scored 9 (a physics role, not DS/ML); Periodic "Scaling RL" scored 9 (LLM training, not Earth/materials) | +8 and +2 errors; all score errors pointed upward |
| **Inconsistent on identical postings** | Planet "Data Analyst" scored 1 (SF) and 3 (Arlington), same text | +2 error |
| **Deal-breakers never caught** | Contract, part-time and out-of-area on-site jobs all kept | 0 of 3 caught |
| **Requirements guessed from snippets** | Lyft: "A/B testing (typical for Lyft DS)", "pricing domain: hard gap" | Gaps listed that the posting never states |
| **Unrelated roles had no tier** | Synthires got tier 0 | A stray "Tier 0" in the digest |

### What I changed (v3)

Added to the system prompt:
1. **Role type:** decide it from responsibilities and required qualifications, not the title or company. "Research/Applied Scientist" counts as DS/AI/ML only if the core work is data science or ML; computational physics/chemistry theory, hardware/instrument engineering and BI/dashboard analyst roles do not.
2. **No guessing:** list only gaps for requirements stated in the posting; never infer what is typical for the company or role.
3. **No double counting:** neither the level mismatch nor the direction mismatch that set the band counts as a gap within the band.
4. **Location:** judge from the description as well as the Location field; acceptable if any work location fits; remote means US-only; outside the allowed areas without remote = deal-breaker.
5. **Job type:** part-time, freelance and fixed-term contract roles are deal-breakers; hourly pay alone is not (internships are often hourly).

Schema and profile:
- `tier` limited to `enum: [1, 2, 3, 4]`; new **tier 4** for roles outside DS/ML and geoscience, so tier 3 keeps one meaning (adjacent roles where my domain helps).
- `profile.yaml`: `remote (US only)` in `work_modes`; new deal-breaker "part-time, freelance, or fixed-term contract roles" (worded without a parenthesis, so it can't be misread as excluding full-time roles).

**Considered, not adopted:**
- *"When confidence is low, choose the lower number of the band."* Snippet jobs can still be strong fits (Picarro, labeled 10, is a snippet), so this would push good jobs down.
- *"A hard gap in a core requirement moves the job down one band."* My labels follow the bands as defined (e.g. Meta FAIR intern, Coulson wildfire = 9 despite core gaps), so I kept the rubric unchanged.

### Result

| Metric (17 scored jobs, 3 deal-breakers) | v2 baseline | v3 |
|---|---|---|
| Deal-breakers caught | 0 of 3 | **2 of 3** |
| False alarms (good jobs dropped) | 0 | **0** |
| Same band | 82% (14/17) | **100% (17/17)** |
| Within 1 point | 82% (14/17) | **100% (17/17)** |
| Exact match | 71% (12/17) | 76% (13/17) |
| Mean absolute error | 0.82 | **0.24** |
| Bias (scorer minus label) | +0.59 | −0.12 |

The three band-leakage errors are gone; the four remaining differences are all ±1 within the correct band. The new location rule produced no false alarms.

### A label was wrong, not the scorer

KoBold "Data Scientist - Staff or Senior (Australia)": I had labeled it a deal-breaker from the title. v3 kept it, with the reason "the description allows US-authorized remote candidates". I checked KoBold's site: the scorer was right. Label corrected (score 6, not a deal-breaker); the v2 baseline above is recalculated with the corrected label. Lesson: disagreements should be checked in both directions; an eval finds labeling errors too.

### Remaining issues (left on purpose)

- **Aditi Consulting (contract, hourly) still missed.** The snippet only hints at a contract ("may be a contract placement"), so the rule doesn't fire. It scores 1, below the digest's `--min-score 5`, so it never reaches me; a job-specific rule would be overfitting. Limitation: on Adzuna snippets, deal-breakers are caught only when the snippet states them.
- **Rule 3 is followed loosely.** KoBold (Australia) got 5 because "4+ years post-PhD is a hard gap", which is the level mismatch that already set the band. A −1 within the band; not worth another rule.

### Consistency: re-running v3

Same prompt, same model, same 20 jobs, scored a second time (`--tag v3-rerun`):

| Metric (17 scored jobs) | v2 baseline | v3 run 1 | v3 run 2 |
|---|---|---|---|
| Same band | 82% | 100% | 94% |
| Within 1 point | 82% | 100% | 94% |
| Mean absolute error | 0.82 | 0.24 | 0.41 |
| Deal-breakers caught | 0 of 3 | 2 of 3 | 2 of 3 |
| False alarms | 0 | 0 | 0 |

The gain over v2 holds in both runs, and the deal-breaker results were identical. One job flips between runs: Periodic Labs "Scaling RL" scored 7 in run 1 and 9 in run 2. It is a genuinely borderline case (AI-for-materials company, RL work aimed at scientific reasoning), so my label of 7 is defensible but not the only reasonable reading. **Reported result: band agreement 82% (v2) → 94–100% across two runs of v3, with no false alarms.**

### Model comparison: can a cheaper model do this?

Scoring costs about $0.018 per job on Sonnet (1,021 calls, $18.71 so far), so I tested Haiku with the same v3 prompt (`--tag v3-haiku`):

| Metric | Sonnet (v3) | Haiku (v3) |
|---|---|---|
| Same band | 94–100% | 62% |
| Within 1 point | 94–100% | 69% |
| Mean absolute error | 0.24–0.41 | 0.81 |
| False alarms | 0 | **1** (dropped KoBold Australia, a job I'd keep) |

Haiku moved my best match (Picarro, labeled 10) down to 7, and scored the KoBold hardware role 3 instead of 1, missing that it isn't DS/ML: judging role type from responsibilities (rule 1) needs the stronger model. **Decision: keep Sonnet.** Cost reduction will come from prompt caching instead (the system prompt, profile and CV summary are identical in every call), which doesn't change the model's output.

### Caveat and next step

These fixes were designed from the same 20 jobs they are measured on, so part of the improvement is by construction. Next: label 10 new jobs I haven't analyzed (`evals/labels_holdout.csv`) and run v3 on them once, without tuning, to check that the improvement holds on unseen jobs.

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
1. *"The band is set by role type, direction and level only. Company, location and domain do not move a role into a higher band; a non-DS/ML, non-geoscience role is 1–2 even at an ideal-direction company."*
2. *"Do not count the level mismatch that set the band as a gap when choosing between the two numbers of a band; choose using the other gaps."*

### Result (v2)

| Job | v1 | v2 | Why |
|---|---|---|---|
| Commercial & Scientific Analyst/Lead | 4 | **1** | Verdict: "the company does not lift an unrelated role out of the 1–2 band" |
| Data Scientist (Global) | 5 | **6** | Level mismatch excluded; remaining gaps only soft or learnable |
| Senior Applied Scientist | 5 | **5** | Now 5 for a stated reason: low confidence from the snippet |

### Follow-up

- The prompt doesn't say how confidence affects the score; the model chose the lower number for the snippet on its own. Planned rule: *"When confidence is low, choose the lower number of the band."*
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

### Follow-up

- These four cases become the first test cases for the fabrication checker (`evals/cv_check.py`, Tuesday).
