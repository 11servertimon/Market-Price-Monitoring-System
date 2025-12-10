FROM python:3.11-slim

# Ne piši .pyc fajlove, i odmah flushaj output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Workdir u kontejneru
WORKDIR /app

# Instaliraj dependency-je
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Kopiraj Django backend kod
COPY backend /app/backend

WORKDIR /app/backend

# Expose port
EXPOSE 8000

# Start skripta: migracije + runserver
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
