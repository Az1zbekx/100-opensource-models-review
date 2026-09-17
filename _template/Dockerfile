FROM python:3.11-slim

# Model turiga qarab kerakli tizim kutubxonalarini shu yerga qo'shing
# (masalan STT/TTS uchun audio kutubxonalari: ffmpeg, libsndfile1)
# RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# GUI/kamera yo'q — standart CMD to'g'ridan-to'g'ri natija beradi (konsolga yoki faylga)
CMD ["python", "demo.py"]
