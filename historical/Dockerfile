# Basis-Image mit OpenJDK 8 und Python
FROM openjdk:11

# Set the working directory in the container
WORKDIR /historical

# Kopiere die bereits heruntergeladenen Spark-Dateien in den Container
COPY spark-3.5.0-bin-hadoop3 /opt/spark

# Install dependencies
COPY requirements.txt .
RUN apt-get update && apt-get install -y python3-pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY scripts/ scripts/
COPY regression/ regression/

# Set JAVA_HOME
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH

# Set Pythonpath
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
