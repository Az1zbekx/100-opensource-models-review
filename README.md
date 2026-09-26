# 100 Open-Source Model Review

This repo exists to test 100 open-source models, document the results, and keep a set of ready, verified models to reuse in future projects.

**Test environment:** laptop, NVIDIA GTX 1650 (4GB VRAM) — so the tests mostly cover small/quantized models. This shows which models are practically usable under limited GPU resources (typical of many small-to-mid-size projects in the Uzbekistan market).

**Categories:** LLM, CV (Computer Vision), TTS (Text-to-Speech), STT (Speech-to-Text) — with special attention to Uzbek language support.

---

## 📋 Model Index (quick overview for PM)

| # | Model | Category | Which project need it fits | GPU required | Estimated monthly cost | Same server as backend? | Details |
|---|---|---|---|---|---|---|---|
| **1** | **YOLOv8n** | CV | Camera-based monitoring, presence detection, object counting | No | $0 (runs on existing server) | ✅ Yes | [README](cv/yolov8n/README.md) |
| **2** | **YOLO11n** | CV | Smart Desk Focus & Distraction Monitor (Workplace ergonomics) | No | $0 (CPU / edge-ready) | ✅ Yes | [README](cv/yolo11n/README.md) |
| **3** | **YOLO11s** | CV | Retail & Checkout Queue Length Monitor (Retail flow analytics) | No | $0 (CPU / low-cost VPS) | ✅ Yes | [README](cv/yolo11s/README.md) |
| **4** | **YOLO11m** | CV | Industrial Hazard & Heavy Machinery Guardian (Workplace safety) | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](cv/yolo11m/README.md) |
| **5** | **YOLOv10n** | CV | Perimeter Intrusion & Tripwire Guardian (NMS-free security) | No | $0 (runs on existing server) | ✅ Yes | [README](cv/yolov10n/README.md) |
| **6** | **YOLOv10s** | CV | Smart Parking Bay & Loitering Patrol (Smart cities & surveillance) | No | $0 (CPU / low-cost VPS) | ✅ Yes | [README](cv/yolov10s/README.md) |
| **7** | **YOLOv9t** | CV | Highway Traffic Flow Counter (PGI dual-head speed & volume) | No | $0 (CPU / edge SBC) | ✅ Yes | [README](cv/yolov9t/README.md) |
| **8** | **YOLOv9s** | CV | Pedestrian Crosswalk & Jaywalking Guardian (Vision Zero alerts) | No | $0 (CPU / edge node) | ✅ Yes | [README](cv/yolov9s/README.md) |
| **9** | **YOLOv8s** | CV | Retail Loss Prevention Baggage Tracker (Anti-theft shopper audit) | No | $0 (CPU / edge server) | ✅ Yes | [README](cv/yolov8s/README.md) |
| **10** | **YOLOv8m** | CV | Crowd Spatial Density & Cluster Analyzer (Public event safety) | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](cv/yolov8m/README.md) |
| **11** | **YOLOv7-tiny** | CV | Commercial Facility Foot-Traffic Counter (Doorway flow monitor) | No | $0 (runs on existing server) | ✅ Yes | [README](cv/yolov7-tiny/README.md) |
| **12** | **YOLOv6n** | CV | Warehouse Conveyor Belt Throughput Monitor (Industrial sorting) | No | $0 (CPU / embedded device) | ✅ Yes | [README](cv/yolov6n/README.md) |
| **13** | **YOLOv6s** | CV | Freight Terminal Dock Bay Occupancy Inspector (Intermodal audit) | No | $0 (CPU / low-cost VPS) | ✅ Yes | [README](cv/yolov6s/README.md) |
| **14** | **YOLOv5n** | CV | Smart Office Energy Occupancy Guardian (HVAC / lighting savings) | No | $0 (CPU / edge IoT) | ✅ Yes | [README](cv/yolov5n/README.md) |
| **15** | **YOLOv5s** | CV | Urban Intersection Safety Analyzer (Vehicle/pedestrian risk) | No | $0 (CPU / edge box) | ✅ Yes | [README](cv/yolov5s/README.md) |
| **16** | **YOLOv5m** | CV | Commercial Fleet & Logistics Yard Dispatcher (Heavy transport) | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](cv/yolov5m/README.md) |
| **17** | **YOLOv4-tiny** | CV | Edge Micro-UAV Aerial Target Recon (Low-power drone SAR) | No | $0 (pure OpenCV DNN CPU) | ✅ Yes | [README](cv/yolov4-tiny/README.md) |
| **18** | **YOLOv3-tiny** | CV | Legacy CPU Vehicle Parking Gate Actuator (Boom barrier trigger) | No | $0 (runs on legacy x86/Atom) | ✅ Yes | [README](cv/yolov3-tiny/README.md) |
| **19** | **Depth-Anything-V2** | CV | Monocular 3D Depth Estimation, LiDAR-free spatial distance | Optional | $0 (CPU / edge-ready) | ✅ Yes | [README](cv/depth-anything-v2-small/README.md) |
| **20** | **YOLO11n-Pose** | CV | 17-Keypoint Human Skeleton & Workplace Posture / Fitness Tracker | No | $0 (CPU / edge-ready) | ✅ Yes | [README](cv/yolo11n-pose/README.md) |
| **21** | **YOLO11n-Seg** | CV | Multi-Class Instance Segmentation & Pixel-Accurate Object Masking | No | $0 (CPU / edge-ready) | ✅ Yes | [README](cv/yolo11n-seg/README.md) |
| **22** | **YOLO-World (v2)** | CV | Open-Vocabulary Zero-Shot Detection (Arbitrary prompt querying) | No | $0 (CPU / edge-ready) | ✅ Yes | [README](cv/yolov8s-worldv2/README.md) |
| **23** | **OpenCV-Stream** | CV | Zero-latency RTSP/Webcam stream ingestion & frame telemetry | No | $0 (pure CPU pipeline) | ✅ Yes | [README](cv/opencv-video-stream/README.md) |
| **24** | **YOLO-Office-Detection** | CV | Workplace presence, IT equipment & distraction alert detector | No | $0 (runs on edge/CPU) | ✅ Yes | [README](cv/yolo-object-detection/README.md) |
| **25** | **InsightFace (ArcFace)** | CV | SOTA SCRFD + ArcFace ResNet-50 biometric face identification | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](cv/insightface-arcface/README.md) |
| **26** | **YOLO-Pose-Sleeping** | CV | 17-Keypoint skeleton workplace fatigue, posture & sleep analyzer | No | $0 (CPU / edge-ready) | ✅ Yes | [README](cv/yolo-pose-sleeping/README.md) |
| **27** | **ByteTrack-MOT** | CV | Multi-Object Tracking (MOT), persistent ID assignment & trajectories | No | $0 (CPU Kalman/Hungarian) | ✅ Yes | [README](cv/bytetrack-mot/README.md) |
| **28** | **BGE-M3** | LLM | World SOTA multilingual semantic embedding (1024-d, 8192 context, Uzbek+100 lang) | No | $0 (runs on CPU, ~20ms latency) | ✅ Yes | [README](llm/bge-m3/README.md) |
| **29** | **BGE-Reranker-v2-M3** | LLM | Cross-Encoder RAG reranker (Full Cross-Attention, false-positive elimination) | No | $0 (runs on CPU, ~30ms latency) | ✅ Yes | [README](llm/bge-reranker-v2-m3/README.md) |
| **30** | **DeepSeek-Coder-V2-Lite** | LLM | Mixture-of-Experts (MoE) 16B/2.4B active code model, 338 languages, 128k context | Optional | $0–$15 (runs on CPU / 8GB GPU) | ✅ Yes | [README](llm/DeepSeek-Coder-V2-Lite-Instruct-GGUF/README.md) |
| **31** | **DeepSeek-R1-1.5B** | LLM | Offline reasoning engine with Chain-of-Thought (<think>) for math/logic | No | $0 (runs on CPU / 4GB GPU) | ✅ Yes | [README](llm/DeepSeek-R1-Distill-Qwen-1.5B-GGUF/README.md) |
| **32** | **DeepSeek-R1-Llama-8B** | LLM | Deep reasoning, proof by contradiction & logic deduction (Meta Llama-3.1) | Recommended | $0–$25 (runs on CPU / 8GB GPU) | ✅ Yes | [README](llm/DeepSeek-R1-Distill-Llama-8B-GGUF/README.md) |
| **33** | **Gemma-2-2B** | LLM | Google flagship 2.6B lightweight model, Sliding Window Attention, soft-capping | No | $0 (runs on CPU / 2GB RAM) | ✅ Yes | [README](llm/Gemma-2-2B-Instruct-GGUF/README.md) |
| **34** | **Granite-3.0-2B** | LLM | IBM enterprise foundation model, 12T tokens, 100% Apache 2.0 unencumbered license | No | $0 (runs on CPU / 2GB RAM) | ✅ Yes | [README](llm/Granite-3.0-2B-Instruct-GGUF/README.md) |
| **35** | **Hermes-3-Llama-3.2-3B** | LLM | Autonomous agent execution, function calling `<tools>`, structured JSON schema | No | $0 (runs on CPU / 4GB GPU) | ✅ Yes | [README](llm/Hermes-3-Llama-3.2-3B-GGUF/README.md) |
| **36** | **Llama-3.1-8B** | LLM | Meta industry-standard 8B foundation, 15T tokens, 128k context, enterprise RAG | Recommended | $0–$25 (runs on CPU / 8GB GPU) | ✅ Yes | [README](llm/Llama-3.1-8B-Instruct-GGUF/README.md) |
| **37** | **Llama-3.2-1B** | LLM | Meta official smartphone/IoT edge engine, 128k context, ~800MB RAM | No | $0 (runs on CPU / 1GB RAM) | ✅ Yes | [README](llm/Llama-3.2-1B-Instruct-GGUF/README.md) |
| **38** | **Llama-Guard-3-1B** | LLM | Meta AI safety & content moderation classifier (S1-S14 hazard policies) | No | $0 (runs on CPU, ~50ms audit) | ✅ Yes | [README](llm/Llama-Guard-3-1B-GGUF/README.md) |
| **39** | **Mistral-7B-v0.3** | LLM | European SOTA 7B flagship, Tekken tokenizer, 32k context, native function calling | Recommended | $0–$25 (runs on CPU / 6GB GPU) | ✅ Yes | [README](llm/Mistral-7B-Instruct-v0.3-GGUF/README.md) |
| **40** | **Moondream2** | LLM | Ultra-lightweight Tiny VLM (~1.86B), instant edge visual Q&A & image captioning | No | $0 (runs on CPU / 2GB RAM) | ✅ Yes | [README](llm/Moondream2-GGUF/README.md) |
| **41** | **NLLB-200-Distilled** | LLM | Meta 200-language direct neural machine translation (Uzbek Latin & Cyrillic) | No | $0 (runs on CPU, ~200ms latency) | ✅ Yes | [README](llm/NLLB-200-Distilled-600M/README.md) |
| **42** | **Phi-3.5-mini** | LLM | Microsoft 3.8B high-density synthetic reasoning, 128k context, math/logic SOTA | No | $0 (runs on CPU / 4GB GPU) | ✅ Yes | [README](llm/Phi-3.5-mini-instruct-GGUF/README.md) |
| **43** | **Qwen2-VL-2B** | LLM | Vision-Language multimodal understanding (VLM), image OCR, chart & document VQA | No | $0 (runs on CPU / 4GB GPU) | ✅ Yes | [README](llm/Qwen2-VL-2B-Instruct-GGUF/README.md) |
| **44** | **Qwen2.5-1.5B** | LLM | Local generative assistant, FAQ bot, structured data extractor | No | $0 (runs on CPU / 4GB GPU) | ✅ Yes | [README](llm/Qwen2.5-1.5B-Instruct-GGUF/README.md) |
| **45** | **Qwen2.5-3B** | LLM | Alibaba 3B sweet-spot powerhouse, 18T tokens, deep Uzbek & Turkic multilingual | No | $0 (runs on CPU / 4GB GPU) | ✅ Yes | [README](llm/Qwen2.5-3B-Instruct-GGUF/README.md) |
| **46** | **Qwen2.5-Coder-1.5B** | LLM | Local Copilot, code generation, refactoring & syntax repair (5.5T tokens) | No | $0 (runs on CPU / 4GB GPU) | ✅ Yes | [README](llm/Qwen2.5-Coder-1.5B-Instruct-GGUF/README.md) |
| **47** | **SmolLM2-1.7B** | LLM | HuggingFace 11T-token curated synthetic model, ultra-compact mobile/edge | No | $0 (runs on CPU / 2GB RAM) | ✅ Yes | [README](llm/SmolLM2-1.7B-Instruct-GGUF/README.md) |
| **48** | **StarCoder2-3B** | LLM | BigCode enterprise-safe code generation (The Stack v2, 100% Permissive) | No | $0 (runs on CPU / 4GB GPU) | ✅ Yes | [README](llm/StarCoder2-3B-GGUF/README.md) |
| **49** | **Bark-Small** | TTS | Expressive generative audio, audiobooks, dialogue with laughter and sighs | Optional | $0–$15 (CPU / entry GPU) | ✅ Yes | [README](tts/bark-small/README.md) |
| **50** | **ChatTTS** | TTS | Conversational dialogue synthesis optimized for LLM agents with laughter and filler words | No | $0 (runs on CPU) | ✅ Yes | [README](tts/chattts/README.md) |
| **51** | **Coqui-TTS-VITS** | TTS | End-to-end conditional variational autoencoder for low-latency voice bots | No | $0 (CPU-ready) | ✅ Yes | [README](tts/coqui-tts-vits/README.md) |
| **52** | **Coqui-XTTS-v2** | TTS | Zero-shot voice cloning across 17+ languages from 3-second reference audio | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](tts/coqui-xtts-v2/README.md) |
| **53** | **CosyVoice-300M** | TTS | Multilingual zero-shot voice cloning and emotional conversational synthesis | Optional | $0–$15 (CPU / GPU) | ✅ Yes | [README](tts/cosyvoice-300m/README.md) |
| **54** | **E2-TTS** | TTS | Duration-free non-autoregressive speech synthesis with instant alignment | Optional | $0–$15 (CPU / GPU) | ✅ Yes | [README](tts/e2-tts/README.md) |
| **55** | **eSpeak-NG** | TTS | Microcontroller / embedded formant synthesizer with microsecond latency (<10MB RAM) | No | $0 (runs on $1 micro-server) | ✅ Yes | [README](tts/espeak-ng/README.md) |
| **56** | **F5-TTS** | TTS | Non-autoregressive Flow Matching speech synthesis with rapid inference | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](tts/f5-tts/README.md) |
| **57** | **FastSpeech2** | TTS | Deterministic ultra-fast non-autoregressive speech synthesis without word skipping | No | $0 (runs on CPU) | ✅ Yes | [README](tts/fastspeech2/README.md) |
| **58** | **Fish-Speech-1.5** | TTS | Dual-autoregressive multi-lingual voice generator with low memory consumption | Optional | $0–$15 (CPU / GPU) | ✅ Yes | [README](tts/fish-speech-1.5/README.md) |
| **59** | **Glow-TTS** | TTS | Generative flow parallel acoustic model with monotonic alignment search | No | $0 (CPU-ready) | ✅ Yes | [README](tts/glow-tts/README.md) |
| **60** | **Matcha-TTS** | TTS | Fast, high-quality, lightweight non-autoregressive ODE flow matching | No | $0 (runs smoothly on CPU) | ✅ Yes | [README](tts/matcha-tts/README.md) |
| **61** | **MetaVoice-1B** | TTS | Conversational 1.2B foundation model trained on 100k hours of expressive dialogue | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](tts/meta-voice-1b/README.md) |
| **62** | **MMS-TTS-KAZ** | TTS | Sister Turkic language TTS for Central Asian regional localization and testing | No | $0 (CPU-ready) | ✅ Yes | [README](tts/mms-tts-kaz/README.md) |
| **63** | **MMS-TTS-UZB (Latin)** | TTS | Official Uzbek Latin text-to-speech audio synthesis (Government & Fintech) | No | $0 (runs on existing server / CPU) | ✅ Yes | [README](tts/mms-tts-uzb-latin/README.md) |
| **64** | **MMS-TTS-UZB** | TTS | Uzbek language text-to-speech audio synthesizer (Voice bots) | No | $0 (VITS architecture on CPU) | ✅ Yes | [README](tts/mms-tts-uzb/README.md) |
| **65** | **OpenVoice-v2** | TTS | Instant versatile voice cloning with independent control over tone color and emotion | No | $0 (CPU-ready) | ✅ Yes | [README](tts/openvoice-v2/README.md) |
| **66** | **Parler-TTS-Mini** | TTS | Controllable speech generation guided by natural language prompts (gender, tone, pace) | Optional | $0–$15 (CPU / GPU) | ✅ Yes | [README](tts/parler-tts-mini/README.md) |
| **67** | **Piper-TTS** | TTS | Ultra-fast local neural TTS for embedded systems, Raspberry Pi, and low-cost CPU VPS | No | $0 (runs on edge / $3 VPS) | ✅ Yes | [README](tts/piper-tts/README.md) |
| **68** | **SeamlessM4T-TTS** | TTS | Expressive multilingual multi-task text-to-speech across 35+ languages | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](tts/seamless-m4t-tts/README.md) |
| **69** | **Sherpa-ONNX-TTS** | TTS | Next-gen Kaldi embedded offline neural TTS for Android, iOS, and Linux edge SBCs | No | $0 (runs on edge / CPU) | ✅ Yes | [README](tts/sherpa-onnx-offline-tts/README.md) |
| **70** | **SpeechT5-TTS** | TTS | Unified encoder-decoder framework with customizable x-vector speaker embeddings | No | $0 (CPU-ready) | ✅ Yes | [README](tts/speecht5-tts/README.md) |
| **71** | **StyleTTS2** | TTS | Human-level speech synthesis using style diffusion and adversarial training | Optional | $0–$15 (CPU / GPU) | ✅ Yes | [README](tts/styletts2/README.md) |
| **72** | **Tacotron2** | TTS | Industry-classic recurrent sequence-to-sequence Mel-spectrogram generator | No | $0 (CPU-ready) | ✅ Yes | [README](tts/tacotron2/README.md) |
| **73** | **Tortoise-TTS** | TTS | Studio-quality multi-voice narration, audiobooks, and luxury voice generation | Recommended | $15–$30 (GPU required for speed) | ⚠️ Dedicated recommended | [README](tts/tortoise-tts/README.md) |
| **74** | **VALL-E-X** | TTS | Zero-shot cross-lingual speech synthesis and speech-to-speech translation | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](tts/valle-x/README.md) |
| **75** | **Conformer-CTC** | STT | Enterprise call-center ASR combining self-attention with depthwise convolutions | No | $0 (runs on CPU) | ✅ Yes | [README](stt/conformer-ctc/README.md) |
| **76** | **Data2Vec-Audio-Large** | STT | Unified multi-modal self-supervised architecture applied to speech recognition | No | $0 (runs on CPU) | ✅ Yes | [README](stt/data2vec-audio-large/README.md) |
| **77** | **FasterWhisper** | STT | Fast audio transcription & voice command parsing (Uzbek & Multi) | Optional | $0–$10 (CTranslate2 on CPU) | ✅ Yes | [README](stt/FasterWhisper/README.md) |
| **78** | **FunASR-Paraformer** | STT | Non-autoregressive industrial speech recognition with continuous streaming support | No | $0 (runs on CPU) | ✅ Yes | [README](stt/funasr-paraformer/README.md) |
| **79** | **HuBERT-Large** | STT | Self-supervised speech representation model with k-means acoustic clustering | No | $0 (runs on CPU) | ✅ Yes | [README](stt/hubert-large-ls960/README.md) |
| **80** | **Insanely-Fast-Whisper** | STT | Batched ultra-fast pipeline inference using Flash Attention 2 and Hugging Face Optimum | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](stt/insanely-fast-whisper/README.md) |
| **81** | **MMS-1B-All** | STT | Meta 1,400-language foundation ASR model for universal speech recognition | Optional | $0–$15 (CPU / GPU) | ✅ Yes | [README](stt/mms-1b-all/README.md) |
| **82** | **Moonshine-Base** | STT | Low-latency live microphone speech transcription for real-time captions | No | $0 (runs on CPU) | ✅ Yes | [README](stt/moonshine-base/README.md) |
| **83** | **Moonshine-Tiny** | STT | Instant edge streaming speech recognition without 30-second chunk latency | No | $0 (runs on microcontrollers) | ✅ Yes | [README](stt/moonshine-tiny/README.md) |
| **84** | **NeMo-Canary-1B** | STT | Multitask speech transcription and translation with punctuation and capitalization | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](stt/nemo-canary-1b/README.md) |
| **85** | **SeamlessM4T-STT** | STT | Multilingual automatic speech recognition and speech-to-text translation across 100+ languages | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](stt/seamless-m4t-stt/README.md) |
| **86** | **SenseVoice-Small** | STT | Ultra-fast speech recognition (<100ms latency) with rich audio event and emotion detection | No | $0 (runs on CPU) | ✅ Yes | [README](stt/sensevoice-small/README.md) |
| **87** | **Sherpa-ONNX-STT** | STT | Offline edge embedded speech recognition for Linux, Android, and IoT SBCs | No | $0 (runs on edge / $3 VPS) | ✅ Yes | [README](stt/sherpa-onnx-offline-stt/README.md) |
| **88** | **Silero-STT** | STT | Enterprise-grade compact models running on single CPU thread (<30MB) with real-time streaming | No | $0 (runs on micro-server) | ✅ Yes | [README](stt/silero-stt/README.md) |
| **89** | **Vosk-API-UZ** | STT | Lightweight Kaldi-based offline speech recognizer (~50MB model) for mobile and Raspberry Pi | No | $0 (runs on CPU / embedded) | ✅ Yes | [README](stt/vosk-api-uz/README.md) |
| **90** | **Wav2Vec2-XLSR-UZ** | STT | End-to-end self-supervised acoustic CTC model fine-tuned for Uzbek speech | No | $0 (runs on CPU) | ✅ Yes | [README](stt/wav2vec2-large-xlsr-uz/README.md) |
| **91** | **WavLM-Large** | STT | Speech recognition with native background denoising and speaker verification | No | $0 (runs on CPU) | ✅ Yes | [README](stt/wavlm-large/README.md) |
| **92** | **Whisper-Base** | STT | Optimal balance of edge speed and acceptable transcription accuracy for bots | No | $0 (runs on existing server) | ✅ Yes | [README](stt/whisper-base/README.md) |
| **93** | **Whisper-Diarization** | STT | Multi-speaker meeting transcription with speaker identification ('Who Spoke When') | Optional | $0–$15 (CPU / GPU) | ✅ Yes | [README](stt/whisper-diarization/README.md) |
| **94** | **Whisper-Large-v3-Turbo** | STT | High-accuracy enterprise transcription at 8x speed (pruned 4-layer decoder) | Optional | $0–$15 (CPU / GPU) | ✅ Yes | [README](stt/whisper-large-v3-turbo/README.md) |
| **95** | **Whisper-Medium** | STT | Production-grade call-center analytics and complex multi-speaker transcription | Recommended | $15–$30 (entry GPU) | ⚠️ Dedicated recommended | [README](stt/whisper-medium/README.md) |
| **96** | **Whisper-Small-UZ** | STT | Domain-fine-tuned Uzbek speech recognition on Common Voice Uzbek corpus | No | $0 (runs on CPU) | ✅ Yes | [README](stt/whisper-small-uz/README.md) |
| **97** | **Whisper-Timestamped** | STT | Accurate word-level timestamping and subtitle synchronization without hallucinations | No | $0 (runs on CPU) | ✅ Yes | [README](stt/whisper-timestamped/README.md) |
| **98** | **Whisper-Tiny** | STT | Ultra-lightweight real-time transcription on low-end CPUs and IoT hardware | No | $0 (runs on $4 VPS) | ✅ Yes | [README](stt/whisper-tiny/README.md) |
| **99** | **Whisper.cpp** | STT | High-performance pure C/C++ ASR inference with zero Python runtime overhead | No | $0 (runs on bare-metal CPU) | ✅ Yes | [README](stt/whisper-cpp/README.md) |
| **100** | **Zipformer-Transducer** | STT | Next-gen Kaldi Zipformer multi-rate transducer with exceptional parameter efficiency | No | $0 (runs on CPU) | ✅ Yes | [README](stt/zipformer-transducer/README.md) |

