# Zadanie 1 – Programowanie aplikacji w chmurze

## Autor
Jakub Kramek

## Repozytoria
- GitHub: [https://github.com/Kr4ms00n/chmury-weather-app]
- DockerHub: [https://hub.docker.com/repository/docker/kr4ms00n/chmury/general]

---

## 1. Dockerfile

FROM python:3.9-slim

LABEL org.opencontainers.image.authors="Jakub Kramek"
LABEL org.opencontainers.image.description="Aplikacja pogodowa z API"
LABEL org.opencontainers.image.version="1.0.0"


WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ templates/


ENV PORT=5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT}/ || exit 1

EXPOSE ${PORT}

CMD ["python", "app.py"]

---

## 2. Komendy

### Budowanie i uruchomienie obrazu wraz z logami:
```bash
docker build -t chmury:latest .

docker run -d -p 5000:5000 -e WEATHER_API_KEY=d271aae8be0f6c6e10b92a21b5dd43cf --name weather-container chmury:latest

c80206f81c93c27829b2a2357d92bf25df5ce40139d1afd6c6441e56245ad4bb

docker logs weather-container
Application started at: 2025-05-13 17:35:01
Author: Jakub Kramek
Listening on port: 5000
Hostname: c80206f81c93
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000
 


