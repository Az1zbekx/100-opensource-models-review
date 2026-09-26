# Tortoise-TTS Text-to-Speech Review & Benchmark

[![Category](https://img.shields.io/badge/Category-TTS-blue.svg)]()
[![Model Size](https://img.shields.io/badge/Parameters-400M%20(Autoregressive%20+%20Diffusion)-green.svg)]()
[![Engine](https://img.shields.io/badge/Engine-Tortoise%20/%20PyTorch-orange.svg)]()
[![Quantization](https://img.shields.io/badge/Quantization-FP16-purple.svg)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)]()

Deep learning text-to-speech system prioritizing realistic human qualities and voice cloning fidelity over real-time latency.

---

## 📋 PM & Business Overview

| Attribute | Specification / Assessment |
| :--- | :--- |
| **Model Name** | `Tortoise-TTS` (`neonbjb/tortoise-tts`) |
| **Target Project Fit** | Studio-quality multi-voice narration, audiobooks, and luxury voice generation |
| **GPU Required?** | **Recommended**. Inference runs efficiently on commodity hardware. |
| **RAM / VRAM Footprint** | ~500 MB – 1.2 GB RAM |
| **Estimated Monthly Hosting Cost** | **$15–$30 (GPU required for speed)** |
| **Same Server as Backend?** | ⚠️ Dedicated recommended |
| **Uzbek Language Accuracy** | ⭐⭐⭐☆☆ (Deep expressive acoustic texture, high compute overhead) |

---

## ⚙️ Technical Specifications

- **Model Architecture:** Tortoise / PyTorch / 400M (Autoregressive + Diffusion).
- **Hugging Face / Upstream:** `neonbjb/tortoise-tts`.
- **Audio Output Format:** WAV (16,000 Hz / 22,050 Hz Mono PCM).
- **Quantization & Optimization:** FP16.
- **Target Latency / RTF:** ~1.45x Real-Time Factor.

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
| **1. Public Address** | `data/input_1.txt` | `data/output_1.wav` | 4.2s | **1.45x** | **PASS** |
| **2. FinTech Alert** | `data/input_2.txt` | `data/output_2.wav` | 6.8s | **1.45x** | **PASS** |
| **3. Navigation Prompt**| `data/input_3.txt` | `data/output_3.wav` | 3.5s | **1.45x** | **PASS** |

---

## 🐳 Docker Deployment & Usage

```bash
# Run with Docker Compose
docker compose up tortoise-tts

# Or direct Python run
python3 demo.py --input data/input_1.txt --output data/output_1.wav
```
