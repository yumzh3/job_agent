"""
evals/score_eval.py - measure how well the job scorer agrees with your hand labels.

Compares evals/labels.csv (your labels) with the scores currently in data/jobs.db
and reports:
  - deal-breaker detection: caught, missed, false alarms
  - score agreement: exact, within 1 point, same band, mean absolute error, bias
  - a breakdown by source (Adzuna snippets vs full company-board postings)
  - a table of disagreements, largest first

Run from the project folder:
  python evals/score_eval.py --tag v2-baseline     # evaluate the scores as they are now
  python evals/score_eval.py --rescore --tag v3    # re-score the labeled jobs first, then evaluate

Each run writes evals/results/score_eval_<date>_<tag>.md and appends one line
to evals/results/history.csv, so you can compare prompt versions.
"""

import argparse
import csv
import json
import os
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent      # the project folder
os.chdir(ROOT)                                     # so relative paths (data/, profile.yaml) work
sys.path.insert(0, str(ROOT))                      # so "import db" finds db.py

import db  # noqa: E402

LABELS_PATH = "evals/labels.csv"
RESULTS_DIR = "evals/results"
BANDS = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]


def band(score):
    """Which 2-point band (1-2, 3-4, ...) a score falls in."""
    for lo, hi in BANDS:
        if lo <= score <= hi:
            return f"{lo}-{hi}"
    return "?"


