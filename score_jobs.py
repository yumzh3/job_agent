import sys
import yaml
import db
from llm import ask_json

SYSTEM_PROMPT = """
You are a job scoring assistant. 
Your task is to evaluate job postings against a candidate's profile and CV summary, applying the bands table, deal-breaker rules, gap severity rules, confidence rule, tier rule, and visa rule.
Bands table:
| Score | Band | Example |
|------|-------|-------------|
| 9-10    | DS/AI/ML title in the candidate's ideal direction (Earth, climate, materials), or a data-driven geoscience role heavy on modeling, at a level in the candidate's profile  | Entry data scientist at KoBold; computational geochemist at Terradot |
| 7-8    | DS/AI/ML title in any other field, at a level in the candidate's profile   | Data Scientist I, Amazon Music |
| 5-6    | DS/AI/ML title in the candidate's ideal direction, but above the candidate's level (senior, staff) | Senior data scientist at KoBold |
| 3-4    | DS/AI/ML title in another field above the candidate's level, or a traditional geoscience role (lab-focused geochemist, technician) | Senior DS at Amazon Music; lab geochemist |
| 1-2    | Unrelated role, or far above the candidate's level (principal, director, manager) | Sales engineer; director of data science |
Company, location and domain do not move an unrelated role into a higher band; an unrelated role is 1–2 even at an ideal-direction company.
Within a band: - Do not count the level mismatch that set the band as a gap when choosing between the two numbers of a band; choose using the other gaps.
               - The higher number if gaps are only soft or learnable, the lower number if there’s a hard gap for the candidate.
               - When confidence is low, choose the lower number of the band.
Deal-breaker rules:
- If any of the cases listed in the deal_breakers section apply, the job should be dropped from the digest whatever its score.
gap severity rules:
- Soft gaps: may not actually block the candidate (e.g. “3+ years” when the candidate's PhD research could count).
- Learnable gaps: a skill you could pick up in weeks to months (Spark, cloud, a framework).
- Hard gaps: can’t change soon (e.g. 8+ years required, a required license or degree).
- For cases listed in the flag_as_gaps section:
  - years of industry experience above what the candidate has: when it is <4 years and the candidate's PhD/postdoc may count, it is a soft gap. Otherwise, it is a hard gap.
  - degree field or domain mismatch: Hard gap.
  - specific tools or frameworks not on the candidate's CV: Learnable gap.
  - no sponsorship available: Soft gap.
confidence rule:
- High confidence means the evaluation is based on clear and strong evidence and a complete job description.
- Low confidence means the evaluation is uncertain or based on the job description that is a snippet or lacks a requirements section.
tier rule:
- Tier 1: AI/data science in Earth, climate or materials, or data-driven geoscience.
- Tier 2: core DS/ML roles in any other field, including PhD internships.
- Tier 3: adjacent roles where the candidate's domain helps: geospatial or remote sensing, environmental data, battery or materials, subsurface or geothermal, national labs.
visa rule:
- If the posting says no sponsorship, flag it as a soft gap (‘OK on OPT; confirm long-term’). If sponsorship isn’t mentioned, don’t flag it.
"""   # role, task, the bands table, deal-breaker rules,
                            # gap severity rules, confidence rule, visa rule
SCHEMA = {
    "type": "object",
    "properties": {
        "deal_breaker": {"type": "boolean"},
        "deal_breaker_reason": {"type": "string"},   # empty string if none
        "tier": {"type": "integer"},                 # 1, 2 or 3, from profile
        "score": {"type": "integer"},                # 1-10, by the bands
        "matched": {"type": "array", "items": {"type": "string"}},
        "gaps": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "requirement": {"type": "string"},
                "severity": {"type": "string", "enum": ["soft", "learnable", "hard"]},
                "note": {"type": "string"},
            },
            "required": ["requirement", "severity", "note"],
            "additionalProperties": False,
        }},
        "confidence": {"type": "string", "enum": ["high", "low"]},
        "confidence_reason": {"type": "string"},
        "verdict": {"type": "string"},              # one sentence
    },
    "required": ["deal_breaker", "deal_breaker_reason", "tier", "score", "matched",
                 "gaps", "confidence", "confidence_reason", "verdict"],
    "additionalProperties": False,
}

def build_prompt(job, profile_text, cv_summary):    # job + profile + summary in tags
    return f"""
<job>
{job}
</job>
<profile>
{profile_text}
</profile>
<cv_summary>
{cv_summary}
</cv_summary>
"""
def format_job(job) -> str:
    return f"""Title: {job['title']}
Company: {job['company']}
Location: {job['location']}
Source: {job['source']}

Description:
{job['description']}"""

def score_job(job, profile_text, cv_summary) -> dict:   # ask_json + score check
    prompt = build_prompt(job, profile_text, cv_summary)
    result = ask_json(prompt, SCHEMA, system=SYSTEM_PROMPT, model="claude-sonnet-5-5", max_tokens=2048, purpose="score_job")
    score = result["score"]
    if not 1 <= score <= 10:
        print(f" Warning: score {score} out of range, clamped")
        result["score"] = max(1, min(score, 10))
    return result

if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    # load profile.yaml as text, load cv_summary.md
    with open("profile.yaml", "r", encoding="utf-8") as f:
        profile_text = f.read()
    with open("cv_summary.md", "r", encoding="utf-8") as f:
        cv_summary = f.read()
    conn = db.connect(); jobs = db.get_unscored(conn)
    if limit:
        jobs = jobs[:limit]  # keep only the first N jobs for testing
    # for each job: score, db.save_score(...), conn.commit() after each one
    # print a short line per job: score, title, company
    for job in jobs:
        try:
            result = score_job(format_job(job), profile_text, cv_summary)
        except Exception as e:
            print(f"Error on {job['id']} ({job['title']} - {job['company']}): {e}")
            continue
        db.save_score(conn, job["id"], result)
        conn.commit()
        flag = " [DEAL-BREAKER]" if result["deal_breaker"] else ""
        print(f"{result['score']:>2} | T{result['tier']} | {job['title']} - {job['company']}{flag}")