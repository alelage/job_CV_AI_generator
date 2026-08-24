import json
import re
from typing import Any

from src.ai.client_factory import call_ai


def get_json_object(content: str) -> dict[str, Any]:
    content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content.strip(), flags=re.I | re.S).strip()
    try:
        value = json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, flags=re.S)
        if not match:
            raise ValueError("The AI returned invalid JSON.") from None
        value = json.loads(match.group(0))
    if not isinstance(value, dict):
        raise ValueError("The AI response was not a JSON object.")
    return value


def analyse_match(client: Any, provider: str, model: str, job: str, cv: str) -> dict[str, Any]:
    system = "You are a precise CV screening assistant. Return only valid JSON, with no Markdown or commentary. Use status exactly 'match' or 'missing'."
    prompt = f"""Extract the top 10 to 15 specific hard and soft-skill requirements from the job description and compare each against the CV.
Use 'match' only when the CV provides credible evidence; use 'missing' when it does not or evidence is too weak. Keep each requirement concise and specific.

Return exactly this JSON shape:
{{"requirements": [{{"text": "5+ years Python", "status": "match"}}]}}

JOB DESCRIPTION:
---
{job}
---

CLEAN CV TEXT:
---
{cv}
---"""
    data = get_json_object(call_ai(client, provider, model, system, prompt))
    requirements = data.get("requirements")
    if not isinstance(requirements, list):
        raise ValueError("The AI response did not contain a requirements list.")
    cleaned = [{"text": str(x["text"]), "status": x["status"]} for x in requirements[:15] if isinstance(x, dict) and x.get("text") and x.get("status") in {"match", "missing"}]
    if not cleaned:
        raise ValueError("The AI did not return any valid requirements.")
    return {"requirements": cleaned}
