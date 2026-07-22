import json, re

def safe_json_parse(content: str) -> dict:
    match = re.search(r"\{.*\}", content, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in LLM response.")
    raw = match.group()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        repaired = raw.replace("\r\n", "\\n").replace("\n", "\\n").replace("\t", "\\t")
        return json.loads(repaired)