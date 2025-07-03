TOOL_NAME = "confirm"
TOOL_DESC = "Erzeugt eine Bestätigungsnachricht für das erstellte Ticket"
TOOL_USAGE = "JIRA"

def run(fields: dict, ticket_type: str, ticket_key: str) -> str:
    title = fields.get("title", "[kein Titel]")
    return (
        f"Vielen Dank! Das Ticket *{ticket_key}* vom Typ *{ticket_type}* mit dem Titel *{title}* wurde erfolgreich erstellt."
    )