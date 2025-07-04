import os
from tool_manager import load_tools

tools = load_tools("JIRA")

print("Tools geladen:", list(tools.keys()))

classify = tools["classify"]["run"]
extract = tools["extract"]["run"]
validate = tools["validate"]["run"]
create = tools["create"]["run"]
confirm = tools["confirm"]["run"]

input_dir = "input"

for file in os.listdir(input_dir):
    if file.endswith(".txt"):
        path = os.path.join(input_dir, file)
        print(f"\nVerarbeite Datei: {file}")

        text = open(path, encoding="utf-8").read()

        print("Klassifiziere Text...")
        ticket_type = classify(text)
        print(f"Tickettyp: {ticket_type}")

        fields = extract(text)

        print("Prüfe extrahierte Daten...")
        valid, errors = validate(fields, ticket_type)

        if not valid:
            print("Ticket unvollständig oder ungültig:")
            for err in errors:
                print(" -", err)
                # TODO: notify user
        else:
            print("\n Vorgeschlagene Story:")
            print(f" - Typ: {ticket_type}")
            print(f" - Titel: {fields.get('title')}")
            print(f" - Beschreibung: {fields.get('description')}")
            
            feedback = input("\nMöchtest du dieses Ticket erstellen? (j/n): ").strip().lower()
            if feedback == "j":
                print(f"Erstelle Ticket mit Titel: {fields['title']}")
                result = create(fields, ticket_type)
                ticket_key = result.get("key", "DEV-???")

                message = confirm(fields, ticket_type, ticket_key)
                print(message)
            else:
                print("Ticket wurde verworfen")