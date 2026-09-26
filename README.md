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
| **MMS-TTS-UZB (Latin)** | TTS | Official Uzbek Latin text-to-speech audio synthesis (Government & Fintech) | No | $0 (runs on existing server / CPU) | ✅ Yes | [README](tts/mms-tts-uzb-latin/README.md) |
| **Bark-Small** | TTS | Expressive generative audio, audiobooks, dialogue with laughter and sighs | Optional | $0–$15 (CPU / entry GPU) | ✅ Yes | [README](tts/bark-small/README.md) |
| **Piper-TTS** | TTS | Ultra-fast local neural TTS for embedded systems, Raspberry Pi, and low-cost CPU VPS | No | $0 (runs on edge / $3 VPS) | ✅ Yes | [README](tts/piper-tts/README.md) |
| **Coqui-TTS-VITS** | TTS | End-to-end conditional variational autoencoder for low-latency voice bots | No | $0 (CPU-ready) | ✅ Yes | [README](tts/coqui-tts-vits/README.md) |
| **Coqui-XTTS-v2** | TTS | Zero-shot voice cloning across 17+ languages from 3-second reference audio | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](tts/coqui-xtts-v2/README.md) |
| **F5-TTS** | TTS | Non-autoregressive Flow Matching speech synthesis with rapid inference | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](tts/f5-tts/README.md) |
| **E2-TTS** | TTS | Duration-free non-autoregressive speech synthesis with instant alignment | Optional | $0–$15 (CPU / GPU) | ✅ Yes | [README](tts/e2-tts/README.md) |
| **Parler-TTS-Mini** | TTS | Controllable speech generation guided by natural language prompts (gender, tone, pace) | Optional | $0–$15 (CPU / GPU) | ✅ Yes | [README](tts/parler-tts-mini/README.md) |
| **CosyVoice-300M** | TTS | Multilingual zero-shot voice cloning and emotional conversational synthesis | Optional | $0–$15 (CPU / GPU) | ✅ Yes | [README](tts/cosyvoice-300m/README.md) |
| **ChatTTS** | TTS | Conversational dialogue synthesis optimized for LLM agents with laughter and filler words | No | $0 (runs on CPU) | ✅ Yes | [README](tts/chattts/README.md) |
| **OpenVoice-v2** | TTS | Instant versatile voice cloning with independent control over tone color and emotion | No | $0 (CPU-ready) | ✅ Yes | [README](tts/openvoice-v2/README.md) |
| **VALL-E-X** | TTS | Zero-shot cross-lingual speech synthesis and speech-to-speech translation | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](tts/valle-x/README.md) |
| **Tortoise-TTS** | TTS | Studio-quality multi-voice narration, audiobooks, and luxury voice generation | Recommended | $15–$30 (GPU required for speed) | ⚠️ Dedicated recommended | [README](tts/tortoise-tts/README.md) |
| **Matcha-TTS** | TTS | Fast, high-quality, lightweight non-autoregressive ODE flow matching | No | $0 (runs smoothly on CPU) | ✅ Yes | [README](tts/matcha-tts/README.md) |
| **SpeechT5-TTS** | TTS | Unified encoder-decoder framework with customizable x-vector speaker embeddings | No | $0 (CPU-ready) | ✅ Yes | [README](tts/speecht5-tts/README.md) |
| **FastSpeech2** | TTS | Deterministic ultra-fast non-autoregressive speech synthesis without word skipping | No | $0 (runs on CPU) | ✅ Yes | [README](tts/fastspeech2/README.md) |
| **Glow-TTS** | TTS | Generative flow parallel acoustic model with monotonic alignment search | No | $0 (CPU-ready) | ✅ Yes | [README](tts/glow-tts/README.md) |
| **Tacotron2** | TTS | Industry-classic recurrent sequence-to-sequence Mel-spectrogram generator | No | $0 (CPU-ready) | ✅ Yes | [README](tts/tacotron2/README.md) |
| **SeamlessM4T-TTS** | TTS | Expressive multilingual multi-task text-to-speech across 35+ languages | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](tts/seamless-m4t-tts/README.md) |
| **Fish-Speech-1.5** | TTS | Dual-autoregressive multi-lingual voice generator with low memory consumption | Optional | $0–$15 (CPU / GPU) | ✅ Yes | [README](tts/fish-speech-1.5/README.md) |
| **StyleTTS2** | TTS | Human-level speech synthesis using style diffusion and adversarial training | Optional | $0–$15 (CPU / GPU) | ✅ Yes | [README](tts/styletts2/README.md) |
| **MetaVoice-1B** | TTS | Conversational 1.2B foundation model trained on 100k hours of expressive dialogue | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](tts/meta-voice-1b/README.md) |
| **eSpeak-NG** | TTS | Microcontroller / embedded formant synthesizer with microsecond latency (<10MB RAM) | No | $0 (runs on $1 micro-server) | ✅ Yes | [README](tts/espeak-ng/README.md) |
| **Sherpa-ONNX-TTS** | TTS | Next-gen Kaldi embedded offline neural TTS for Android, iOS, and Linux edge SBCs | No | $0 (runs on edge / CPU) | ✅ Yes | [README](tts/sherpa-onnx-offline-tts/README.md) |
| **MMS-TTS-KAZ** | TTS | Sister Turkic language TTS for Central Asian regional localization and testing | No | $0 (CPU-ready) | ✅ Yes | [README](tts/mms-tts-kaz/README.md) |
| **Whisper-Large-v3-Turbo** | STT | High-accuracy enterprise transcription at 8x speed (pruned 4-layer decoder) | Optional | $0–$15 (CPU / GPU) | ✅ Yes | [README](stt/whisper-large-v3-turbo/README.md) |
| **Whisper-Tiny** | STT | Ultra-lightweight real-time transcription on low-end CPUs and IoT hardware | No | $0 (runs on $4 VPS) | ✅ Yes | [README](stt/whisper-tiny/README.md) |
| **Whisper-Base** | STT | Optimal balance of edge speed and acceptable transcription accuracy for bots | No | $0 (runs on existing server) | ✅ Yes | [README](stt/whisper-base/README.md) |
| **Whisper-Small-UZ** | STT | Domain-fine-tuned Uzbek speech recognition on Common Voice Uzbek corpus | No | $0 (runs on CPU) | ✅ Yes | [README](stt/whisper-small-uz/README.md) |
| **Whisper-Medium** | STT | Production-grade call-center analytics and complex multi-speaker transcription | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](stt/whisper-medium/README.md) |
| **Whisper.cpp** | STT | High-performance pure C/C++ ASR inference with zero Python runtime overhead | No | $0 (runs on bare-metal CPU) | ✅ Yes | [README](stt/whisper-cpp/README.md) |
| **Moonshine-Tiny** | STT | Instant edge streaming speech recognition without 30-second chunk latency | No | $0 (runs on microcontrollers) | ✅ Yes | [README](stt/moonshine-tiny/README.md) |
| **Moonshine-Base** | STT | Low-latency live microphone speech transcription for real-time captions | No | $0 (runs on CPU) | ✅ Yes | [README](stt/moonshine-base/README.md) |
| **Wav2Vec2-XLSR-UZ** | STT | End-to-end self-supervised acoustic CTC model fine-tuned for Uzbek speech | No | $0 (runs on CPU) | ✅ Yes | [README](stt/wav2vec2-large-xlsr-uz/README.md) |
| **MMS-1B-All** | STT | Meta 1,400-language foundation ASR model for universal speech recognition | Optional | $0–$15 (CPU / GPU) | ✅ Yes | [README](stt/mms-1b-all/README.md) |
| **Conformer-CTC** | STT | Enterprise call-center ASR combining self-attention with depthwise convolutions | No | $0 (runs on CPU) | ✅ Yes | [README](stt/conformer-ctc/README.md) |
| **NeMo-Canary-1B** | STT | Multitask speech transcription and translation with punctuation and capitalization | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](stt/nemo-canary-1b/README.md) |
| **SenseVoice-Small** | STT | Ultra-fast speech recognition (<100ms latency) with rich audio event and emotion detection | No | $0 (runs on CPU) | ✅ Yes | [README](stt/sensevoice-small/README.md) |
| **FunASR-Paraformer** | STT | Non-autoregressive industrial speech recognition with continuous streaming support | No | $0 (runs on CPU) | ✅ Yes | [README](stt/funasr-paraformer/README.md) |
| **Sherpa-ONNX-STT** | STT | Offline edge embedded speech recognition for Linux, Android, and IoT SBCs | No | $0 (runs on edge / $3 VPS) | ✅ Yes | [README](stt/sherpa-onnx-offline-stt/README.md) |
| **Vosk-API-UZ** | STT | Lightweight Kaldi-based offline speech recognizer (~50MB model) for mobile and Raspberry Pi | No | $0 (runs on CPU / embedded) | ✅ Yes | [README](stt/vosk-api-uz/README.md) |
| **Silero-STT** | STT | Enterprise-grade compact models running on single CPU thread (<30MB) with real-time streaming | No | $0 (runs on micro-server) | ✅ Yes | [README](stt/silero-stt/README.md) |
| **Zipformer-Transducer** | STT | Next-gen Kaldi Zipformer multi-rate transducer with exceptional parameter efficiency | No | $0 (runs on CPU) | ✅ Yes | [README](stt/zipformer-transducer/README.md) |
| **HuBERT-Large** | STT | Self-supervised speech representation model with k-means acoustic clustering | No | $0 (runs on CPU) | ✅ Yes | [README](stt/hubert-large-ls960/README.md) |
| **Data2Vec-Audio-Large** | STT | Unified multi-modal self-supervised architecture applied to speech recognition | No | $0 (runs on CPU) | ✅ Yes | [README](stt/data2vec-audio-large/README.md) |
| **WavLM-Large** | STT | Speech recognition with native background denoising and speaker verification | No | $0 (runs on CPU) | ✅ Yes | [README](stt/wavlm-large/README.md) |
| **SeamlessM4T-STT** | STT | Multilingual automatic speech recognition and speech-to-text translation across 100+ languages | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](stt/seamless-m4t-stt/README.md) |
| **Whisper-Timestamped** | STT | Accurate word-level timestamping and subtitle synchronization without hallucinations | No | $0 (runs on CPU) | ✅ Yes | [README](stt/whisper-timestamped/README.md) |
| **Insanely-Fast-Whisper** | STT | Batched ultra-fast pipeline inference using Flash Attention 2 and Hugging Face Optimum | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](stt/insanely-fast-whisper/README.md) |
| **Whisper-Diarization** | STT | Multi-speaker meeting transcription with speaker identification ('Who Spoke When') | Optional | $0–$15 (CPU / GPU) | ✅ Yes | [README](stt/whisper-diarization/README.md) |

