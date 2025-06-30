# Setup

## Ollama herunterladen
1. Unter folgendem Link Ollama herunterladen: https://ollama.com/download
2. Ollama starten
3. LLM herunterladen & starten: `ollama run mistral`

## Python Env aufsetzen
```
python -m venv venv
.\venv\Scripts\activate

# Falls VSC o.Ä. keine .ps Scripts zulässt: Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

pip install -r .\requirements.txt
```

## Agent starten
`python .\agent.py`

# Was beinhaltet dieses Projekt?

# Spick
`pip list`

`pip freeze > requirements.txt`