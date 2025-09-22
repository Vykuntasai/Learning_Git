# # Use official Python slim image
# FROM python:3.10-slim

# # Set working directory inside container
# WORKDIR /app

# # Install dependencies
# RUN pip install --no-cache-dir pyyaml pytest

# # Copy all files from current folder into container
# COPY . /app

# # Default command to run the agent on workflow.yaml and "build" job
# CMD ["python", "agent.py"]

# Use lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
COPY agent.py .
COPY sample_pipeline_template.yml .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run agent
CMD ["python", "agent.py"]

