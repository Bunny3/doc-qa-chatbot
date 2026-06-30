FROM python:3.11-slim

WORKDIR /app

# Install system dependencies needed for some Python packages (e.g. chromadb)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies first (better Docker layer caching —
# this layer only rebuilds if requirements.txt changes, not on every code edit)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the actual application code
COPY src/ ./src/
COPY seed_data/sample.pdf ./data/raw/sample.pdf
COPY main.py .

# ChromaDB will persist data here — mount this as a volume in production
RUN mkdir -p chroma_db

EXPOSE 8000

# Health check — Docker can use this to know if the container is actually healthy
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]