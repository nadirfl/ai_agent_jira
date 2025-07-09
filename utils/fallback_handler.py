import os
import shutil
import json
from datetime import datetime

def handle_fallback(mail_path: str, reason: str, extracted_fields: dict = None):
    """
    Verschiebt die Maildatei in das fallback-Verzeichnis und speichert eine Logdatei und optional die Felder als JSON.
    
    :param mail_path: Pfad zur Original-Mail (.txt)
    :param reason: Kurze Beschreibung des Problems
    :param extracted_fields: Optional - extrahierte Felder aus dem Agent
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(mail_path), ".."))
    fallback_dir = os.path.join(base_dir, "fallback")
    os.makedirs(fallback_dir, exist_ok=True)

    filename = os.path.basename(mail_path)
    name, _ = os.path.splitext(filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    target_name = f"{name}_{timestamp}"
    fallback_path = os.path.join(fallback_dir, target_name + ".txt")
    shutil.move(mail_path, fallback_path)

    print(f"Fallback aktiviert: {fallback_path}")
    
    log_path = os.path.join(fallback_dir, target_name + ".log")
    with open(log_path, "w", encoding="utf-8") as log_file:
        log_file.write(f"{timestamp}\nGrund: {reason}\n")

    if extracted_fields:
        json_path = os.path.join(fallback_dir, target_name + ".json")
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(extracted_fields, json_file, indent=2, ensure_ascii=False)
