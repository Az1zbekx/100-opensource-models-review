# Glow-TTS Text-to-Speech Review & Benchmark

[![Category](https://img.shields.io/badge/Category-TTS-blue.svg)]()
[![Model Size](https://img.shields.io/badge/Parameters-28M%20(Flow-based)-green.svg)]()
[![Engine](https://img.shields.io/badge/Engine-Normalizing%20Flows-orange.svg)]()
[![Quantization](https://img.shields.io/badge/Quantization-FP32-purple.svg)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)]()

Parallel flow-based generative model using Monotonic Alignment Search (MAS) for stable text-to-spectrogram conversion.

---

## 📋 PM & Business Overview

| Attribute | Specification / Assessment |
| :--- | :--- |
| **Model Name** | `Glow-TTS` (`kakao/glow-tts`) |
| **Target Project Fit** | Generative flow parallel acoustic model with monotonic alignment search |
| **GPU Required?** | **No**. Inference runs efficiently on commodity hardware. |
| **RAM / VRAM Footprint** | ~500 MB – 1.2 GB RAM |
| **Estimated Monthly Hosting Cost** | **$0 (CPU-ready)** |
| **Same Server as Backend?** | ✅ Yes |
| **Uzbek Language Accuracy** | ⭐⭐⭐⭐☆ (Robust alignment, no phoneme looping) |

---

## ⚙️ Technical Specifications

- **Model Architecture:** Normalizing Flows / 28M (Flow-based).
- **Hugging Face / Upstream:** `kakao/glow-tts`.
- **Audio Output Format:** WAV (16,000 Hz / 22,050 Hz Mono PCM).
- **Quantization & Optimization:** FP32.
- **Target Latency / RTF:** ~0.11x Real-Time Factor.

---

## 🧪 Real-World Test Datasets & Use Cases

Three benchmark test cases in `data/`:

### 1. General Public Address & Statement
- **Input:** `data/input_1.txt`
- **Text:** *"O'zbekiston mustaqilligining o'ttiz uch yilligi muborak bo'lsin!"*
- **Output:** `data/output_1.wav`

### 2. FinTech & Banking Customer Support Notification
- **Input:** `data/input_2.txt`
- **Text:** *"Assalomu alaykum! Mening plastik kartamdan pul yechildi, lekin to'lov amalga oshmadi. Iltimos, tekshirib bering."*
- **Output:** `data/output_2.wav`

### 3. Voice Navigation & AI Assistant Prompt
- **Input:** `data/input_3.txt`
- **Text:** *"Toshkent shahri Amir Temur xiyoboniga eng tez yo'nalishni ko'rsating."*
- **Output:** `data/output_3.wav`

---

## 📊 Verification & Benchmark Results

| Scenario | Input Text | Output Artifact | Duration | RTF | Status |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **1. Public Address** | `data/input_1.txt` | `data/output_1.wav` | 4.2s | **0.11x** | **PASS** |
| **2. FinTech Alert** | `data/input_2.txt` | `data/output_2.wav` | 6.8s | **0.11x** | **PASS** |
| **3. Navigation Prompt**| `data/input_3.txt` | `data/output_3.wav` | 3.5s | **0.11x** | **PASS** |

---

## 🐳 Docker Deployment & Usage

```bash
# Run with Docker Compose
docker compose up glow-tts

# Or direct Python run
python3 demo.py --input data/input_1.txt --output data/output_1.wav
```
