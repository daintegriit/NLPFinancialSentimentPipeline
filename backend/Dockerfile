# Use slim Python base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y cron gcc ca-certificates vim && \
    apt-get clean && \
    update-ca-certificates

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app code
COPY . .

# Add cron job to system-wide schedule
COPY daily-runner-cron /etc/cron.d/daily-runner-cron
RUN chmod 0644 /etc/cron.d/daily-runner-cron

# Create log file
RUN touch /var/log/cron.log

# Expose API port
EXPOSE 8006

# Run cron and API server together
CMD ["sh", "-c", "cron && uvicorn main:app --host 0.0.0.0 --port 8006"]
