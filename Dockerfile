# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "gunicorn --workers 2 --threads 2 --timeout 300 --bind 0.0.0.0:8087 api:app"]
