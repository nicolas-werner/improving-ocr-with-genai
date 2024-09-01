# Installation

Um das Projekt zu installieren, folge diesen Schritten:

1. Klon das Repository:
```bash
git clone https://github.com/nicolaswerner/improving-ocr-with-genai.git
```

2. Installiere die Abhängigkeiten mit poetry:


```bash
brew install poetry
```

```bash
poetry install
```

3. Starte die Entwicklungsumgebung:
```bash
poetry shell
```

4. Erstelle eine `.env` Datei mit folgendem Inhalt (du kannst `.env.template` als Template verwenden und in `.env` umbenennen)
```bash
OPENAI_API_KEY=
```

5. Führe das Notebook `openai_ocr.ipynb` in `/notebooks` aus.