TOOL_NAME = "validate"
TOOL_DESC = "Validiert Pflichtfelder und Inhalt für ein JIRA-Element"
TOOL_USAGE = "JIRA"

import yaml
import os

config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "validation.yaml"))
print("Lade Validierungsregeln aus: ", config_path)
with open(config_path, "r", encoding="utf-8") as f:
    RULES = yaml.safe_load(f)

def run(fields: dict, ticket_type) -> tuple[bool, list[str]]:
    errors = []

    rules = RULES.get(ticket_type, {}) 

    # Fallback default
    required = rules.get("required_fields", []) + RULES.get("default", {}).get("required_fields", [])
    min_length = {**RULES.get("default", {}).get("min_length", {}), **rules.get("min_length", {})}

    for key in required:
        if not fields.get(key):
            errors.append(f"Pflichtfeld '{key}' fehlt.")

    for key, length in min_length.items():
        if key in fields and len(str(fields[key])) < length:
            errors.append(f"'{key}' ist zu kurz (min. {length} Zeichen).")
    
    # TODO: more checks

    return len(errors) == 0, errors