# Interview prep: applied scientist

13 notes · 13 new in the last 7 days · updated 2026-11-08

**Contents:** Technical / ML (1) · Statistics (2) · Coding (3) · Behavioral (1) · Company-specific (5) · Resources (1)

## Technical / ML

### Amazon Applied Scientist ML breadth round: tree/RF/dropout/overfitting questions
Amazon · saved 2026-11-05 · [source](https://www.geeksforgeeks.org/interview-experiences/amazon-interview-experience-for-applied-scientist/) · **new**

GeeksforGeeks write-up (campus new-grad loop Oct 2023, page updated Jul 2025). 5 rounds: DSA+resume, ML breadth, ML depth, scalable ML, ML applications/managerial. Coding: largest lexicographic substring ("ababaa" -> "babaa"); reverse linked list in groups of K (40-45 min; interviewer gave hints - talk aloud). Resume probe: metrics, loss function, why that model over others, impact on business metrics. ML breadth questions: explain decision tree and random forest; why RF beats a single tree (many deep high-variance trees, decorrelated via row/feature subsampling -> variance reduction); what is regularization and is dropout one (and derive/write equation); how dropout weights are handled at inference; when to scale inputs for NNs; given two models' fit()/eval() and new test data, how to decide which is better and which overfits (compare train vs held-out, CV, not just train-low/test-high); K-means. Candidate was rejected - lesson: need both breadth and mathematical depth, plus Leadership Principles.

## Statistics

### PracHub DS statistics bank: topics + sample questions (updated Sep 2026)
saved 2026-11-05 · [source](https://prachub.com/positions/data-scientist/categories/statistics-and-math) · **new**

PracHub's Data Scientist Statistics & Math bank (507 questions, updated 30 Sep 2026; Meta, Google, Uber, Capital One, Citadel, Waymo). Reported question themes: justify why comment-count data is right-skewed not normal (pick the distribution and defend it); probability of a 4th good response after three successes; who is missing from a survey sample (sampling bias); what a p-value does and does not tell you; regularisation, resampling, and metrics for imbalanced classifiers. Sample items: 'Explain p-values and confidence intervals in simple linear regression' (Google, Sep 2026); 'Compare two rare-event rates with different exposure' (Waymo, Sep 2026; Poisson rates with exposure/offset, rate-ratio test); 'Measure bird species segregation' (an ecology-flavored stats question, relevant to a natural-science PhD). Strong answers state assumptions, name the distribution/test, and interpret in plain language. Statistics is graded verbally (no code), so rehearse explaining out loud. Note some solutions are paywalled.

### Amazon unfair-coin to fair bits (von Neumann), study-bias, fraud-model metric questions (Dec 2025)
Amazon · saved 2026-11-05 · [source](https://dataloopr.com/blog/data-scientist-interview-questions-amazon-134/) · **new**

Dataloopr (Dec 11, 2025) collects Amazon/Tesla DS-style questions that also appear in Amazon applied-scientist screens (IGotAnOffer lists the unfair-coin item under Amazon coding/modeling; an AS intern reported a Bayesian coin-toss problem in a peer-coding screen). (1) Given a biased coin (p != 0.5), generate unbiased 0/1: von Neumann extractor - flip twice, HT->1, TH->0, discard HH/TT; works since P(HT)=P(TH)=p(1-p); expected pairs per bit = 1/(2p(1-p)), inefficient for extreme p; be able to code it. (2) Bias in a study claiming an airline has fastest boarding: selection bias, sample size, time of day, aircraft size, demographics, measurement definition, self-reported data; propose stratified analysis and significance testing. (3) Fraud-detection model with SMS confirmation: supervised binary classification (LR/RF/GBT, anomaly detection if labels sparse), class imbalance, real-time scoring, trade-off of false positives (annoyed customers) vs false negatives (loss); choose precision/recall/PR-AUC by cost, not accuracy. Also related: simulate a fair die from a biased coin, expected tosses to see HTH.

## Coding

### Microsoft Applied Scientist Intern (Feb 2026): K-means from scratch, hypothesis testing, Python debug, case study
Microsoft · saved 2026-11-05 · [source](https://www.fastprep.io/experience/2020-2026-microsoft-coreai-and-ai-ml-intern-oa-interviews-118-experiences-part-2-wl1bqu6j2d) · **new**

FastPrep report 007 (Feb 2026): phone screen on ML and LLM fundamentals, then three virtual-onsite rounds; offer. Questions: implement K-means from scratch and discuss time complexity (O(n·k·d·iterations)); business hypothesis-testing question; simple Python debugging; project discussion; open-ended case study. Related PhD intern reports from the same page: implement a precision-recall curve (Data Scientist PhD intern, Jan 2026; also KNN, PCA, LLM fundamentals), design counterfactual evaluation when A/B testing is unavailable, diagnose a sudden one-day product-metric drop, 'explain how ChatGPT is trained' (Oct 2025). Prepare to code basic ML algorithms in numpy without libraries and reason about experiments.

### Microsoft Data & Applied Scientist: Codility test (pandas + lasso/ridge/elastic net), kth largest (Apr-Jun 2024)
Microsoft · saved 2026-11-05 · [source](https://www.glassdoor.com/Interview/Microsoft-Data-and-Applied-Scientist-Interview-Questions-EI_IE1651.0,9_KO10,36.htm) · **new**

Glassdoor reports (Apr-Jun 2024), Microsoft Data and Applied Scientist. One candidate: ~2.5-hour Codility test with (1) a lengthy pandas data-manipulation task on a phone-company-style database and (2) a task on lasso, ridge and elastic net; then resume screening and a live coding round. Another: first round = 30 min technical questions from resume, then ~25 min coding (find the kth largest number - use heap/quickselect, discuss complexity). Accepted-offer Bengaluru report: 5 rounds - two DS rounds with a DS coding question, DS design round, one DSA round, hiring manager round, optional ML/coding round; topics ML basics, project walkthrough, DSA. Prep: pandas groupby/merge fluency, implement/compare L1 vs L2 vs elastic net (sparsity, correlated features, when to use), heaps/kth-largest.

### Amazon Applied Scientist ML-coding question list (PracHub, updated 2026)
Amazon · saved 2026-11-05 · [source](https://prachub.com/companies/amazon/positions/applied-scientist) · **new**

PracHub's Amazon Applied Scientist page (updated May-Aug 2026; 80 candidate-reported questions, some tagged New Grad, many Senior+ so filter) lists question titles worth practicing: implement K-means (+interval/frequency tasks); implement multi-head attention from scratch in NumPy; implement top-p (nucleus) sampling in NumPy; implement a PyTorch training loop; derive mean and variance via maximum likelihood; merge overlapping time ranges; course schedule (cycle detection in directed graph); two-sum; binary search lower/upper bound; shortest path in grid with obstacles; optimal bucket batching; evolution of NLP embeddings to LLM embeddings; design RAG end-to-end (skip S3 design as senior-level). Page describes loop as recruiter + tech phone screen, then 4-6 rounds mixing ML depth, ML breadth, coding, and Leadership Principles/Bar Raiser. Note: site is a paid platform; solutions partly locked - use titles as a checklist.

## Behavioral

### Amazon AS: PhD research deep-dive and "why that architecture" questions (Glassdoor, Sep 2026)
Amazon · saved 2026-11-05 · [source](https://www.glassdoor.com/Interview/Amazon-Applied-Scientist-Interview-Questions-EI_IE6036.0,6_KO7,24.htm) · **new**

Recent Glassdoor reports (Sep 2026): one accepted-offer candidate (Seattle) described a sequence of ML questions, LeetCode, Leadership Principles, situational cases ("what would you do solving this problem") and questions about their PhD research. Another (screen, Apr 2026) got basic AI/ML + project questions focused on justifying choices, e.g. "why did you pick that architecture?". Another process: recruiter prep call, initial coding assessment, then 5 loop interviews. Prep: a 2-minute plain-language pitch of your thesis, be able to defend every modeling choice (alternatives, ablations, trade-offs), prepare 6-8 STAR stories mapped to Leadership Principles, and practice LeetCode medium. For a geochemist: frame thesis as problem -> data -> method -> validation -> impact.

## Company-specific

### Amazon/AWS Applied Scientist virtual onsite (PhD): 40-min research talk + ML depth/breadth/open-ended (Blind, Feb 2022)
Amazon · saved 2026-11-05 · [source](https://www.teamblind.com/post/applied-scientist-amazon-interview-huyl7wdv) · **new**

Blind thread (Feb 2022, older but loop format still echoed in 2026 reports): successful candidate's virtual onsite = 40-min presentation of own research + 15 min Q&A (clear visuals, leave >=10 min at end since time management is assessed, tie to customer impact); 2 coding rounds (algorithms/DS); ML depth (interviewer probes your talk, e.g. 'why is there a normalization layer there?', often open-ended asking for plausible scientific reasoning); ML breadth (rapid-fire list of classic + DL questions, not limited to your subfield; you aren't expected to know everything); ML open-ended (hiring manager gives an Amazon-style problem to scope and propose solutions). All 5 interviews start with ~half behavioral (Leadership Principles) so prepare many STAR stories. For a geochem PhD: build the talk so a non-domain ML audience follows it, and be ready to defend every modeling choice.

### Microsoft Applied Science PhD Intern (Redmond, Feb 2026): ablation, precision/recall coding, RAG design
Microsoft · saved 2026-11-05 · [source](https://www.fastprep.io/experience/2020-2026-microsoft-coreai-and-ai-ml-intern-oa-interviews-118-experiences-part-2-wl1bqu6j2d) · **new**

FastPrep report 006 (Feb 2026): one screen then three back-to-back interviews; offer received. Topics: project + ablation-study discussion, NLP/ML fundamentals, RL/agents/metrics/regularization. Coding: (1) given [-1,-2,-4,-5,7,10] return every pair with the minimum difference (easy; sort + adjacent scan); (2) 10 animal images, API returns k files, compute precision and recall for 'dog' and handle edge cases like None or result count != k; (3) design a RAG system (agentic tool framing). Strong answer: justify ablations (what you removed and why), robust input validation, define precision/recall explicitly, and discuss RAG retrieval/eval/failure modes.

### Microsoft Applied Scientist (AS1/AS2) process: 30-min ML-grounded phone screen + design rounds (2026)
Microsoft · saved 2026-11-05 · [source](https://www.tryexponent.com/guides/microsoft-applied-scientist-as-interview) · **new**

Aced/Exponent guide (updated ~Oct 2026). Microsoft hires AS1 (entry) and AS2 (PhD, or MS + ~2 yrs). Flow: recruiter screen (30 min, team fit, technical credibility on your own work) -> 30-min technical phone screen with one interviewer: ~15 min ML-grounded coding (example reported: top-n most frequent words from a list of sentences), ~5 min CV/projects, 5-10 min ML fundamentals -> onsite panel of 3-5: hiring-manager round (ML depth/breadth, probes every CV project until gaps show, feedback/growth mindset), two end-to-end ML pipeline design rounds (data collection, preprocessing, model choice, eval, production; narrate trade-offs), optional extra coding round. Calibration is by team leaders, not an Amazon-style bar raiser. Key advice: explain models at the building-block level (mechanics, not buzzwords); Microsoft moved away from pure algorithmic puzzles for this screen.

### Motive Applied Scientist 1: ML coding on two CSVs + ML theory + scenario questions (Nov 2025)
Motive · saved 2026-11-05 · [source](https://www.geeksforgeeks.org/interview-experiences/motive-interview-experience-for-applied-scientist-1/) · **new**

GeeksforGeeks report (Nov 2025), Motive Applied Scientist 1, no LeetCode. Process: hackathon -> resume shortlist -> (1) 90-min ML coding: given two CSVs with different attributes of same entity, build a classifier (merge, dedupe, feature select, encode categoricals, logistic regression + random forest); follow-ups: why RF performs well, what happens if duplicates not removed (leakage/overfitting), what to improve (sklearn pipelines). (2) 90-min ML theory: thesis questions (IMU sensors, odometry), precision/recall and PR curve axes/area/threshold choice, regularization for trees/RF, LLM vs LSTM advantages, explain LLM architecture layer by layer, class weighting to prioritize one class, AdaBoost and adapting it, scenario questions (new PM requirement, multi-stakeholder story, external AI API with sensitive data -> mask/anonymize then build in-house model). (3) 'Top grading' deep dive on projects: model choice, fine-tuning, knowledge distillation. Good practice for a PhD with domain thesis: be ready to explain your thesis domain to ML interviewers.

### Amazon Applied Scientist intern: official OA + loop structure (Aug 2026 guide)
Amazon · saved 2026-11-05 · [source](https://prachub.com/resources/amazon-applied-scientist-intern-interview-2027-coding-ml-depth-and-behavioral-questions) · **new**

PracHub guide (Aug 21, 2026) summarizing Amazon's official student page: Applied Science Intern OA = ~70 min coding (Python/R etc. allowed; browser use logged, public docs only) + a work-styles assessment (not an ML quiz; answer consistently). Then 1-2 technical screens and a ~4 interview loop (problem solving/coding, ML depth & breadth, research/tech talk, Leadership Principles). Coding target: medium DSA (arrays, strings, hash maps, sorting, binary search, heaps, trees, graphs, intervals, basic DP). Strong answer: restate, ask constraints, baseline then improve, state complexity, test edge cases, talk aloud. ML breadth/depth topics: linear/logistic regression, trees/ensembles, bias-variance, regularization, calibration, class imbalance, cross-validation, Bayes rule, CIs, hypothesis testing, sampling bias, experiment design, choosing metrics by cost structure (precision-recall, temporal splits), plus transformers/CNNs/recsys per resume. Includes a 7-day prep plan ending with a full simulation (coding + ML depth + behavioral).

## Resources

### AI research internship hunt as PhD student: process, prep list, 20-min research talk format (Mar 2024)
saved 2026-11-05 · [source](https://yongzx.substack.com/p/ai-research-internship-search-as) · **new**

Substack post by a 3rd-year CS PhD (Mar 2024) covering interviews at Google, Meta, Adobe, Salesforce, Pinterest, etc. Process: OA/take-home (ML/DL or DS&A coding, sometimes ML MCQs) -> technical interviews (LeetCode-style or ML coding, LLM/DL questions, research presentation) -> hiring-manager behavioral. Prep: Blind 75 / NeetCode 150; reimplement basic ML algorithms; refresh bias-variance, SVM, precision/recall, AUC; read 'Attention is All You Need' and HF docs for GenAI roles. Research talk template (~20 min, verbal, leave room for Q&A): problem -> existing approaches and shortcomings -> your solution in one sentence -> significance in one sentence -> details/setup/results. Some companies ask you to present a paper you did not author. Useful for a geochem PhD translating research into an ML-audience talk. Timing note: startups open early fall, big tech later; referrals helped pass resume screen.
