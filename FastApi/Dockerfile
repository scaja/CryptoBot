# Offizielles Python-Image verwenden
FROM openjdk:11

# Arbeitsverzeichnis im Container setzen
WORKDIR /app

# Kopiere die bereits heruntergeladenen Spark-Dateien in den Container
COPY spark-3.5.0-bin-hadoop3 /opt/spark

# Kopiere die Requirements-Datei in den Container
COPY requirements.txt .
RUN apt-get update && apt-get install -y python3-pip

# Installiere die Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest der Anwendung
COPY . .

# Set JAVA_HOME
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH

# Exponiere den Port für FastAPI
EXPOSE 8000

# Starte die FastAPI-App mit Uvicorn
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Set Pythonpath
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]