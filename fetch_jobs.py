"""
fetch_jobs.py - collect job postings into data/jobs.db.

Two kinds of sources:
  1. Adzuna (broad search across many job sites). Needs a free API key.
     Note: Adzuna returns only a SHORT snippet of each description.
  2. Company job boards on Greenhouse, Lever, or Ashby (your watchlist in
     companies.yaml). Public, no key needed, and they return FULL descriptions.

Run:  python fetch_jobs.py
"""

import html
import os
import time

import requests
import yaml
from bs4 import BeautifulSoup
from dotenv import load_dotenv

import db

load_dotenv()

TIMEOUT = 30            # seconds to wait for any website before giving up
MAX_DESC_CHARS = 15000  # cap stored description length (keeps scoring cost down)

# On-site/hybrid search areas for Adzuna, plus a separate "remote" search.
ADZUNA_LOCATIONS = ["California", "Washington", "Oregon", "Boston"]
ADZUNA_MAX_DAYS_OLD = 7  # pipeline runs every 3 days; overlap is fine (dedupe)

# Company boards can list hundreds of jobs (sales, legal, ...). Keep only titles
# containing one of these words, so we don't pay to score irrelevant jobs.
TITLE_KEYWORDS = [
    "scientist", "data", "machine learning", " ml ", " ai ", "research",
    "geolog", "geochem", "geoscien", "geophys", "analyst", "intern",
    "statistic", "quantitative", "modeling", "modeler",
]


# ---------- helpers ----------

def clean_html(raw: str) -> str:
    """Turn HTML (possibly HTML-escaped, as Greenhouse sends it) into plain text."""
    if not raw:
        return ""
    text = BeautifulSoup(html.unescape(raw), "html.parser").get_text("\n")
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)[:MAX_DESC_CHARS]


def title_is_relevant(title: str) -> bool:
    # Spaces on both sides let short keywords like " ai " match whole words
    # only ("AI Engineer" yes, "Retail Associate" no). Punctuation becomes a
    # space so "ML/AI" and "(AI)" still match.
    t = " " + "".join(ch if ch.isalnum() else " " for ch in (title or "").lower()) + " "
    return any(k in t for k in TITLE_KEYWORDS)


def get_json(url: str, params: dict = None):
    resp = requests.get(url, params=params, timeout=TIMEOUT)
    resp.raise_for_status()      # turns HTTP errors (404, 500...) into exceptions
    return resp.json()


# ---------- source 1: Adzuna ----------

def fetch_adzuna(titles: list) -> list:
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")
    if not app_id or not app_key:
        print("  Adzuna: skipped (ADZUNA_APP_ID / ADZUNA_APP_KEY not in .env)")
        return []

    searches = [(t, loc) for t in titles for loc in ADZUNA_LOCATIONS]
    searches += [(f"remote {t}", None) for t in titles]

    jobs = []
    for what, where in searches:
        params = {
            "app_id": app_id,
            "app_key": app_key,
            "what": what,
            "results_per_page": 50,
            "max_days_old": ADZUNA_MAX_DAYS_OLD,
            "content-type": "application/json",
        }
        if where:
            params["where"] = where
        try:
            data = get_json("https://api.adzuna.com/v1/api/jobs/us/search/1", params)
        except requests.RequestException as e:
            print(f"  Adzuna error for '{what}' / {where}: {e}")
            continue
        for r in data.get("results", []):
            jobs.append({
                "id": f"adzuna:{r['id']}",
                "source": "adzuna",
                "company": r.get("company", {}).get("display_name"),
                "title": r.get("title"),
                "location": r.get("location", {}).get("display_name"),
                "url": r.get("redirect_url"),
                "description": clean_html(r.get("description", "")),  # snippet only
                "posted_at": r.get("created"),
            })
        time.sleep(1)    # be polite: one request per second
    return jobs


# ---------- source 2: company boards ----------

def fetch_greenhouse(name: str, token: str) -> list:
    data = get_json(f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs",
                    {"content": "true"})
    return [{
        "id": f"greenhouse:{j['id']}",
        "source": "greenhouse",
        "company": name,
        "title": j.get("title"),
        "location": (j.get("location") or {}).get("name"),
        "url": j.get("absolute_url"),
        "description": clean_html(j.get("content", "")),
        "posted_at": j.get("updated_at"),
    } for j in data.get("jobs", [])]


def fetch_lever(name: str, token: str) -> list:
    data = get_json(f"https://api.lever.co/v0/postings/{token}", {"mode": "json"})
    jobs = []
    for j in data:
        # Lever splits the description into an intro plus titled lists.
        parts = [j.get("descriptionPlain", "")]
        for lst in j.get("lists", []):
            parts.append(lst.get("text", ""))
            parts.append(clean_html(lst.get("content", "")))
        parts.append(j.get("additionalPlain", ""))
        jobs.append({
            "id": f"lever:{j['id']}",
            "source": "lever",
            "company": name,
            "title": j.get("text"),
            "location": (j.get("categories") or {}).get("location"),
            "url": j.get("hostedUrl"),
            "description": "\n".join(p for p in parts if p)[:MAX_DESC_CHARS],
            "posted_at": str(j.get("createdAt", "")),   # milliseconds since 1970
        })
    return jobs


def fetch_ashby(name: str, token: str) -> list:
    data = get_json(f"https://api.ashbyhq.com/posting-api/job-board/{token}")
    jobs = []
    for j in data.get("jobs", []):
        location = j.get("location") or ""
        if j.get("isRemote"):
            location = f"{location} (Remote)".strip()
        jobs.append({
            "id": f"ashby:{j['id']}",
            "source": "ashby",
            "company": name,
            "title": j.get("title"),
            "location": location,
            "url": j.get("jobUrl"),
            "description": (j.get("descriptionPlain") or "")[:MAX_DESC_CHARS],
            "posted_at": j.get("publishedAt"),
        })
    return jobs


BOARD_FETCHERS = {"greenhouse": fetch_greenhouse, "lever": fetch_lever, "ashby": fetch_ashby}


def fetch_company_boards(companies: list) -> list:
    jobs = []
    for c in companies:
        fetcher = BOARD_FETCHERS.get(c.get("ats", "").lower())
        if not fetcher:
            print(f"  {c.get('name')}: unknown ats '{c.get('ats')}', skipped")
            continue
        try:
            found = fetcher(c["name"], c["token"])
        except requests.RequestException as e:
            print(f"  {c['name']}: error ({e})")
            continue
        relevant = [j for j in found if title_is_relevant(j["title"])]
        print(f"  {c['name']}: {len(found)} jobs, {len(relevant)} with relevant titles")
        jobs.extend(relevant)
    return jobs


# ---------- main ----------

def main():
    with open("profile.yaml", encoding="utf-8") as f:
        profile = yaml.safe_load(f)
    companies = []
    if os.path.exists("companies.yaml"):
        with open("companies.yaml", encoding="utf-8") as f:
            companies = yaml.safe_load(f) or []

    print("Fetching Adzuna...")
    adzuna_jobs = fetch_adzuna(profile.get("target_titles", []))
    jobs = [j for j in adzuna_jobs if title_is_relevant(j["title"])]
    print(f"  Adzuna: {len(adzuna_jobs)} results, {len(jobs)} with relevant titles")
    print("Fetching company boards...")
    jobs += fetch_company_boards(companies)

    conn = db.connect()
    new = sum(db.add_job(conn, j) for j in jobs)   # True counts as 1
    conn.commit()
    conn.close()
    print(f"\nDone: {len(jobs)} fetched, {new} new (others were already saved).")


if __name__ == "__main__":
    main()
