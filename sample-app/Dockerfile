FROM python:3.9-slim

# Set WORKDIR
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source files
COPY . .

# Expose the detected application port
EXPOSE 5000

# Use the correct application startup command
CMD ["python", "app.py"]
