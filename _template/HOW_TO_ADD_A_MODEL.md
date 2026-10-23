# How to Add a New Model

This document outlines the standard engineering protocol for benchmarking and adding a new model to `100-opensource-models-review`.

---

## 1. Directory Structure

Each model must be placed in its respective category directory (`cv/`, `llm/`, `stt/`, or `tts/`).

```
category/
└── model-name/
    ├── README.md           # Standardized technical documentation
    ├── demo.py             # Minimal runnable CLI inference script
    ├── requirements.txt    # Specific Python dependencies
    └── Dockerfile          # Container setup (required for llm, stt, tts)
```

---

## 2. Category Execution Model

- **CV Models (`cv/`)**:
  - Run natively on the host using the shared virtual environment (`cv/venv-cv`).
  - Native execution ensures direct hardware access to laptop webcams (`--source 0`), GUI visualization (`cv2.imshow`), and local GPU acceleration without container pass-through overhead.
- **LLM, STT, and TTS Models (`llm/`, `stt/`, `tts/`)**:
  - Run containerized via Docker and `docker-compose.yml`.
  - Must inherit from `ml-base-cpu:latest` or `ml-base-gpu:latest`.

---

## 3. Required Files

### A. `README.md`
Every model README must follow this exact 4-part structure in English:
1. **Model Overview & Architecture**: Parameters, license, context window, quantization format.
2. **Benchmark & Resource Usage**: Measured latency, throughput (FPS or tokens/sec), RAM and VRAM footprints on the test environment (NVIDIA GTX 1650 4GB VRAM / CPU).
3. **Production Deployment & Sizing**: Recommended cloud VM specs, monthly estimated cost, scale feasibility.
4. **Quickstart & Usage**: Exact terminal commands to run `demo.py`.

### B. `demo.py`
- Self-contained and minimal.
- Supports both headless batch execution (for automated tests) and interactive mode.
- Downloads weights on demand to `models/` or Hugging Face cache (never commit binary weights to Git).
- No verbose boilerplate comments.

### C. `requirements.txt`
- Pins only packages strictly required on top of `ml-base` or `cv/requirements.txt`.

### D. `Dockerfile` (for LLM, STT, TTS)
```dockerfile
FROM ml-base-cpu:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "demo.py"]
```

---

## 4. Verification Checklist

- [ ] `demo.py` executes cleanly without unhandled exceptions.
- [ ] No binary weight files (`.pt`, `.bin`, `.onnx`, `.gguf`) are committed to Git.
- [ ] `README.md` adheres to the 4-section standard.
- [ ] Model is registered in root `README.md` Model Index table.
- [ ] If LLM/TTS/STT: Docker service generated via `python3 generate-compose.py`.
