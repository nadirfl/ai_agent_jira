TOOL_NAME = "extract"
TOOL_DESC = "Extrahiert relevante Daten aus einer Mail für ein JIRA-Element"
TOOL_USAGE = "JIRA"

from llm import ask_ollama
import re, json

def run(text: str) -> dict:
    prompt = f"""
Bitte formuliere eine Jira-Story aus folgendem Text und verwende dieses JSON Format:

--- FORMAT START ---
**Titel**: <prägnanter Titel>

**Beschreibung**:
Als <Rolle>
möchte ich <Funktion>
damit ich <Nutzen>.

**Akzeptanzkriterien**:
- [ ] ...

**Priorität**: Hoch / Mittel / Niedrig
--- FORMAT ENDE ---

--- INPUT START ---
Hier ist der Inputtext:
\"\"\"
{text}
\"\"\"
--- INPUT ENDE ---

Verwende folgendes Format für das JSON:
--- JSON FORMAT START ---
{{
  "title": "...",
  "description": "...",
}}
--- JSON FORMAT ENDE ---

Gib ausschliesslich nur ein valides JSON-Objekt zurück, kein Markdown oder Kommentar. Die Felder sollen in Deutsch sein.
"""
    raw = ask_ollama(prompt)
    raw = re.sub(r"^```json", "", raw, flags=re.I).strip()
    raw = re.sub(r"```$", "", raw).strip()
    return json.loads(raw)