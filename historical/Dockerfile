# Use the OpenJDK 11 base image (contains Java runtime and development tools)
FROM openjdk:11

# Set the working directory inside the container
WORKDIR /historical

# Copy the pre-downloaded Apache Spark files into the container
COPY spark-3.5.0-bin-hadoop3 /opt/spark

# Copy the dependency file (Python packages required for the application)
COPY requirements.txt .

# Update the package lists and install Python 3 and pip
RUN apt-get update && apt-get install -y python3-pip

# Install the Python dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all script files into the container (used for processing or data handling)
COPY scripts/ scripts/

# Copy the regression model files into the container
COPY regression/ regression/

# Set the environment variable for Apache Spark
ENV SPARK_HOME=/opt/spark

# Add Spark binaries to the system PATH so they can be executed from anywhere
ENV PATH=$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH

# Copy the entrypoint script and give it execute permissions
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the entrypoint script to run when the container starts
ENTRYPOINT ["/entrypoint.sh"]
