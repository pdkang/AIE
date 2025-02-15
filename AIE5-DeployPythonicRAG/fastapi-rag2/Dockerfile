FROM python:3.9-slim

WORKDIR /app

# Copy requirements from root directory
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend files  
COPY backend/ .

# Copy frontend files
COPY frontend/dist/ ./static/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]