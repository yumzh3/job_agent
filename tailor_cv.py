import sys, json, os
from datetime import date
from llm import ask_json

SYSTEM_PROMPT = """
You are an expert technical recruiter and CV tailor.
You will receive a master CV and a job description. Produce a tailored CV specifically for this job, selected and rewritten only from the master CV.
The candidate (the CV's owner) is a geochemistry PhD moving into data science and AI/ML, so data and modeling work should be emphasized, and domain expertise framed as an advantage when the job involves Earth science.
Rules you should follow:
1.Only facts from the master CV. You may select, reorder, reword, and omit; you may never add skills, tools, numbers, titles, or dates.
2.Keep qualifiers. Items listed as limited exposure stay limited, and team work stays team work.
3.Keep numbers exactly as written. Never calculate, combine, or estimate new numbers (e.g. years of experience, totals). Never change a number; if unsure, omit it.
4.Rewrite the summary for this job, using only true claims.
5.Use the job’s terminology where it’s honestly true (e.g. if the job says “Bayesian inference” and the candidate's CV does Monte Carlo sampling, don’t relabel it as Bayesian).
6.Prioritize the projects most relevant to this job, and keep it to about 2 pages.
7.Put anything the job wants that the CV lacks into gaps_not_addressed.
8.Before answering, verify that every number, date, and named skill in the tailored CV appears in the master CV. Remove anything that doesn’t.
"""   # your rules
SCHEMA = {
    "type": "object",
    "properties": {
        "tailored_cv_markdown": {"type": "string"},
        "changes": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "section": {"type": "string"},
                "change": {"type": "string"},
                "reason": {"type": "string"},
            },
            "required": ["section", "change", "reason"],
            "additionalProperties": False,
        }},
        "keywords_matched": {"type": "array", "items": {"type": "string"}},
        "gaps_not_addressed": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["tailored_cv_markdown", "changes", "keywords_matched", "gaps_not_addressed"],
    "additionalProperties": False,
}
    
def load_text(path):
    with open(path, "r") as f:
        return f.read()
def tailor(master_cv: str, job_text: str) -> dict:    # builds prompt, calls ask_json
    prompt = f"""Tailor the master CV below to this job description.
    <Master CV>\n{master_cv}\n</Master CV>\n<Job Description>\n{job_text}\n</Job Description>"""
    return ask_json(prompt, SCHEMA, system=SYSTEM_PROMPT, model="claude-opus-5-5", max_tokens=8000)   # builds prompt, calls ask_json
def save_outputs(result: dict, job_name: str):
    today = date.today().isoformat()
    os.makedirs("output", exist_ok=True)
    with open(f"output/cv_{job_name}_{today}.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    with open(f"output/cv_{job_name}_{today}.md", "w", encoding="utf-8") as f:
        f.write(result["tailored_cv_markdown"])

if __name__ == "__main__":
    job_path = sys.argv[1]          # e.g. "jobs/kobold.txt"
    job_text = load_text(job_path)
    master_cv = load_text("master_cv.md")
    result = tailor(master_cv, job_text)
    job_name = os.path.splitext(os.path.basename(job_path))[0]
    save_outputs(result, job_name)
    print(f"{len(result['gaps_not_addressed'])} gaps:", *result['gaps_not_addressed'], sep="\n- ")