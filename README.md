# 100 Open-Source Model Review

This repo exists to test 100 open-source models, document the results, and keep a set of ready, verified models to reuse in future projects.

**Test environment:** laptop, NVIDIA GTX 1650 (4GB VRAM) — so the tests mostly cover small/quantized models. This shows which models are practically usable under limited GPU resources (typical of many small-to-mid-size projects in the Uzbekistan market).

**Categories:** LLM, CV (Computer Vision), TTS (Text-to-Speech), STT (Speech-to-Text) — with special attention to Uzbek language support.

---

## 📋 Model Index (quick overview for PM)

| Model | Category | Which project need it fits | GPU required | Estimated monthly cost | Same server as backend? | Details |
|---|---|---|---|---|---|---|
| **YOLOv8n** | CV | Camera-based monitoring, presence detection, object counting | No | $0 (runs on existing server) | ✅ Yes | [README](cv/yolov8n/README.md) |
| **YOLO11n** | CV | Smart Desk Focus & Distraction Monitor (Workplace ergonomics) | No | $0 (CPU / edge-ready) | ✅ Yes | [README](cv/yolo11n/README.md) |
| **YOLO11s** | CV | Retail & Checkout Queue Length Monitor (Retail flow analytics) | No | $0 (CPU / low-cost VPS) | ✅ Yes | [README](cv/yolo11s/README.md) |
| **YOLO11m** | CV | Industrial Hazard & Heavy Machinery Guardian (Workplace safety) | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](cv/yolo11m/README.md) |
| **YOLOv10n** | CV | Perimeter Intrusion & Tripwire Guardian (NMS-free security) | No | $0 (runs on existing server) | ✅ Yes | [README](cv/yolov10n/README.md) |
| **YOLOv10s** | CV | Smart Parking Bay & Loitering Patrol (Smart cities & surveillance) | No | $0 (CPU / low-cost VPS) | ✅ Yes | [README](cv/yolov10s/README.md) |
| **YOLOv9t** | CV | Highway Traffic Flow Counter (PGI dual-head speed & volume) | No | $0 (CPU / edge SBC) | ✅ Yes | [README](cv/yolov9t/README.md) |
| **YOLOv9s** | CV | Pedestrian Crosswalk & Jaywalking Guardian (Vision Zero alerts) | No | $0 (CPU / edge node) | ✅ Yes | [README](cv/yolov9s/README.md) |
| **YOLOv8s** | CV | Retail Loss Prevention Baggage Tracker (Anti-theft shopper audit) | No | $0 (CPU / edge server) | ✅ Yes | [README](cv/yolov8s/README.md) |
| **YOLOv8m** | CV | Crowd Spatial Density & Cluster Analyzer (Public event safety) | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](cv/yolov8m/README.md) |
| **YOLOv7-tiny** | CV | Commercial Facility Foot-Traffic Counter (Doorway flow monitor) | No | $0 (runs on existing server) | ✅ Yes | [README](cv/yolov7-tiny/README.md) |
| **YOLOv6n** | CV | Warehouse Conveyor Belt Throughput Monitor (Industrial sorting) | No | $0 (CPU / embedded device) | ✅ Yes | [README](cv/yolov6n/README.md) |
| **YOLOv6s** | CV | Freight Terminal Dock Bay Occupancy Inspector (Intermodal audit) | No | $0 (CPU / low-cost VPS) | ✅ Yes | [README](cv/yolov6s/README.md) |
| **YOLOv5n** | CV | Smart Office Energy Occupancy Guardian (HVAC / lighting savings) | No | $0 (CPU / edge IoT) | ✅ Yes | [README](cv/yolov5n/README.md) |
| **YOLOv5s** | CV | Urban Intersection Safety Analyzer (Vehicle/pedestrian risk) | No | $0 (CPU / edge box) | ✅ Yes | [README](cv/yolov5s/README.md) |
| **YOLOv5m** | CV | Commercial Fleet & Logistics Yard Dispatcher (Heavy transport) | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](cv/yolov5m/README.md) |
| **YOLOv4-tiny** | CV | Edge Micro-UAV Aerial Target Recon (Low-power drone SAR) | No | $0 (pure OpenCV DNN CPU) | ✅ Yes | [README](cv/yolov4-tiny/README.md) |
| **YOLOv3-tiny** | CV | Legacy CPU Vehicle Parking Gate Actuator (Boom barrier trigger) | No | $0 (runs on legacy x86/Atom) | ✅ Yes | [README](cv/yolov3-tiny/README.md) |
| **Qwen2.5-1.5B** | LLM | Local generative assistant, FAQ bot, structured data extractor | No | $0 (runs on CPU / 4GB GPU) | ✅ Yes | [README](llm/Qwen2.5-1.5B-Instruct-GGUF/README.md) |
| **FasterWhisper** | STT | Fast audio transcription & voice command parsing (Uzbek & Multi) | Optional | $0–$10 (CTranslate2 on CPU) | ✅ Yes | [README](stt/FasterWhisper/README.md) |
| **MMS-TTS-UZB** | TTS | Uzbek language text-to-speech audio synthesizer (Voice bots) | No | $0 (VITS architecture on CPU) | ✅ Yes | [README](tts/mms-tts-uzb/README.md) |

*(21 of 100 models reviewed and verified)*

---

## Repo structure

100-opensource-models-review/
├── README.md # this file — overall index
├── _template/ # template files and rules for adding a new model
├── cv/
│   ├── requirements.txt # unified master dependencies for all 18 CV models
│   ├── yolo11n/         # each model has demo.py, data/ (3 inputs & 3 outputs), and README.md
│   ├── yolo11s/
│   ├── yolo11m/
│   ├── yolov10n/
│   ├── yolov10s/
│   ├── yolov9t/
│   ├── yolov9s/
│   ├── yolov8n/
│   ├── yolov8s/
│   ├── yolov8m/
│   ├── yolov7-tiny/
│   ├── yolov6n/
│   ├── yolov6s/
│   ├── yolov5n/
│   ├── yolov5s/
│   ├── yolov5m/
│   ├── yolov4-tiny/
│   └── yolov3-tiny/
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

- **CV models**: Run directly in the dedicated, shared `cv/venv-cv` virtual environment (`pip install -r cv/requirements.txt`) with full local webcam (`--source 0`), GUI preview, or `--headless` batch processing.
- **LLM / TTS / STT models**: Run through Docker (`docker compose up --build` or `./run.sh`).

Rules and template files for adding a new model — [`_template/HOW_TO_ADD_A_MODEL.md`](_template/HOW_TO_ADD_A_MODEL.md).