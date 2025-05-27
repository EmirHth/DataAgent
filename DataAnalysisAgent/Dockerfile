FROM python:3.11-slim

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Çalışma dizinini ayarla
WORKDIR /app

# Python bağımlılıklarını yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Environment variables
ENV SMITHERY_API_KEY=81c0c036-745e-42ae-9090-eebd33950d82
ENV SMITHERY_PROFILE_KEY=probable-capybara-wWraCH
ENV PYTHONPATH=/app
ENV LOG_LEVEL=INFO

# Port'u expose et
EXPOSE 8000

# Sağlık kontrolü
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Uygulamayı başlat
CMD ["python", "server.py"] 