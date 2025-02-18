# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /historical

# Copy the requirements file first (to leverage Docker's caching mechanism)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY scripts/ scripts/

# Run the script when the container launches
CMD ["python", "scripts/retrieval_script.py"]
