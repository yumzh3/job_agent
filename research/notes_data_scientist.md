# Interview prep: data scientist

20 notes · 20 new in the last 7 days · updated 2026-11-09

**Contents:** Technical / ML (2) · Statistics (4) · Coding (2) · Case studies (1) · Behavioral (2) · Company-specific (5) · Resources (4)

## Technical / ML

### Entry-level ML interview set: normalization, dimensionality reduction, EDA, model choice, CNN theory
saved 2026-11-05 · [source](https://builtin.com/data-science/data-science-and-machine-learning-interview-questions) · **new**

Written by a master's-level grad who interviewed for entry-level DS/ML/NLP/CV roles at Amazon, Tesla, Samsung, Uber, Huawei and startups. Questions asked: why normalize data (equal feature weighting in the loss, better convergence); explain dimensionality reduction and its benefits (storage, speed, redundancy removal, visualization, less overfitting); handle missing/corrupted data (drop vs impute; pandas isnull/dropna/fillna); explain a clustering algorithm; how to do EDA (coarse-to-fine: df.info, class imbalance, distributions, pairwise plots, PCA, then start with simple baselines like linear regression/Naive Bayes before SVM/trees/NN, check ROC/precision/recall); how to choose a model (no free lunch); handle imbalanced data; for CV roles: why convolutions vs FC layers, translation invariance, max-pooling, residual nets, batch norm, small 3x3 kernels. Closing questions were project-based: 'explain your current research - what worked, what didn't, future directions?' A strong answer for a geochemist: prepare an EDA walkthrough using a geochemical dataset (compositional data, missing values below detection limit) and a research explanation with failures and next steps.

### Classifier with 98% accuracy on fraud data / imbalanced classes and leakage
saved 2026-11-05 · [source](https://copilotinterview.com/blog/data-scientist-interview-questions) · **new**

Question: "Your classifier has 98% accuracy on fraud data. Is it good?" Strong answer: ask about class balance first (a majority-class baseline may already score ~98%), then use precision, recall, PR-AUC, confusion matrix, threshold tuning tied to cost of each error type, class weights/resampling, stratified CV. Companion questions: What is data leakage and how have you caught it (features unavailable at prediction time, time-based split violations); L1 vs L2 regularization (L1 sparsity/feature selection, L2 smooth shrinkage); random forest (bagging) vs gradient boosting (sequential residual correction); how would you detect a deployed model degrading (input/prediction drift, delayed labels, retraining plan). For a geoscientist: leakage via spatial autocorrelation between train/test samples (use spatial/grouped CV) is a good example.

## Statistics

### Correlation vs causation, Type I/II error, and "8 heads in 10 flips" exact-test question
saved 2026-11-09 · [source](https://www.interviewpilot.app/interview-guides/data-scientist) · **new**

From Interview Pilot's DS guide (updated May 2026). Three easy/medium stats questions with model answers: (1) Correlation vs causation: strong answer names confounding, reverse causality, selection bias, and proposes RCT / natural experiment / IV / RDD / diff-in-diff; example: push notifications and retention; follow-ups: sources of confounding, how to test causality. (2) Type I vs Type II error: false positive vs false negative, alpha vs power (1-beta), sample size trade-off, and tie the acceptable error to cost (risky checkout change vs low-risk UI tweak; medical diagnosis). (3) A coin lands heads 8/10 times - is it biased? Null p=0.5; P(>=8 heads)=56/1024≈5.5%; two-sided ≈10.9%, so not significant at 5%. Also defines p-value (not P(null true)), CI (method coverage over repeated samples), power, selection bias. Useful for a geochemist: practise computing exact binomial tail probabilities by hand and stating interpretations carefully.

### Probability screen staples: coin/disease Bayes, HH vs TH, expected rolls, ants, MLE of exponential
saved 2026-11-09 · [source](https://www.nicksingh.com/posts/40-probability-statistics-data-science-interview-questions-asked-by-fang-wall-street) · **new**

Nick Singh (DataLemur) list of 40 probability/stats questions tagged by company. Probability examples: fair vs two-tailed coin, 5 tails in a row, P(unfair) (Facebook, Bayes); HH vs TH coin game (Lyft); disease 1/1000 with 98% sensitivity & 1% false-positive, P(disease | positive) (Amazon); expected rolls to see all 6 faces (Facebook); expected flips to get HH (Two Sigma); three ants on triangle no collision (Bloomberg); fair odds from biased coin (Airbnb); A with n+1 coins vs B with n coins (Robinhood). Stats examples: explain a confidence interval to non-technical audience (Facebook), correlated predictors in multiple regression (Two Sigma), p-value in layman's terms (Uber), MLE of lambda for exponential lifetimes (Stripe), derive mean/variance of U(a,b) (Lyft), MLE vs MAP (Uber). Page also lists what to review: counting/combinatorics, expectation/variance/covariance, Uniform/Normal/Poisson/Binomial/Geometric, CLT, p-values, CIs, Type I/II errors, linear regression, MLE, Bayesian stats. Strong answers state the model/distribution, set up the conditioning (Bayes table) and show the derivation. Good fit for a PhD with solid stats background: practise out loud. Note: page date not shown (undated), but content is evergreen fundamentals.

### Core stats conceptual set: central tendency, correlation, outliers, hypothesis test, CI, CLT
saved 2026-11-05 · [source](https://www.tryexponent.com/blog/data-science-interview-questions) · **new**

Exponent/Aced guide (compiled from real candidate questions; input from Amazon, Google, Tinder, BCG, Instacart DS). Stats round has numerical, conceptual and applied question types. Examples: mean vs median in positively skewed data (mean larger, outlier-sensitive); interpret correlation of +0.8 (linear, standardized; not causation; note the guide's '80% of increase' phrasing is loose - be precise, r^2=0.64); detect outliers (1.5xIQR rule, z-score); design a hypothesis test (hypotheses, test choice, alpha, statistic, critical region/p-value, interpretation); define p-value; Type I vs II; CLT and why it underpins tests; correct interpretation of 95% confidence interval (frequentist repeated-sampling meaning). Also a Tinder DS question: determine sample size for an experiment. Practice explaining each in plain words then with math.

### Peeking at A/B test results daily and stopping at p<0.05
saved 2026-11-05 · [source](https://copilotinterview.com/blog/data-scientist-interview-questions) · **new**

Question: "What goes wrong if you check A/B results every day and stop when p is below 0.05?" Strong answer: repeated peeking inflates the false-positive (Type I) rate; fixes are a pre-registered fixed horizon with sample size from power analysis, or sequential testing / alpha-spending methods. Related questions in the same set: what is power and what drives it (sample size, effect size, variance, alpha); you tested 20 metrics and one is significant (multiple comparisons: Bonferroni, FDR); when would you NOT run an A/B test (low traffic, network effects, ethics); Simpson's paradox. Geochem angle: relate to multiple-testing when screening many element/isotope variables.

## Coding

### Python coding-screen question bank: arrays/strings, Kadane, combinations, sample-from-normal histogram, apply vs applymap
saved 2026-11-05 · [source](https://github.com/youssefHosni/Data-Science-Interview-Questions-Answers/blob/main/Python%20Interview%20Questions%20&%20Answers%20for%20Data%20Scientists.md) · **new**

GitHub repo (youssefHosni) Python list for DS interviews, 15 questions. Typical asks: (1) intersection of two arrays (use sets); (2) find duplicates in an array (seen-set pass, O(n)); (3) max product of three numbers (consider two negatives - compare top3 product vs two smallest x largest); (4) max contiguous subarray sum (Kadane's algorithm, O(n)); (5) tuples vs lists (mutability, memory); (6) Euclidean distance between two Series via numpy; (7) k-combinations of 1..n (itertools.combinations or recursion/backtracking); (8) generate N samples from a normal distribution and plot histogram (np.random.normal + plt.hist, mention seed and doing it from scratch via Box-Muller); (9) apply vs applymap (elementwise on DataFrame vs row/column-wise; note applymap is now DataFrame.map in newer pandas); (10) first recurring character (use set, not repeated .count which is O(n^2)); (11) recursive factorial with edge cases (negative returns -1); (12) longest increasing path in a matrix (DFS + memoization); (13) Flask; (15) ways to handle missing data. Strong answers state time/space complexity and edge cases, and prefer set/hash-map solutions. Good for a PhD without CS background to rehearse; date of repo undetermined (reference resource).

### SQL screen staples: second-highest salary (DENSE_RANK vs LIMIT/OFFSET) and finding duplicate emails
saved 2026-11-05 · [source](https://www.dataquest.io/blog/data-scientist-interview-questions/) · **new**

Dataquest guide (Oct 30, 2026) lists 31 DS questions by round; the SQL screen is typically in a shared online editor. Q1: 'Given an employees table with tied salaries, return the second-highest salary.' Strong answer: DENSE_RANK() OVER (ORDER BY salary DESC) in a subquery (WHERE runs before window functions) and SELECT DISTINCT; explain why plain LIMIT 1 OFFSET 1 fails with ties (skips a row, not a salary) - fix with DISTINCT; generalize to Nth-highest; handle no-such-salary case by wrapping to return NULL. Q2: 'Find emails that appear more than once in users table.' Strong answer: GROUP BY LOWER(email) HAVING COUNT(*)>1 (HAVING not WHERE because filtering after aggregation; normalize case or you miss KIM@example.com); follow-up: which duplicate to keep (oldest/most recent). The guide maps rounds: SQL screen, stats/experiments, ML, Python (pandas bucket counts by grade, small functions like palindrome check with regex), product case, behavioral.

## Case studies

### Product case: WAU dropped 10% - how do you investigate? (+ SQL retention query)
saved 2026-11-05 · [source](https://copilotinterview.com/blog/data-scientist-interview-questions) · **new**

Case/SQL round items: "Weekly active users dropped 10%. How do you investigate?" Strong answer: check data quality/instrumentation/logging first, then segment by platform, region, user type, cohort, then look at releases/seasonality/external events; state hypotheses before computing. Also: write 7-day retention by signup cohort (define 'retained' first; date joins and conditional aggregation); second-highest salary per department (DENSE_RANK, tie handling); rolling 7-day average per user in pandas (sort, groupby + rolling); measure success of a recommendation feature (one primary metric, guardrails, novelty effect). Typical loop: recruiter screen, SQL/Python technical screen, stats & experiments, ML, case, behavioral, sometimes take-home.

## Behavioral

### Presenting PhD research in a 20-minute verbal industry interview (5-part structure)
saved 2026-11-05 · [source](https://yongzx.substack.com/p/ai-research-internship-search-as) · **new**

From a CS PhD student's account of PhD research-internship interviews (Google, Meta AI, Salesforce, Adobe, Pinterest, etc.). Research interviews usually took ~20 minutes or less; some companies asked candidates to present a paper they did NOT author. Slides usually weren't needed unless the recruiter emailed otherwise. Suggested structure: (1) general problem, (2) how people currently solve it and shortcomings, (3) your solution in one sentence, (4) significance in one sentence, (5) then details: method, experimental setup, results. Keep it brief, use short sentences, leave room for the interviewer to interrupt so it becomes a discussion. Prep tips from the same source: re-implement basic ML algorithms from scratch, refresh bias-variance, SVM, precision/recall, AUC; practice DS&A (Blind 75/NeetCode) for companies that ask it; referrals helped get past resume screens; big tech intern interviews often start in Dec or later. Geochemist action: draft a 5-part version of your thesis using non-geoscience vocabulary and also prepare a paper-walkthrough of someone else's ML paper.

### Academia-to-industry transition questions (Insight Data Science style)
Insight Data Science · saved 2026-11-05 · [source](https://dataford.io/interview-guides/insight-data-science/data-scientist) · **new**

Typical PhD-transition questions (Insight Data Science guide): Why do you want to move from academia to data science? Professional goals for next 2-5 years? Which sectors interest you? Explain your complex PhD research to a non-technical person (e.g. your grandmother). Also commonly asked there: statistical significance in hypothesis testing, design an experiment for a product change (hard, very common), validate an ML model, purpose of cross-validation, bias-variance tradeoff, handling messy datasets. Prepare a 2-min non-jargon geochemistry story framed as problem -> data -> method -> decision/impact, plus a quantitative example of messy data handling (detection limits, missing values, batch effects).

## Company-specific

### Capital One Data Science Intern process: OA, manager call (elementary ML), Power Day
Capital One · saved 2026-11-09 · [source](https://www.glassdoor.com/Interview/Capital-One-Data-Science-Intern-Interview-Questions-EI_IE3736.0,11_KO12,31.htm) · **new**

Glassdoor reports (Capital One DS Intern, page updated 3 Nov 2026; 2025-26 interviews). Process: online assessment with four Python data-science coding problems (reported very hard / near impossible to finish fully, but partial credit still passed), HR call/background check, then possible wait of ~3 months to be matched to a team, a 30-min hiring-manager call (elementary ML: boosting trees, neural networks, logistic regression; 'tell me about your experience'), then Power Day of 4 consecutive one-hour rounds: coding/role-play round, business-insight (case) round, and manager call on behavior/culture fit. Average difficulty 3.2/5; avg ~39 days to hire. Capital One also lists a Summer 2027 PhD AI Engineering Internship. Prep: timed pandas/Python problem solving with partial solutions, ML fundamentals for boosted trees/NN/logistic regression, and a business-case structure (ties to Capital One-heavy statistics questions in credit-risk framing).

### Microsoft PhD summer DS intern (Stats PhD): OA + 3 resume-driven rounds, precision-recall curve coding
Microsoft · saved 2026-11-09 · [source](https://prachub.com/interview-experiences/microsoft-phd-summer-intern-data-scientist-interview-experience-oa-then-three-back-to-back-rounds-offer-a-month-later) · **new**

PracHub report (interview Jan 2026, published Aug 2026), offer received. Timeline: HackerRank OA (one LeetCode-style + one data-processing problem) -> three back-to-back rounds -> offer a month later. R1: 30 min behavioral + 15 min ML fundamentals (KNN and PCA), no coding. R2: 35 min deep-dive on resume projects + 20 min coding: compute and plot a precision-recall curve (candidate had to recall definition of recall; practise implementing precision/recall/thresholds from scratch and with sklearn+matplotlib). R3: 15 min resume + 15 min rapid-fire LLM fundamentals. No SQL/LeetCode in the live rounds. Key lesson: nearly every question, including behavioral ones, was pulled back to the research projects, with technical follow-ups; the candidate was weakest on ML fundamentals outside the resume. Prep: be able to explain each project's setup concisely to non-experts, and refresh KNN (tuning k, distance, scaling), PCA, PR vs ROC metrics.

### DoorDash new-grad DS/ML loop: take-home + ML round + 2 'business intuition' A/B rounds
DoorDash · saved 2026-11-05 · [source](https://www.teamblind.com/post/doordash-new-grad-ds-ml-rant-1b3cnmsa) · **new**

Blind account (Feb 2021) from a new-grad (master's) DoorDash DS/ML candidate: the process began with a take-home advertised as 6 hours that took ~20 hours; then a virtual onsite with 1 ML round and 2 'business intuition' rounds. ML round drew on methods from coursework and DoorDash/Lyft/Uber Eats engineering blogs (candidate spent ~60 hours reading them). Business-intuition rounds asked very specific A/B testing scenarios with made-up metrics (non-standard experiment design), which a candidate without experiment experience struggled with. Commenters advise: A/B testing questions are standard at Bay Area tech DS roles; read 'Trustworthy Online Controlled Experiments' (Kohavi); study company case studies/engineering blogs; practise communicating business implications; note that 2 product-sense rounds signal an experimentation-heavy analytics DS role rather than a pure ML role. Prep for a geochemist: learn randomization, sample size/power, metric choice, interference/network effects, and how to reason about guardrail metrics even without industry experience. Anecdotal, 2021.

### Microsoft Data & Applied Scientist PhD intern interview format (Blind thread)
Microsoft · saved 2026-11-05 · [source](https://www.teamblind.com/post/help-microsoft-data-scientist-intern-interview-hfry1lcw) · **new**

Blind thread (Feb 2021) from a PhD grad facing a Microsoft Data & Applied Scientist intern interview: recruiter said 4 rounds of 60 min. A former D&AS PhD intern (summer 2019) reported four ~45-min rounds covering: (1) ML algorithms and performance metrics, (2) experimental design, (3) open-ended case studies, (4) more structured/linear case studies; no coding rounds for them, though other product areas had a coding round. Team isn't always known in advance; each team hires independently. Another commenter: applied ML team -> recap ML basics; analytical DS team -> recap SQL; the last round may be with the hiring manager with more design/abstract questions. Intern rigor equals full-time because most interns convert. Prep: ML algorithms + metrics, A/B/experimental design, open-ended case reasoning, SQL refresher, and ask the recruiter which team/product area. Note: 2021 anecdotal data, so confirm current format.

### FanDuel: design an ML monitoring system for a fantasy sports app
FanDuel · saved 2026-11-05 · [source](https://www.tryexponent.com/blog/data-science-interview-questions) · **new**

Asked at FanDuel: "How would you design an ML monitoring system for a fantasy sports app, taking into account outliers, data quality, and drift?" Strong answer covers: input data validation (schema, missingness, range checks), outlier detection (IQR/z-score) on features, feature/prediction drift metrics (PSI, KS test), concept drift detection with delayed labels, performance dashboards and alert thresholds, retraining triggers and rollback. Analogy for a geochemist: instrument drift/QC standards in analytical labs.

## Resources

### PracHub DS statistics & math question bank (company-tagged, Sept 2026 update)
saved 2026-11-09 · [source](https://prachub.com/positions/data-scientist/categories/statistics-and-math) · **new**

PracHub's Data Scientist Statistics & Math category: ~500 questions from 81 companies (Meta, Capital One, Google, Uber, Citadel, Waymo), last updated 30 Sep 2026; 81% readable without premium. Themes: explain why a comment-count distribution is right-skewed not normal; probability of a fourth success after three; who is missing from a survey sample (selection bias); what a p-value does/doesn't say; regularisation, resampling, metrics for imbalanced classifiers; Poisson mean/variance; compare two rare-event rates with different exposure (e.g., incidents per mile, Waymo); Google: explain p-values and CIs in simple linear regression. Difficulty spread from easy definitions (116) to hard derivations (88); Capital One leans credit-risk framing, Citadel leans expected value/combinatorics. Use it for targeted practice of stats answered out loud with no code. Caveat: page contains heavy marketing/testimonials; treat claims of 'exact questions' skeptically.

### Four-hour plan for a time-boxed DS take-home (SQLPad)
saved 2026-11-05 · [source](https://sqlpad.io/tutorial/take-home-data-science-assignment-tips/) · **new**

SQLPad guide (updated Oct 2026) with a 240-minute schedule: 0-20 scope the brief/assumptions; 20-65 inspect and validate data (row meaning, key uniqueness, units, missingness, join cardinality; keep raw data unchanged; log exclusions); 65-140 core answer with a simple baseline; 140-180 one sensitivity/validation check; 180-220 write report (recommendation first, then evidence, limitations); 220-240 clean-run and packaging. Key rubric points: don't mean-impute everything; fit preprocessing on training data only (leakage); validation split should resemble deployment (time-based split for forecasts, group split for repeated subjects such as samples from the same site/core); pick a decision-tied primary metric plus a segment failure check; keep test set out of model selection; separate prediction from causation (feature importance != causes); put extras in an appendix; README + reproducible run order; no employer data in public repos or external AI tools. Be ready to defend your baseline, one rejected alternative and the next check. Geochemist angle: spatial/group CV for samples from the same site is a natural talking point.

### GitHub: 36 core ML interview Q&As (regularization, boosting vs RF, PCA, drift, ARIMA)
saved 2026-11-05 · [source](https://github.com/youssefHosni/Data-Science-Interview-Questions-Answers/blob/main/Machine%20Learning%20Interview%20Questions%20&%20Answers%20for%20Data%20Scientists.md) · **new**

Free resource: youssefHosni's 'Machine Learning Interview Questions & Answers for Data Scientists' (36 questions; repo also has Statistics, Probability, Python, SQL, Deep Learning files). Highest-yield for new-grad PhD screens: L1 vs L2 regularization; bias-variance; random forest vs gradient boosting; handling outliers and missing data; logistic regression; batch/SGD/mini-batch GD; entropy/information gain; linear regression assumptions; choosing K in K-Means; precision/recall/F1 trade-off; MSE vs MAE loss; parametric vs non-parametric; kernel trick; cross-validation; imbalanced data; ROC; curse of dimensionality and PCA variants; scaling for SVM; concept vs data drift; ARIMA assumptions (relevant to geoscience time series). Use as a self-quiz: answer aloud in ~60-90 seconds each, with a concrete example from your geochemical data (e.g. regularization for many correlated element concentrations, PCA for compositional data).

### Interview Query: frequency of DS interview topics (SQL >90%, ML 85%, Python 80%)
saved 2026-11-05 · [source](https://www.interviewquery.com/p/data-science-interview-questions) · **new**

Interview Query's 110-question guide reports SQL asked in over 90% of data science interviews, machine learning 85%+, Python 80%+, plus statistics/A-B testing and data structures & algorithms. Use it to prioritize: a PhD with strong stats but weaker SQL should spend early prep time on SQL (joins, window functions, aggregation). Sample questions listed: predict customer churn, A/B test significance, feature importance analysis, clean missing data, neural network architecture, Bayesian probability, recommend similar products. Also useful: GitHub repo youssefHosni/Data-Science-Interview-Questions-Answers (ML Q&A on outlier robustness, bias-variance, imbalance, SVM scaling, concept vs data drift).
