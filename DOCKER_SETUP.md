# 100+ Opensource Models - Docker Edition

Barcha 100+ opensource modellarni **bir commandda** local da ishga tushiring!

## 🚀 Tez start

```bash
# 1. Repository clone qiling
git clone <repo-url>
cd 100-opensource-models-review

# 2. docker-compose.yml generate qiling
python3 generate-compose.py

# 3. Barcha modellarni ishga tushiring
docker compose up --pull always
```

## 📋 Modellarni qo'shish

`generate-compose.py` faylda `MODELS` listiga modelingizni qo'shing:

```python
MODELS = [
    ("model-name", "path/to/model", 8001),  # port raqami auto-increment
    ("yolov8", "cv/yolov8n", 8001),
    ("mms-tts-uzb", "tts/mms-tts-uzb", 8002),
    ("faster-whisper", "stt/FasterWhisper", 8003),
    # 96 ta model qo'shing...
]
```

Keyin qayta jarayonni ishga tushiring:

```bash
python3 generate-compose.py
docker compose up
```

## 📁 Struktura

```
100-opensource-models-review/
├── Dockerfile.base              # Base image (pytorch + kutubxonalar)
├── docker-compose.yml           # Generated (run this!)
├── generate-compose.py          # Script: 100 ta model uchun compose yaratadi
├── .dockerignore
├── cv/yolov8n/                  # Computer Vision model
│   ├── Dockerfile
│   ├── requirements.txt
│   └── demo.py
├── tts/mms-tts-uzb/             # Text-to-Speech model
│   ├── Dockerfile
│   ├── requirements.txt
│   └── demo.py
├── stt/FasterWhisper/           # Speech-to-Text model
│   ├── dockerfile
│   ├── requirements.txt
│   └── demo.py
└── llm/Qwen2.5-1.5B-Instruct-GGUF/  # LLM model
    ├── dockerfile
    ├── requirements.txt
    └── demo.py
```

## 🎯 Har bir model

| Model | Port | URL |
|-------|------|-----|
| yolov8 | 8001 | http://localhost:8001 |
| mms-tts-uzb | 8002 | http://localhost:8002 |
| faster-whisper | 8003 | http://localhost:8003 |
| qwen2.5-1.5b | 8004 | http://localhost:8004 |

## 🛑 Modellarni to'xtatish

```bash
docker compose down
```

## 📊 Status tekshirish

```bash
docker compose ps
docker compose logs -f yolov8
```

## 💾 Requirements

- Docker 20.10+
- Docker Compose 2.0+
- 16+ GB RAM
- 50+ GB disk space (100 ta model uchun)

## 📝 Qayta build

```bash
docker compose up --build
```

## 🔧 Kustomizatsiya

`docker-compose.yml` ni to'g'rilash:
- **Environment variables** qo'shish: `environment:` bölümga
- **Volumes** o'zgarish: `volumes:` bölümga
- **Ports** o'zgarish: `ports:` bölümga

Misol:

```yaml
services:
  yolov8:
    build: ./cv/yolov8n
    ports:
      - "9001:8000"  # Changed from 8001
    environment:
      GPU_ENABLED: "false"
      LOG_LEVEL: "debug"
```

---

**Yaratuvchi:** Gordon (Docker Assistant)
