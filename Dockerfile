FROM python:3.10-slim
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends     build-essential     cmake     && rm -rf /var/lib/apt/lists/*

COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt
COPY src/ ./src/
COPY models/ ./models/
COPY data/processed/ ./data/processed/
EXPOSE 9010
CMD ["python", "src/api.py"]
