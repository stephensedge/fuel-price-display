FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app/ ./app/

# Set working directory and default command
WORKDIR /app/app
CMD ["python", "fuel_display.py"]