*(100 of 100 models reviewed, scaffolded and verified — 100% COMPLETE)*

---

## Repo structure

```text
100-opensource-models-review/
├── README.md # this file — overall index
├── _template/ # template files and rules for adding a new model
├── cv/
│   ├── requirements.txt # unified master dependencies for all 27 CV models
│   ├── bytetrack-mot/
│   ├── depth-anything-v2-small/
│   ├── insightface-arcface/
│   ├── opencv-video-stream/
│   ├── yolo-object-detection/
│   ├── yolo-pose-sleeping/
│   ├── yolo11m/
│   ├── yolo11n/
│   ├── yolo11n-pose/
│   ├── yolo11n-seg/
│   ├── yolo11s/
│   ├── yolov10n/
│   ├── yolov10s/
│   ├── yolov3-tiny/
│   ├── yolov4-tiny/
│   ├── yolov5m/
│   ├── yolov5n/
│   ├── yolov5s/
│   ├── yolov6n/
│   ├── yolov6s/
│   ├── yolov7-tiny/
│   ├── yolov8m/
│   ├── yolov8n/
│   ├── yolov8s/
│   ├── yolov8s-worldv2/
│   ├── yolov9s/
│   ├── yolov9t/
├── llm/
│   ├── DeepSeek-Coder-V2-Lite-Instruct-GGUF/
│   ├── DeepSeek-R1-Distill-Llama-8B-GGUF/
│   ├── DeepSeek-R1-Distill-Qwen-1.5B-GGUF/
│   ├── Gemma-2-2B-Instruct-GGUF/
│   ├── Granite-3.0-2B-Instruct-GGUF/
│   ├── Hermes-3-Llama-3.2-3B-GGUF/
│   ├── Llama-3.1-8B-Instruct-GGUF/
│   ├── Llama-3.2-1B-Instruct-GGUF/
│   ├── Llama-Guard-3-1B-GGUF/
│   ├── Mistral-7B-Instruct-v0.3-GGUF/
│   ├── Moondream2-GGUF/
│   ├── NLLB-200-Distilled-600M/
│   ├── Phi-3.5-mini-instruct-GGUF/
│   ├── Qwen2-VL-2B-Instruct-GGUF/
│   ├── Qwen2.5-1.5B-Instruct-GGUF/
│   ├── Qwen2.5-3B-Instruct-GGUF/
│   ├── Qwen2.5-Coder-1.5B-Instruct-GGUF/
│   ├── SmolLM2-1.7B-Instruct-GGUF/
│   ├── StarCoder2-3B-GGUF/
│   ├── bge-m3/
│   ├── bge-reranker-v2-m3/
├── tts/
│   ├── bark-small/
│   ├── chattts/
│   ├── coqui-tts-vits/
│   ├── coqui-xtts-v2/
│   ├── cosyvoice-300m/
│   ├── e2-tts/
│   ├── espeak-ng/
│   ├── f5-tts/
│   ├── fastspeech2/
│   ├── fish-speech-1.5/
│   ├── glow-tts/
│   ├── matcha-tts/
│   ├── meta-voice-1b/
│   ├── mms-tts-kaz/
│   ├── mms-tts-uzb/
│   ├── mms-tts-uzb-latin/
│   ├── openvoice-v2/
│   ├── parler-tts-mini/
│   ├── piper-tts/
│   ├── seamless-m4t-tts/
│   ├── sherpa-onnx-offline-tts/
│   ├── speecht5-tts/
│   ├── styletts2/
│   ├── tacotron2/
│   ├── tortoise-tts/
│   ├── valle-x/
├── stt/
│   ├── FasterWhisper/
│   ├── conformer-ctc/
│   ├── data2vec-audio-large/
│   ├── funasr-paraformer/
│   ├── hubert-large-ls960/
│   ├── insanely-fast-whisper/
│   ├── mms-1b-all/
│   ├── moonshine-base/
│   ├── moonshine-tiny/
│   ├── nemo-canary-1b/
│   ├── seamless-m4t-stt/
│   ├── sensevoice-small/
│   ├── sherpa-onnx-offline-stt/
│   ├── silero-stt/
│   ├── vosk-api-uz/
│   ├── wav2vec2-large-xlsr-uz/
│   ├── wavlm-large/
│   ├── whisper-base/
│   ├── whisper-cpp/
│   ├── whisper-diarization/
│   ├── whisper-large-v3-turbo/
│   ├── whisper-medium/
│   ├── whisper-small-uz/
│   ├── whisper-timestamped/
│   ├── whisper-tiny/
│   ├── zipformer-transducer/
└── benchmark_scripts/ # shared benchmark scripts per category
```

## What's in each model's README

- Technical info about the model (architecture, parameters, versions)
- What was done in the project and what issues were encountered
- GPU compatibility and resource requirements (CPU-only or GPU-required)
- Estimated monthly cost if run in the cloud
- How to run it

## Running the models

Each model folder is self-contained — it has its own `Dockerfile`, `run_benchmarks.py`, and `README.md`.

- **CV models (27)**: Run directly in the dedicated, shared `cv/venv-cv` virtual environment (`pip install -r cv/requirements.txt`) with full local webcam (`--source 0`), GUI preview, or `--headless` batch processing.
- **LLM (21) / TTS (26) / STT (26) models**: Run through Docker (`docker compose up <model-name> --build`) or locally via Python.

Rules and template files for adding a new model — [`_template/HOW_TO_ADD_A_MODEL.md`](_template/HOW_TO_ADD_A_MODEL.md).
