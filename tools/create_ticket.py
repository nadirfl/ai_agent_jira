TOOL_NAME = "create"
TOOL_DESC = "Erstellt ein JSON-Objekt für die Erstellung eines JIRA-Elementes via das JIRA-API"
TOOL_USAGE = "JIRA"

import requests
import yaml

config = yaml.safe_load(open("config.yaml"))["jira"]

def run(fields: dict, issue_type: str):
    '''
    TODO: create account and generate API-Key, afterwards activate this code
    
    url = f"{config['base_url']}/rest/api/3/issue"
    headers = {
        "Authorization": f"Basic {config['user_email']}:{config['api_token']}",
        "Content-Type": "application/json"
    }

    data = {
        "fields": {
            "project": {"key": config["project_key"]},
            "summary": fields['title'],
            "description": fields["description"],
            "issuetype": {"name": issue_type or config["default_issue_type"]}
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()
    '''
    print("Simulierter Ticket-Aufruf:")
    print("Typ: ", issue_type)
    print("Titel: ", fields['title'])
    print("Beschreibung: ", fields['description'])
    return {"status": "simuliert", "key": "DEV-ABC"}