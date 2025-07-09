import os
from tool_manager import load_tools
from utils.fallback_handler import handle_fallback

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

        max_attempts = 3
        attempts = 0
        
        while attempts < max_attempts:
            attempts += 1

            print("Prüfe extrahierte Daten...")
            valid, errors, missing_fields = validate(fields, ticket_type)

            if not valid:
                print("Ticket unvollständig oder ungültig:")
                for err in errors:
                    print(" -", err)
                    # TODO: notify user
                
                for field in missing_fields:
                    action = input("Möchtest du für '{field}' etwas eingeben (e) oder generieren lassen (g)?").strip().lower()

                    if action == "e":
                        user_value = input(f"Bitte gebe den Wert für '{field}' ein:\n>")
                        fields[field] = user_value
                    elif action == "g":
                        from llm import ask_ollama
                        suggestion = ask_ollama(f"Bitte generiere einen sinnvollen Wert für das Feld '{field}' basierend auf dem Kontext:\n{text}")
                        fields[field] = suggestion.strip()
                    else:
                        print("Feld bleibt leer.")
            else:
                break
        
        if not valid:
            print("Maximalanzahl an Korrekturversuchen erreicht - Ticket wird nicht erstellt.")
            handle_fallback(path, reason="Maximale Korrekturversuche erreicht")
            continue

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

