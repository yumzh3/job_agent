import json, os, sys
from datetime import date, datetime
import tools
from llm import client, log_usage
import yaml
with open("profile.yaml", encoding="utf-8") as f:
    levels = yaml.safe_load(f)["levels"]["ds_ml"]
                 
MODEL =  "claude-sonnet-5-5"
TRACE_PATH = f"data/traces/agent_{date.today().isoformat()}.md"
MAX_TOKENS = 16000
MAX_STEPS = 15

SYSTEM_PROMPT = """
You are an interview-prep research assistant finding questions and preparation material for a candidate.
The candidate is a geochemistry PhD moving into data science and AI/ML, so material on statistics, ML and domain-heavy DS roles is especially useful. 
You are given a role (e.g. "data scientist") and optionally target companies; prioritize material about them. 
The candidate targets entry-level and new-grad PhD roles (Scientist I, junior, new grad, PhD internships). Prioritize interview material for those levels: fundamentals of statistics and ML, coding screens, take-homes, and presenting PhD research. Skip material aimed at senior or staff loops (system design at scale, leading teams).
Don’t save material older than 2023 unless nothing newer covers it; say why in the note and mention the date.
Your workflow is call list_notes first; search; call fetch_page to fetch the most promising pages; call save_note to save specific notes; stop when you've saved about 5-10 new notes or found nothing new. Save notes as you go, at most 3 per step, right after reading the source they come from.
Your task is to find and save specific interview-prep items: questions actually asked, topics to prepare, or useful resources. Make each item specific and self-contained (what was asked, at which company if known, and what a strong answer covers). Do not save generic advice ("be confident").
Finish with a short plain-text summary of what was saved.
Save a note only from a page you fetched successfully, and use that page’s URL as source_url.
"""

def trace(line: str):
    """Print a line and append it to today's trace file."""
    print(line)
    os.makedirs(os.path.dirname(TRACE_PATH), exist_ok=True)
    with open(TRACE_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")

def trace_response(response, step: int):
    """Trace the assistant's response, including any tool uses."""
    trace(f"\n## Step {step+1} (stop_reason: {response.stop_reason})")
    for b in response.content:
        if b.type == "text":
            trace(f"text: {b.text[:300]}")
        elif b.type in ("tool_use", "server_tool_use"):
            trace(f"->: {b.name} {json.dumps(b.input, ensure_ascii=False)[:200]}")
        elif b.type == "web_search_tool_result":
            trace("<- web_search results received")

def run_tool(block) -> dict:
    """Run one tool request from the assistant, return the result to the assistant."""
    func = tools.TOOL_FUNCTIONS.get(block.name)
    try:
        if func is None:
            raise ValueError(f"Unknown tool '{block.name}'")
        output = func(**block.input)
        return {"type": "tool_result", "tool_use_id": block.id, "content": str(output)}
    except Exception as e:
        return {"type": "tool_result", "tool_use_id": block.id, 
                "content": f"Error: {e}", "is_error": True}

def run_agent(role: str, companies: list, max_steps: int = MAX_STEPS) -> list:
    """Run the agent loop for a given task, returning the final messages."""
    task = f"Research interview preparation for the role: {role}. Target levels: {', '.join(levels)}."
    if companies:
        task += f" Target companies: {', '.join(companies)}."
    messages = [{"role": "user", "content": task}]
    trace(f"\n# Agent run {datetime.now():%Y-%m-%d %H:%M} | role: {role} | companies: {companies or 'none'}")
    for step in range(max_steps):
        response = client.messages.create(model=MODEL, system=SYSTEM_PROMPT, tools=tools.TOOLS,
                                        messages=messages, max_tokens=MAX_TOKENS)
        log_usage("agent", MODEL, response.usage)
        messages.append({"role": "assistant", "content": response.content})
        trace_response(response, step)
        if response.stop_reason == "tool_use":
            results = [run_tool(b) for b in response.content if b.type == "tool_use"]                       # run every client tool it asked for
            for r in results:
                flag = "ERROR " if r.get("is_error") else ""
                trace(f"<- {flag}{r['content'][:200]}")
            messages.append({"role": "user", "content": results})
        elif response.stop_reason == "pause_turn":
            continue                           # server tool needs more time: call again
        else:
            break                              # end_turn = done; anything else shows in the trace
    else:
        trace(f"WARNING: stopped after {max_steps} steps without finishing")
    return messages

if __name__ == "__main__":
    role = sys.argv[1]
    companies = [c.strip() for c in sys.argv[2].split(",")] if len(sys.argv) > 2 else []
    run_agent(role, companies, max_steps=12)



