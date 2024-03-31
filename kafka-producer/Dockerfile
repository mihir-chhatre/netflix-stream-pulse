# Use the Python 3.8 slim image as the base image.
FROM python:3.8-slim

# Copy the requirements.txt file to the root of the container.
COPY requirements.txt .

# Install the Python dependencies defined in requirements.txt.
# The 'set -ex' command will print each command and its expanded arguments to the terminal and will make the script exit if any command fails.
# The '--no-cache-dir' option prevents pip from caching installed packages, which keeps the Docker image size smaller.
RUN set -ex; \
    pip install --no-cache-dir -r requirements.txt

# Set the working directory to the root of the container.
WORKDIR /

# Copy the 'wait-for-it.sh' script to the root of the container.
# This script is used to wait for other services (like Kafka or Zookeeper) to be available before starting the main application.
COPY wait-for-it.sh wait-for-it.sh

RUN chmod +x wait-for-it.sh

# Add the 'simulate_data.py' script to the root of the container.
# Simulates data and produces messages for Kafka.
ADD simulate_data.py .

# Define the command that runs when the container starts.
# This command uses 'wait-for-it.sh' to wait for both Zookeeper and Kafka to be available before running 'simulate_data.py'.
# The '-s' flag makes the script silent and '-t 30' sets a 30-second timeout for each service to be available.
CMD ./wait-for-it.sh -s -t 30 $ZOOKEEPER_SERVER -- ./wait-for-it.sh -s -t 30 $KAFKA_SERVER -- python -u simulate_data.py
