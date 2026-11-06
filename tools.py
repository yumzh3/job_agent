import json, os
from datetime import datetime
import requests
from bs4 import BeautifulSoup

NOTES_PATH = "research/notes.jsonl"
MAX_PAGE_CHARS = 8000

# ---- the functions ----
def fetch_page(url: str) -> str:
    try:
        resp = requests.get(url, timeout=20, headers={"User-Agent": "job-agent-research/0.1"})
        resp.raise_for_status()
    except requests.RequestException as e:
        return f"Error: could not fetch page ({e})"
    if "html" not in resp.headers.get("Content-Type", ""):
        return "Error: not an HTML page"
    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "form"]):
        tag.decompose()                     # remove code, menus, sidebars
    title = soup.title.get_text(strip=True) if soup.title else ""
    lines = (line.strip() for line in soup.get_text("\n").splitlines())
    text = "\n".join(line for line in lines if line)
    return f"{title}\n\n{text}"[:MAX_PAGE_CHARS]

def _load_notes() -> list:
    if not os.path.exists(NOTES_PATH):
        return []
    notes = []
    with open(NOTES_PATH, "r", encoding="utf-8") as f:
        for line in f:
            notes.append(json.loads(line))
    return notes

def list_notes(role: str) -> str:
    notes = _load_notes()
    role_notes = [note for note in notes if note.get("role") == role]
    if not role_notes:
        return "No notes saved yet for this role."
    output = []
    for note in role_notes:
        output.append(f"Category: {note.get('category')}\n"
                      f"Title: {note.get('title')}\n"
                      f"Source URL: {note.get('source_url')}\n"
                      )
    return "\n".join(output)

def save_note(role, category, title, content, company, source_url) -> str:
    role = role.strip().lower()
    for n in _load_notes():
        if n["role"] == role and n["title"].strip().lower() == title.strip().lower():
            return f"Not saved: a note titled '{title}' already exists for {role}."
    note = {
        "role": role,
        "category": category.lower(),
        "title": title.strip(),
        "content": content,
        "company": company.strip(),
        "source_url": source_url,
        "saved_at": datetime.now().isoformat()
    }
    os.makedirs(os.path.dirname(NOTES_PATH), exist_ok=True)
    with open(NOTES_PATH, "a", encoding="utf-8") as f:  
        f.write(json.dumps(note, ensure_ascii=False) + "\n")
    return f"Saved: '{title}'"

# ---- what the model sees ----
TOOLS = [
    {"type": "web_search_20250305", "name": "web_search", "max_uses": 5,
     "blocked_domains": ["medium.com"]},
    {
        "name": "fetch_page",
        "description": (
            "Fetch a web page and return its main text (title plus body, scripts and menus removed, "
            "truncated to about 8,000 characters). Use it to read a promising search result in full "
            "before saving notes from it. Don't fetch pages whose URL is already listed by list_notes. "
            "Return an error message if the page can't be read (blocked, not HTML, timeout); "
            "if so, move on to another source."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Full URL starting with http:// or https://"},
            },
            "required": ["url"],
        }   
    },
    {
        "name": "list_notes",
        "description": (
            "List the notes already saved for a role: each note's title and category, plus the source "
            "URLs already used. Call this FIRST, before searching, so you only look for new material."   
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "role": {"type": "string", "description": "Target role, e.g. 'data scientist'"},
            },
            "required": ["role"],
        }
    },
    {
        "name": "save_note",
        "description": (
            "Save ONE specific interview-prep item: a question actually asked, a topic to prepare, or a  "
            "useful resource. Make it specific and self-contained (what was asked, at which company if "
            "known, and what a strong answer covers). Do not save generic advice ('be confident') or "
            "anything already in list_notes. Call once per item. Returns whether it was used."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "role": {"type": "string", "description": "Target role, e.g. 'data scientist'"},
                "category": {
                    "type": "string",
                    "enum": ["technical", "statistics", "coding", "case_study",
                             "behavioral", "company_specific", "resource"],
                },
                "title": {"type": "string", "description": "Short unique title, e.g. 'Explain bias-variance tradeoff'"},
                "content": {"type": "string", "description": "The question or topic, context, and what a good answer covers"},
                "company": {"type": "string", "description": "Company it was asked at, or empty string if general"},
                "source_url": {"type": "string", "description": "URL the item came from"},
            },
            "required": ["role", "category", "title", "content", "company", "source_url"],
        }
    }
]

# ---- name -> function, for the loop ----
TOOL_FUNCTIONS = {
    "fetch_page": fetch_page,
    "list_notes": list_notes,
    "save_note": save_note,
}

# ---- test ----
if __name__ == "__main__":
    args = dict(role="data scientist", category="technical", title="Explain bias-variance tradeoff",
                content="Test note.", company="", source_url="http://example.com")
    print(save_note(**args))
    print(save_note(**args))
    print(list_notes("data scientist"))
    print(fetch_page("https://www.example.com")[:300])
    print(fetch_page("https://en.wikipedia.org/wiki/Bias%E2%80%93variance_tradeoff")[:500]) 
    print(fetch_page("https://example.com/this-page-does-not-exist"))