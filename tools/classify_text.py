TOOL_NAME = "classify"
TOOL_DESC = "Klassifiziert Anforderungen in Mails in die Kategorien Story, Bug, Epic, Task, Question"
TOOL_USAGE = "JIRA"

from llm import ask_ollama

def run(text: str) -> str:
    prompt = f"""
Du erhältst folgenden Text:

\"\"\"
{text}
\"\"\"

Welcher Tickettyp passt am besten?

Wähle aus den Kategorien: Story, Bug, Epic, Task, Question

Gib ausschliesslich nur den Tickettyp zurück.

"""
    return ask_ollama(prompt)