"""
db.py - SQLite storage for job postings.

One table, `jobs`. Each posting gets a stable id like "greenhouse:12345",
so fetching the same posting twice never creates a duplicate.

Lifecycle of a row:
  fetch_jobs.py inserts it      -> status = 'new', score = NULL
  score_jobs.py scores it       -> score, tier, score_json, scored_at filled
  digest.py reports it          -> status = 'reported'
"""

import json
import os
import sqlite3
from datetime import datetime

DB_PATH = "data/jobs.db"


def connect():
    """Open the database (creating the folder and table if needed)."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row          # rows behave like dicts: row["title"]
    conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id          TEXT PRIMARY KEY,   -- "source:external_id"
            source      TEXT NOT NULL,      -- adzuna / greenhouse / lever / ashby
            company     TEXT,
            title       TEXT,
            location    TEXT,
            url         TEXT,
            description TEXT,
            posted_at   TEXT,
            fetched_at  TEXT NOT NULL,
            score       REAL,
            tier        INTEGER,
            score_json  TEXT,               -- full JSON from score_jobs.py
            scored_at   TEXT,
            status      TEXT DEFAULT 'new'  -- new / reported
        )
    """)
    return conn


def add_job(conn, job: dict) -> bool:
    """Insert a job. Returns True if it was new, False if we already had it."""
    cur = conn.execute(
        """INSERT OR IGNORE INTO jobs
           (id, source, company, title, location, url, description, posted_at, fetched_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            job["id"], job["source"], job.get("company"), job.get("title"),
            job.get("location"), job.get("url"), job.get("description"),
            job.get("posted_at"), datetime.now().isoformat(),
        ),
    )
    return cur.rowcount == 1    # 0 means the id already existed (ignored)


def get_unscored(conn) -> list:
    """Jobs that have been fetched but not scored yet."""
    return conn.execute("SELECT * FROM jobs WHERE score IS NULL").fetchall()


def save_score(conn, job_id: str, result: dict):
    """Store the scorer's output for one job."""
    conn.execute(
        """UPDATE jobs SET score = ?, tier = ?, score_json = ?, scored_at = ?
           WHERE id = ?""",
        (
            result.get("score"), result.get("tier"),
            json.dumps(result, ensure_ascii=False),
            datetime.now().isoformat(), job_id,
        ),
    )


def get_unreported(conn) -> list:
    """Scored jobs not yet included in a digest, best first."""
    return conn.execute(
        """SELECT * FROM jobs
           WHERE score IS NOT NULL AND status = 'new'
           ORDER BY score DESC"""
    ).fetchall()


def mark_reported(conn, job_ids: list):
    conn.executemany(
        "UPDATE jobs SET status = 'reported' WHERE id = ?",
        [(i,) for i in job_ids],
    )
