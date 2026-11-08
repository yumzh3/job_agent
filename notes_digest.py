"""
notes_digest.py - turn the agent's interview-prep notes into one readable study guide per role.

Reads research/notes.jsonl and writes research/notes_<role>.md, e.g.
research/notes_data_scientist.md: notes grouped by category, newest first,
each with its company, date and source link. Notes saved in the last 7 days
are marked "new", so after each weekly run you can see what was added.

Run:  python notes_digest.py
"""

import json
import os
import re
from collections import defaultdict
from datetime import datetime, timedelta

NOTES_PATH = "research/notes.jsonl"
OUT_DIR = "research"
NEW_DAYS = 7

# Display order and headings; any other category goes at the end.
CATEGORIES = [
    ("technical", "Technical / ML"),
    ("statistics", "Statistics"),
    ("coding", "Coding"),
    ("case_study", "Case studies"),
    ("behavioral", "Behavioral"),
    ("company_specific", "Company-specific"),
    ("resource", "Resources"),
]


def load_notes() -> list:
    if not os.path.exists(NOTES_PATH):
        return []
    with open(NOTES_PATH, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def slug(text: str) -> str:
    """'data scientist' -> 'data_scientist', safe for a file name."""
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def saved_at(note) -> datetime:
    try:
        return datetime.fromisoformat(note.get("saved_at", ""))
    except ValueError:
        return datetime.min


def format_note(note, cutoff) -> list:
    when = saved_at(note)
    new = " · **new**" if when >= cutoff else ""
    meta = []
    if note.get("company"):
        meta.append(note["company"])
    if when != datetime.min:
        meta.append(f"saved {when:%Y-%m-%d}")
    if note.get("source_url"):
        meta.append(f"[source]({note['source_url']})")
    return [
        f"### {note.get('title', '(untitled)')}",
        " · ".join(meta) + new,
        "",
        note.get("content", ""),
        "",
    ]


def write_role(role: str, notes: list, cutoff) -> str:
    by_cat = defaultdict(list)
    for n in notes:
        by_cat[str(n.get("category", "other")).lower()].append(n)

    order = [c for c, _ in CATEGORIES if c in by_cat] + sorted(c for c in by_cat if c not in dict(CATEGORIES))
    names = dict(CATEGORIES)
    n_new = sum(saved_at(n) >= cutoff for n in notes)

    out = [
        f"# Interview prep: {role}",
        "",
        f"{len(notes)} notes · {n_new} new in the last {NEW_DAYS} days · updated {datetime.now():%Y-%m-%d}",
        "",
        "**Contents:** " + " · ".join(f"{names.get(c, c.title())} ({len(by_cat[c])})" for c in order),
        "",
    ]
    for c in order:
        out += [f"## {names.get(c, c.title())}", ""]
        for n in sorted(by_cat[c], key=saved_at, reverse=True):
            out += format_note(n, cutoff)

    path = os.path.join(OUT_DIR, f"notes_{slug(role)}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    return f"{path}: {len(notes)} notes ({n_new} new)"


def main():
    notes = load_notes()
    if not notes:
        print(f"No notes found in {NOTES_PATH}.")
        return
    cutoff = datetime.now() - timedelta(days=NEW_DAYS)
    by_role = defaultdict(list)
    for n in notes:
        by_role[str(n.get("role", "unknown")).strip().lower()].append(n)
    os.makedirs(OUT_DIR, exist_ok=True)
    for role, role_notes in sorted(by_role.items()):
        print("Wrote " + write_role(role, role_notes, cutoff))


if __name__ == "__main__":
    main()
