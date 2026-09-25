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
| **Depth-Anything-V2** | CV | Monocular 3D Depth Estimation, LiDAR-free spatial distance | Optional | $0 (CPU / edge-ready) | ✅ Yes | [README](cv/depth-anything-v2-small/README.md) |
| **YOLO11n-Pose** | CV | 17-Keypoint Human Skeleton & Workplace Posture / Fitness Tracker | No | $0 (CPU / edge-ready) | ✅ Yes | [README](cv/yolo11n-pose/README.md) |
| **YOLO11n-Seg** | CV | Multi-Class Instance Segmentation & Pixel-Accurate Object Masking | No | $0 (CPU / edge-ready) | ✅ Yes | [README](cv/yolo11n-seg/README.md) |
| **YOLO-World (v2)** | CV | Open-Vocabulary Zero-Shot Detection (Arbitrary prompt querying) | No | $0 (CPU / edge-ready) | ✅ Yes | [README](cv/yolov8s-worldv2/README.md) |
| **OpenCV-Stream** | CV | Zero-latency RTSP/Webcam stream ingestion & frame telemetry | No | $0 (pure CPU pipeline) | ✅ Yes | [README](cv/opencv-video-stream/README.md) |
| **YOLO-Office-Detection** | CV | Workplace presence, IT equipment & distraction alert detector | No | $0 (runs on edge/CPU) | ✅ Yes | [README](cv/yolo-object-detection/README.md) |
| **InsightFace (ArcFace)** | CV | SOTA SCRFD + ArcFace ResNet-50 biometric face identification | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](cv/insightface-arcface/README.md) |
| **YOLO-Pose-Sleeping** | CV | 17-Keypoint skeleton workplace fatigue, posture & sleep analyzer | No | $0 (CPU / edge-ready) | ✅ Yes | [README](cv/yolo-pose-sleeping/README.md) |
| **ByteTrack-MOT** | CV | Multi-Object Tracking (MOT), persistent ID assignment & trajectories | No | $0 (CPU Kalman/Hungarian) | ✅ Yes | [README](cv/bytetrack-mot/README.md) |
| **DeepSeek-R1-1.5B** | LLM | Offline reasoning engine with Chain-of-Thought (<think>) for math/logic | No | $0 (runs on CPU / 4GB GPU) | ✅ Yes | [README](llm/DeepSeek-R1-Distill-Qwen-1.5B-GGUF/README.md) |
| **DeepSeek-R1-Llama-8B** | LLM | Deep reasoning, proof by contradiction & logic deduction (Meta Llama-3.1) | Recommended | $0–$25 (runs on CPU / 8GB GPU) | ✅ Yes | [README](llm/DeepSeek-R1-Distill-Llama-8B-GGUF/README.md) |
| **Qwen2.5-Coder-1.5B** | LLM | Local Copilot, code generation, refactoring & syntax repair (5.5T tokens) | No | $0 (runs on CPU / 4GB GPU) | ✅ Yes | [README](llm/Qwen2.5-Coder-1.5B-Instruct-GGUF/README.md) |
| **DeepSeek-Coder-V2-Lite** | LLM | Mixture-of-Experts (MoE) 16B/2.4B active code model, 338 languages, 128k context | Optional | $0–$15 (runs on CPU / 8GB GPU) | ✅ Yes | [README](llm/DeepSeek-Coder-V2-Lite-Instruct-GGUF/README.md) |
| **StarCoder2-3B** | LLM | BigCode enterprise-safe code generation (The Stack v2, 100% Permissive) | No | $0 (runs on CPU / 4GB GPU) | ✅ Yes | [README](llm/StarCoder2-3B-GGUF/README.md) |
| **Hermes-3-Llama-3.2-3B** | LLM | Autonomous agent execution, function calling `<tools>`, structured JSON schema | No | $0 (runs on CPU / 4GB GPU) | ✅ Yes | [README](llm/Hermes-3-Llama-3.2-3B-GGUF/README.md) |
| **SmolLM2-1.7B** | LLM | HuggingFace 11T-token curated synthetic model, ultra-compact mobile/edge | No | $0 (runs on CPU / 2GB RAM) | ✅ Yes | [README](llm/SmolLM2-1.7B-Instruct-GGUF/README.md) |
| **Llama-3.2-1B** | LLM | Meta official smartphone/IoT edge engine, 128k context, ~800MB RAM | No | $0 (runs on CPU / 1GB RAM) | ✅ Yes | [README](llm/Llama-3.2-1B-Instruct-GGUF/README.md) |
| **Llama-Guard-3-1B** | LLM | Meta AI safety & content moderation classifier (S1-S14 hazard policies) | No | $0 (runs on CPU, ~50ms audit) | ✅ Yes | [README](llm/Llama-Guard-3-1B-GGUF/README.md) |
| **Phi-3.5-mini** | LLM | Microsoft 3.8B high-density synthetic reasoning, 128k context, math/logic SOTA | No | $0 (runs on CPU / 4GB GPU) | ✅ Yes | [README](llm/Phi-3.5-mini-instruct-GGUF/README.md) |
| **Mistral-7B-v0.3** | LLM | European SOTA 7B flagship, Tekken tokenizer, 32k context, native function calling | Recommended | $0–$25 (runs on CPU / 6GB GPU) | ✅ Yes | [README](llm/Mistral-7B-Instruct-v0.3-GGUF/README.md) |
| **Llama-3.1-8B** | LLM | Meta industry-standard 8B foundation, 15T tokens, 128k context, enterprise RAG | Recommended | $0–$25 (runs on CPU / 8GB GPU) | ✅ Yes | [README](llm/Llama-3.1-8B-Instruct-GGUF/README.md) |
| **Qwen2-VL-2B** | LLM | Vision-Language multimodal understanding (VLM), image OCR, chart & document VQA | No | $0 (runs on CPU / 4GB GPU) | ✅ Yes | [README](llm/Qwen2-VL-2B-Instruct-GGUF/README.md) |
| **Moondream2** | LLM | Ultra-lightweight Tiny VLM (~1.86B), instant edge visual Q&A & image captioning | No | $0 (runs on CPU / 2GB RAM) | ✅ Yes | [README](llm/Moondream2-GGUF/README.md) |
| **BGE-M3** | LLM | World SOTA multilingual semantic embedding (1024-d, 8192 context, Uzbek+100 lang) | No | $0 (runs on CPU, ~20ms latency) | ✅ Yes | [README](llm/bge-m3/README.md) |
| **BGE-Reranker-v2-M3** | LLM | Cross-Encoder RAG reranker (Full Cross-Attention, false-positive elimination) | No | $0 (runs on CPU, ~30ms latency) | ✅ Yes | [README](llm/bge-reranker-v2-m3/README.md) |
| **NLLB-200-Distilled** | LLM | Meta 200-language direct neural machine translation (Uzbek Latin & Cyrillic) | No | $0 (runs on CPU, ~200ms latency) | ✅ Yes | [README](llm/NLLB-200-Distilled-600M/README.md) |
| **Gemma-2-2B** | LLM | Google flagship 2.6B lightweight model, Sliding Window Attention, soft-capping | No | $0 (runs on CPU / 2GB RAM) | ✅ Yes | [README](llm/Gemma-2-2B-Instruct-GGUF/README.md) |
| **Qwen2.5-3B** | LLM | Alibaba 3B sweet-spot powerhouse, 18T tokens, deep Uzbek & Turkic multilingual | No | $0 (runs on CPU / 4GB GPU) | ✅ Yes | [README](llm/Qwen2.5-3B-Instruct-GGUF/README.md) |
| **Granite-3.0-2B** | LLM | IBM enterprise foundation model, 12T tokens, 100% Apache 2.0 unencumbered license | No | $0 (runs on CPU / 2GB RAM) | ✅ Yes | [README](llm/Granite-3.0-2B-Instruct-GGUF/README.md) |

