# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /

# Install Java and procps (for the ps command)
RUN apt-get update && \
    apt-get install -y openjdk-17-jre-headless procps && \
    rm -rf /var/lib/apt/lists/*

# Accept credential filename as a build argument
ARG GCP_CREDENTIALS

# Copy the current directory contents into the container at /
COPY . .

RUN chmod +x wait-for-it.sh

# Install Python packages
RUN pip install --no-cache-dir pyspark kafka-python==2.0.2 pandas==1.4.1 psycopg2-binary==2.9.3 google-cloud-bigquery==3.1.0

# Set environment variables
ENV GOOGLE_APPLICATION_CREDENTIALS ${GCP_CREDENTIALS}
ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64

# Run load_to_bq.py when the container launches
CMD ./wait-for-it.sh -s -t 30 $ZOOKEEPER_SERVER -- ./wait-for-it.sh -s -t 30 $KAFKA_SERVER -- python -u load_to_bq.py
