TOOL_NAME = "extract"
TOOL_DESC = "Extrahiert relevante Daten aus einer Mail für ein JIRA-Element"
TOOL_USAGE = "JIRA"

from llm import ask_ollama
import re, json

def run(text: str) -> dict:
    prompt = f"""
Extrahiere aus folgendem Text die Felder für ein JIRA-Ticket im JSON-Format:

- title
- description

Text:
\"\"\"
{text}
\"\"\"

Gib ausschliesslich nur ein valides JSON-Objekt zurück, kein Markdown oder Kommentar. Die Felder sollen in Deutsch sein.
"""
    raw = ask_ollama(prompt)
    raw = re.sub(r"^```json", "", raw, flags=re.I).strip()
    raw = re.sub(r"```$", "", raw).strip()
    return json.loads(raw)