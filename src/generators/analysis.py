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
    prompt = f"""Extract the name of the position and the name of the enterprise or institution offering the job. Extract a brief description of the position.
Extract the top 10 to 15 specific hard and soft-skill requirements from the job description and compare each against the CV.
Use 'match' only when the CV provides credible evidence; use 'missing' when it does not or evidence is too weak. Keep each requirement concise and specific.

Return exactly this JSON shape:
{{"position_name":"", "institution_name":"", "brief_description":"", "requirements": [{{"text": "5+ years Python", "status": "match"}}]}}

JOB FULL DESCRIPTION:
---
{job}
---

CLEAN CV TEXT:
---
{cv}
---"""
    data = get_json_object(call_ai(client, provider, model, system, prompt))
    position_name = data.get("position_name")
    institution_name = data.get("institution_name")
    brief_description = data.get("brief_description")
    requirements = data.get("requirements")
    if not isinstance(requirements, list):
        raise ValueError("The AI response did not contain a requirements list.")

    cleaned: list[dict[str, str]] = []
    for item in requirements[:15]:
        if not isinstance(item, dict):
            continue
        raw_text = item.get("text", "")
        if isinstance(raw_text, bool) or raw_text is None:
            continue
        if isinstance(raw_text, (list, dict)):
            try:
                text = json.dumps(raw_text, ensure_ascii=False)
            except Exception:
                text = str(raw_text)
        else:
            text = str(raw_text).strip()
        if not text or text.lower() in {"false", "true", "none", "null"}:
            continue
        if len(text) < 3:
            continue
        raw_status = item.get("status")
        if isinstance(raw_status, bool):
            status = "match" if raw_status else "missing"
        elif isinstance(raw_status, str):
            status = raw_status.strip().lower()
        else:
            status = str(raw_status).strip().lower()

        if not text:
            continue
        if text.strip().lower() in {"true", "false", "null", "none", "0", "1"}:
            continue
        if not re.search(r"[A-Za-z]", text):
            continue
        if status not in {"match", "missing"}:
            continue
        cleaned.append({"text": text, "status": status})

    if not cleaned:
        raise ValueError("The AI did not return any valid requirements.")
    return {"position_name": position_name, "institution_name": institution_name, "brief_description": brief_description, "requirements": cleaned}