*(50 of 100 models reviewed, scaffolded and verified)*

---

## Repo structure

100-opensource-models-review/
├── README.md # this file — overall index
├── _template/ # template files and rules for adding a new model
├── cv/
│   ├── requirements.txt # unified master dependencies for all 27 CV models
│   ├── yolo11n/         # each model has demo.py, data/ (3 inputs & 3 outputs), and README.md
│   ├── yolo11s/
│   ├── yolo11m/
│   ├── yolo11n-pose/
│   ├── yolo11n-seg/
│   ├── yolov8s-worldv2/
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
│   ├── yolov3-tiny/
│   ├── depth-anything-v2-small/
│   ├── opencv-video-stream/
│   ├── yolo-object-detection/
│   ├── insightface-arcface/
│   ├── yolo-pose-sleeping/
│   └── bytetrack-mot/
├── llm/
│   ├── Qwen2.5-1.5B-Instruct-GGUF/
│   ├── DeepSeek-R1-Distill-Qwen-1.5B-GGUF/
│   ├── DeepSeek-R1-Distill-Llama-8B-GGUF/
│   ├── Qwen2.5-Coder-1.5B-Instruct-GGUF/
│   ├── DeepSeek-Coder-V2-Lite-Instruct-GGUF/
│   ├── StarCoder2-3B-GGUF/
│   ├── Hermes-3-Llama-3.2-3B-GGUF/
│   ├── SmolLM2-1.7B-Instruct-GGUF/
│   ├── Llama-3.2-1B-Instruct-GGUF/
│   ├── Llama-Guard-3-1B-GGUF/
│   ├── Phi-3.5-mini-instruct-GGUF/
│   ├── Mistral-7B-Instruct-v0.3-GGUF/
│   ├── Llama-3.1-8B-Instruct-GGUF/
│   ├── Qwen2-VL-2B-Instruct-GGUF/
│   ├── Moondream2-GGUF/
│   ├── bge-m3/
│   ├── bge-reranker-v2-m3/
│   ├── NLLB-200-Distilled-600M/
│   ├── Gemma-2-2B-Instruct-GGUF/
│   ├── Qwen2.5-3B-Instruct-GGUF/
│   └── Granite-3.0-2B-Instruct-GGUF/
├── tts/
│   └── mms-tts-uzb/
├── stt/
│   └── FasterWhisper/
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