# Define the application build stage
FROM python:3.11.8-slim-bookworm AS build-stage

# Set work directory and environment variables
WORKDIR /crowdfund
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONBUFFERED=1

# Install & upgrade system dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends netcat-openbsd gcc \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application
COPY . .

# run_dev.sh
RUN ["chmod", "+x", "./run.sh"]
CMD ["./run.sh"]
