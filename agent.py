from tool_manager import load_tools

tools = load_tools("JIRA")

print("Tools geladen:", list(tools.keys()))

classify = tools["classify"]["run"]
extract = tools["extract"]["run"]
validate = tools["validate"]["run"]
create = tools["create"]["run"]


text = open("input/beispiel_mail.txt").read()

print("Klassifiziere Text...")
ticket_type = classify(text)
print(f"Tickettyp: {ticket_type}")

fields = extract(text)

print("Prüfe extrahierte Daten...")
valid, errors = validate(fields)

if not valid:
    print("Ticket unvollständig oder ungültig:")
    for err in errors:
        print(" -", err)
        # TODO: notify user
else:
    print(f"Erstelle Ticket mit Titel: {fields['title']}")
    response = create(fields, ticket_type)
    print("Ticket erstellt: ", response.get("key", response))