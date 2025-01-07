FROM python:3.11-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y dos2unix curl python3 python3-pip

RUN apt-get update && apt-get install -y libpq-dev gcc

# Çalışma dizinini ayarla
WORKDIR /app

# Gerekli paketleri yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Convert scripts to Unix format
RUN dos2unix /app/entrypoint.sh

EXPOSE 8000

# Entrypoint script'ine çalıştırma izni ver
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

# Django sunucusunu başlat
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
