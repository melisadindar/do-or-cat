FROM python:3.11-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y dos2unix curl python3 python3-pip

# Çalışma dizinini ayarla
WORKDIR /app

# Gerekli paketleri yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

EXPOSE 8000

# Django sunucusunu başlat
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]