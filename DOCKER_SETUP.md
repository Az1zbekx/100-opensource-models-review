# Docker Setup & Containerization Guide

This guide describes how to run and benchmark containerized open-source models (`llm/`, `tts/`, and `stt/`) in isolated environments.

---

## Architecture Overview

```
                           +----------------------+
                           |  Dockerfile.base     | (CPU: ml-base-cpu:latest)
                           |  Dockerfile.base.gpu | (GPU: ml-base-gpu:latest)
                           +----------+-----------+
                                      |
         +----------------------------+----------------------------+
         |                            |                            |
         v                            v                            v
   llm/* Services               tts/* Services               stt/* Services
 (Profile: `llm`)             (Profile: `tts`)             (Profile: `stt`)
```

> **Note on Computer Vision models (`cv/`)**:
> Computer Vision models run natively on the host using the shared virtual environment (`cv/venv-cv`). Native execution allows direct webcam streaming (`--source 0`), GUI visualization (`cv2.imshow`), and zero-overhead hardware pipeline testing.

---

## Prerequisites

- Docker Engine 24.0+
- Docker Compose v2.20+
- *(Optional for GPU acceleration)*: NVIDIA Container Toolkit (`nvidia-ctk`) with an NVIDIA GPU (e.g., GTX 1650 or higher).

---

## 1. Build Base Image

Before launching any container, build the shared base image once:

### For CPU (Default / Universal):
```bash
docker build -f Dockerfile.base -t ml-base-cpu:latest .
```

### For GPU (NVIDIA CUDA):
```bash
docker build -f Dockerfile.base.gpu -t ml-base-gpu:latest .
```

---

## 2. Generate Docker Compose

Generate the unified `docker-compose.yml` service definitions:

```bash
python3 generate-compose.py
```

This automatically scans all model directories and registers each under its respective category profile.

---

## 3. Running Models (Preventing OOM Crashes)

Never run all 70+ services simultaneously with a plain `docker compose up`, as this will deplete host RAM. Use **Docker Profiles** to run specific categories:

### Run LLM Models Only:
```bash
docker compose --profile llm up -d
```

### Run Speech-to-Text (STT) Models Only:
```bash
docker compose --profile stt up -d
```

### Run Text-to-Speech (TTS) Models Only:
```bash
docker compose --profile tts up -d
```

### Run a Single Model Interactively:
```bash
docker compose up deepseek_r1_distill_qwen_1_5b_gguf
```

---

## 4. Resource Allocation & Caching

- **Hugging Face Cache**: Shared via volume mount `~/.cache/huggingface:/root/.cache/huggingface` to prevent re-downloading model weights across container restarts.
- **Model Storage**: Mapped to `./models/<model-name>:/app/models`.
