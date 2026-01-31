# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# 1. Install system dependencies FIRST (these rarely change)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# 2. Copy ONLY requirements.txt first
COPY requirements.txt .

# 3. Install Python dependencies (Cached unless requirements.txt changes)
RUN pip install --no-cache-dir -r requirements.txt

# 4. NOW copy the rest of the application code
COPY . .

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run app.py when the container launches
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]