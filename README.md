# 100 Open-Source Model Review

This repo exists to test 100 open-source models, document the results, and keep a set of ready, verified models to reuse in future projects.

**Test environment:** laptop, NVIDIA GTX 1650 (4GB VRAM) — so the tests mostly cover small/quantized models. This shows which models are practically usable under limited GPU resources (typical of many small-to-mid-size projects in the Uzbekistan market).

**Categories:** LLM, CV (Computer Vision), TTS (Text-to-Speech), STT (Speech-to-Text) — with special attention to Uzbek language support.

---

## 📋 Model Index (quick overview for PM)

| Model | Category | Which project need it fits | GPU required | Estimated monthly cost | Same server as backend? | Details |
|---|---|---|---|---|---|---|
| YOLOv8n | CV | Camera-based monitoring, presence detection, object counting | No | $0 (runs on existing server) | ✅ Yes | [README](cv/yolov8n/README.md) |

*(A new row is added to this table each time a new model is added.)*

---

## Repo structure

100-opensource-models-review/
├── README.md # this file — overall index
├── _template/ # template files and rules for adding a new model
├── cv/
│ └── yolov8n/ # each model lives in its own folder, with its own README
├── llm/
├── tts/
├── stt/
└── benchmark_scripts/ # shared benchmark scripts per category

## What's in each model's README

- Technical info about the model (architecture, parameters, versions)
- What was done in the project and what issues were encountered
- GPU compatibility and resource requirements (CPU-only or GPU-required)
- Estimated monthly cost if run in the cloud
- How to run it

## Running the models

Each model folder is self-contained — it has its own `Dockerfile`, `docker-compose.yml`, and `README.md`.

- **LLM / TTS / STT models** — run only through Docker (`docker compose up --build` or `./run.sh`), no venv or manual package installation needed.
- **CV models** (when a camera/GUI is needed) — two modes are provided: native (venv, with a GUI window) and Docker (headless). The reason is explained in that model's own README.

Rules and template files for adding a new model — [`_template/HOW_TO_ADD_A_MODEL.md`](_template/HOW_TO_ADD_A_MODEL.md).