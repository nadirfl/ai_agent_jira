TOOL_NAME = "validate"
TOOL_DESC = "Validiert Pflichtfelder und Inhalt für ein JIRA-Element"
TOOL_USAGE = "JIRA"

def run(fields: dict) -> tuple[bool, list[str]]:
    errors = []

    if not fields.get("title"):
        errors.append("Titel fehlt oder ist leer.")
    elif len(fields["title"]) < 5:
        errors.append("Titel ist sehr kurz.")
    
    if not fields.get("description"):
        errors.append("Beschreibung fehlt.")
    elif len(fields["description"]) < 20:
        errors.append("Beschreibung ist zu knapp.")
    
    # TODO: more checks

    is_valid = len(errors) == 0
    return is_valid, errors