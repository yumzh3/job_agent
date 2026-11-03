"""
digest.py - write a ranked Markdown report of newly scored jobs.

Reads scored jobs that haven't been reported yet, drops deal-breakers,
groups the rest by tier, sorts by score, and writes data/digest_<date>.md.
Then marks those jobs as reported so the next digest only shows new ones.

Run:
  python digest.py                 # normal run
  python digest.py --preview       # write the digest but DON'T mark jobs reported
  python digest.py --min-score 5   # only include jobs scoring 5 or higher
"""

import argparse
import json
import os
from collections import Counter
from datetime import date

import db

TIER_NAMES = {
    1: "Tier 1: AI/data science in Earth, climate & materials, or data-driven geoscience",
    2: "Tier 2: Core data science / ML",
    3: "Tier 3: Adjacent roles where your domain helps",
}
SEVERITY_ORDER = {"hard": 0, "learnable": 1, "soft": 2}


def load_result(row) -> dict:
    """The scorer's full JSON for one job (stored as text in score_json)."""
    try:
        return json.loads(row["score_json"] or "{}")
    except json.JSONDecodeError:
        return {}


def format_gaps(gaps: list) -> list:
    """One line per gap, hard gaps first."""
    gaps = sorted(gaps, key=lambda g: SEVERITY_ORDER.get(str(g.get("severity", "")).lower(), 3))
    return [
        f"  - **{str(g.get('severity', '?')).lower()}**: {g.get('requirement', '')}"
        + (f" ({g['note']})" if g.get("note") else "")
        for g in gaps
    ]


def format_job(row, r: dict) -> str:
    sev = Counter(str(g.get("severity", "")).lower() for g in r.get("gaps", []))
    gap_summary = ", ".join(f"{n} {s}" for s, n in sev.items()) or "no gaps"
    low = " · ⚠ low confidence: check the full posting" if str(r.get("confidence", "")).lower() == "low" else ""

    lines = [
        f"### [{row['score']:.0f}] {row['title']} · {row['company'] or 'Unknown company'}",
        f"{row['location'] or 'Location not given'} · {row['source']} · {gap_summary}{low}",
        "",
        f"**Verdict:** {r.get('verdict', '')}",
        "",
    ]
    if r.get("gaps"):
        lines += ["**Gaps:**"] + format_gaps(r["gaps"]) + [""]
    if row["url"]:
        lines += [f"[View posting]({row['url']})", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Write the job digest.")
    parser.add_argument("--preview", action="store_true",
                        help="don't mark jobs as reported")
    parser.add_argument("--min-score", type=int, default=1,
                        help="leave out jobs scoring below this")
    args = parser.parse_args()

    conn = db.connect()
    rows = db.get_unreported(conn)          # scored, not yet reported, best first

    kept, dropped = [], []
    for row in rows:
        r = load_result(row)
        if r.get("deal_breaker"):
            dropped.append((row, r))
        elif row["score"] >= args.min_score:
            kept.append((row, r))

    if not kept and not dropped:
        # Don't overwrite today's digest with an empty one.
        print("No new scored jobs since the last digest. Nothing written.")
        conn.close()
        return

    today = date.today().isoformat()
    by_tier = {}
    for row, r in kept:
        by_tier.setdefault(row["tier"], []).append((row, r))

    out = [
        f"# Job digest · {today}",
        "",
        f"{len(kept)} jobs (score ≥ {args.min_score}) · "
        f"{len(dropped)} dropped as deal-breakers · "
        f"{sum(1 for _, r in kept if str(r.get('confidence', '')).lower() == 'low')} low confidence",
        "",
    ]
    for tier in sorted(by_tier, key=lambda t: (t is None, t)):
        jobs = by_tier[tier]                 # already sorted by score (from the query)
        out += [f"## {TIER_NAMES.get(tier, f'Tier {tier}')} ({len(jobs)})", ""]
        out += [format_job(row, r) for row, r in jobs]

    if dropped:
        reasons = Counter((r.get("deal_breaker_reason") or "no reason given") for _, r in dropped)
        out += ["## Dropped as deal-breakers", ""]
        out += [f"- {n} × {reason}" for reason, n in reasons.most_common(10)]
        out += [""]

    os.makedirs("data", exist_ok=True)
    path = f"data/digest_{today}.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    if not args.preview:
        db.mark_reported(conn, [row["id"] for row, _ in kept + dropped])
        conn.commit()
    conn.close()

    print(f"Wrote {path}: {len(kept)} jobs, {len(dropped)} deal-breakers dropped"
          + (" (preview: nothing marked as reported)" if args.preview else ""))


if __name__ == "__main__":
    main()