*(100 of 100 models reviewed, scaffolded and verified — 100% COMPLETE)*

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
│   ├── mms-tts-uzb/
│   ├── mms-tts-uzb-latin/
│   ├── bark-small/
│   ├── piper-tts/
│   ├── coqui-tts-vits/
│   ├── coqui-xtts-v2/
│   ├── f5-tts/
│   ├── e2-tts/
│   ├── parler-tts-mini/
│   ├── cosyvoice-300m/
│   ├── chattts/
│   ├── openvoice-v2/
│   ├── valle-x/
│   ├── tortoise-tts/
│   ├── matcha-tts/
│   ├── speecht5-tts/
│   ├── fastspeech2/
│   ├── glow-tts/
│   ├── tacotron2/
│   ├── seamless-m4t-tts/
│   ├── fish-speech-1.5/
│   ├── styletts2/
│   ├── meta-voice-1b/
│   ├── espeak-ng/
│   ├── sherpa-onnx-offline-tts/
│   ├── mms-tts-kaz/
├── stt/
│   ├── FasterWhisper/
│   ├── whisper-large-v3-turbo/
│   ├── whisper-tiny/
│   ├── whisper-base/
│   ├── whisper-small-uz/
│   ├── whisper-medium/
│   ├── whisper-cpp/
│   ├── moonshine-tiny/
│   ├── moonshine-base/
│   ├── wav2vec2-large-xlsr-uz/
│   ├── mms-1b-all/
│   ├── conformer-ctc/
│   ├── nemo-canary-1b/
│   ├── sensevoice-small/
│   ├── funasr-paraformer/
│   ├── sherpa-onnx-offline-stt/
│   ├── vosk-api-uz/
│   ├── silero-stt/
│   ├── zipformer-transducer/
│   ├── hubert-large-ls960/
│   ├── data2vec-audio-large/
│   ├── wavlm-large/
│   ├── seamless-m4t-stt/
│   ├── whisper-timestamped/
│   ├── insanely-fast-whisper/
│   ├── whisper-diarization/
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