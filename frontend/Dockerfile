# Base image olarak Node.js kullan
FROM node:18

# Çalışma dizinini oluştur
WORKDIR /app

# Frontend dosyalarını kopyala
COPY . .

# http-server'ı global olarak yükle
RUN npm install -g http-server

# Varsayılan portu expose et
EXPOSE 8080

# http-server ile frontend'i başlat
CMD ["http-server", "-o", "index.html", ".", "-p", "8080", "-c-1", "--silent"]
