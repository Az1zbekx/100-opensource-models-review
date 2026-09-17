FROM python:3.11-slim

# OpenCV va Ultralytics uchun kerakli tizim kutubxonalari
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Konteyner ichida standart holda headless (oynasiz) rejimda ishlaydi
CMD ["python", "demo.py", "--headless"]
