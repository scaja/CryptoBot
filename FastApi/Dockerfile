# Offizielles Python-Image verwenden
FROM python:3.9

# Arbeitsverzeichnis im Container setzen
WORKDIR /app

# Kopiere die Requirements-Datei in den Container
COPY requirements.txt .

# Installiere die Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest der Anwendung
COPY . .

# Exponiere den Port für FastAPI
EXPOSE 8000

# Starte die FastAPI-App mit Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]