FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt lives at the project root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# actual app code lives inside backend/ — copy its *contents* into /app
# so main.py ends up at /app/main.py, not /app/backend/main.py
COPY backend/ .

RUN mkdir -p uploads data

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]