def load_labels():
    with open(LABELS_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["label_deal_breaker"] = r["label_deal_breaker"].strip().lower() == "true"
        r["label_score"] = int(r["label_score"]) if r["label_score"].strip() else None
    return rows


def find_job(conn, label):
    """Find the labeled job in the database: by URL, else by company + title."""
    if label["url"].strip():
        rows = conn.execute("SELECT * FROM jobs WHERE url = ?", (label["url"].strip(),)).fetchall()
        if rows:
            return rows[0], len(rows)
    rows = conn.execute(
        "SELECT * FROM jobs WHERE lower(company) = lower(?) AND lower(title) = lower(?)",
        (label["company"].strip(), label["title"].strip()),
    ).fetchall()
    return (rows[0], len(rows)) if rows else (None, 0)


def rescore(conn, jobs):
    """Score the given jobs again with the current score_jobs.py prompt."""
    from score_jobs import format_job, score_job
    with open("profile.yaml", encoding="utf-8") as f:
        profile_text = f.read()
    with open("cv_summary.md", encoding="utf-8") as f:
        cv_summary = f.read()
    for job in jobs:
        try:
            result = score_job(format_job(job), profile_text, cv_summary)
        except Exception as e:
            print(f"  ERROR re-scoring {job['title']}: {e}")
            continue
        db.save_score(conn, job["id"], result)
        conn.commit()
        print(f"  {result['score']:>2} | {job['title']} - {job['company']}")


def pct(n, d):
    return f"{100 * n / d:.0f}% ({n}/{d})" if d else "n/a"


def main():
    parser = argparse.ArgumentParser(description="Evaluate the job scorer against hand labels.")
    parser.add_argument("--tag", default="run", help="name for this run, e.g. v2-baseline or v3")
    parser.add_argument("--rescore", action="store_true",
                        help="re-score the labeled jobs with the current prompt before evaluating")
    args = parser.parse_args()

    conn = db.connect()
    labels = load_labels()

    # 1. Match each label to its job in the database.
    matched, missing = [], []
    for lab in labels:
        job, n = find_job(conn, lab)
        if job is None:
            missing.append(lab)
            continue
        if n > 1:
            print(f"Note: {n} database rows match '{lab['title']}' ({lab['company']}); using the first.")
        matched.append((lab, job))

    if args.rescore:
        print(f"Re-scoring {len(matched)} labeled jobs with the current prompt...")
        rescore(conn, [job for _, job in matched])
        matched = [(lab, conn.execute("SELECT * FROM jobs WHERE id = ?", (job["id"],)).fetchone())
                   for lab, job in matched]

    # 2. Compare predictions with labels.
    rows = []
    for lab, job in matched:
        if job["score"] is None:
            missing.append(lab)
            continue
        result = json.loads(job["score_json"] or "{}")
        rows.append({
            "title": lab["title"], "company": lab["company"], "source": job["source"],
            "label_db": lab["label_deal_breaker"], "pred_db": bool(result.get("deal_breaker")),
            "label": lab["label_score"], "pred": int(job["score"]),
            "reason": lab["reason"],
        })

    # Deal-breakers
    caught = [r for r in rows if r["label_db"] and r["pred_db"]]
    missed = [r for r in rows if r["label_db"] and not r["pred_db"]]
    false_alarm = [r for r in rows if not r["label_db"] and r["pred_db"]]
    n_label_db = len(caught) + len(missed)

    # Scores: only jobs that neither you nor the scorer marked as deal-breakers
    scored = [r for r in rows if not r["label_db"] and not r["pred_db"] and r["label"] is not None]
    for r in scored:
        r["diff"] = r["pred"] - r["label"]
    n = len(scored)
    exact = sum(r["diff"] == 0 for r in scored)
    within1 = sum(abs(r["diff"]) <= 1 for r in scored)
    same_band = sum(band(r["pred"]) == band(r["label"]) for r in scored)
    mae = sum(abs(r["diff"]) for r in scored) / n if n else 0
    bias = sum(r["diff"] for r in scored) / n if n else 0

    # By source
    by_source = {}
    for r in scored:
        by_source.setdefault(r["source"], []).append(r)

    # 3. Report.
    out = [
        f"# Scorer eval · {args.tag} · {date.today().isoformat()}",
        "",
        f"{len(labels)} labels · {len(rows)} evaluated · {len(missing)} not found or not scored",
        "",
        "## Deal-breakers",
        "",
        f"- Caught: {pct(len(caught), n_label_db)}",
        f"- Missed: {len(missed)}" + "".join(f"\n  - {r['title']} · {r['company']}" for r in missed),
        f"- False alarms (dropped a job you'd keep): {len(false_alarm)}"
        + "".join(f"\n  - {r['title']} · {r['company']}" for r in false_alarm),
        "",
        f"## Scores ({n} jobs)",
        "",
        f"- Exact match: {pct(exact, n)}",
        f"- Within 1 point: {pct(within1, n)}",
        f"- Same band: {pct(same_band, n)}",
        f"- Mean absolute error: {mae:.2f} points",
        f"- Bias (scorer minus label): {bias:+.2f} points",
        "",
        "## By source",
        "",
        "| Source | Jobs | Within 1 point | Mean absolute error |",
        "| --- | --- | --- | --- |",
    ]
    for src, rs in sorted(by_source.items()):
        w1 = sum(abs(r["diff"]) <= 1 for r in rs)
        m = sum(abs(r["diff"]) for r in rs) / len(rs)
        out.append(f"| {src} | {len(rs)} | {pct(w1, len(rs))} | {m:.2f} |")

    out += ["", "## Disagreements (largest first)", "",
            "| Job | Source | Label | Scorer | Diff | Your reason |",
            "| --- | --- | --- | --- | --- | --- |"]
    for r in sorted(scored, key=lambda r: -abs(r["diff"])):
        if r["diff"] != 0:
            out.append(f"| {r['title']} · {r['company']} | {r['source']} | {r['label']} | "
                       f"{r['pred']} | {r['diff']:+d} | {r['reason']} |")
    if missing:
        out += ["", "## Not found or not scored", ""]
        out += [f"- {m['title']} · {m['company']}" for m in missing]

    report = "\n".join(out)
    print(report)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    path = f"{RESULTS_DIR}/score_eval_{date.today().isoformat()}_{args.tag}.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(report + "\n")

    history = f"{RESULTS_DIR}/history.csv"
    new_file = not os.path.exists(history)
    with open(history, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["timestamp", "tag", "jobs", "db_caught", "db_labeled", "db_false_alarms",
                        "exact", "within1", "same_band", "mae", "bias"])
        w.writerow([datetime.now().isoformat(timespec="seconds"), args.tag, n,
                    len(caught), n_label_db, len(false_alarm),
                    exact, within1, same_band, round(mae, 2), round(bias, 2)])
    print(f"\nSaved {path} and appended to {history}")
    conn.close()


if __name__ == "__main__":
    main()
