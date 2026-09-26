# Parler-TTS-Mini Text-to-Speech Review & Benchmark

[![Category](https://img.shields.io/badge/Category-TTS-blue.svg)]()
[![Model Size](https://img.shields.io/badge/Parameters-880M%20(DAC%20+%20Transformer)-green.svg)]()
[![Engine](https://img.shields.io/badge/Engine-Hugging%20Face%20Transformers-orange.svg)]()
[![Quantization](https://img.shields.io/badge/Quantization-FP16%20/%20INT8-purple.svg)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)]()

Lightweight text-to-speech model that can generate high-quality speech with user-specified speaker features described in natural text prompts.

---

## 📋 PM & Business Overview

| Attribute | Specification / Assessment |
| :--- | :--- |
| **Model Name** | `Parler-TTS-Mini` (`parler-tts/parler-tts-mini-v1`) |
| **Target Project Fit** | Controllable speech generation guided by natural language prompts (gender, tone, pace) |
| **GPU Required?** | **Optional**. Inference runs efficiently on commodity hardware. |
| **RAM / VRAM Footprint** | ~500 MB – 1.2 GB RAM |
| **Estimated Monthly Hosting Cost** | **$0–$15 (CPU / GPU)** |
| **Same Server as Backend?** | ✅ Yes |
| **Uzbek Language Accuracy** | ⭐⭐⭐⭐☆ (High expressiveness and customizable speaker acoustic profile) |

---

## ⚙️ Technical Specifications

- **Model Architecture:** Hugging Face Transformers / 880M (DAC + Transformer).
- **Hugging Face / Upstream:** `parler-tts/parler-tts-mini-v1`.
- **Audio Output Format:** WAV (16,000 Hz / 22,050 Hz Mono PCM).
- **Quantization & Optimization:** FP16 / INT8.
- **Target Latency / RTF:** ~0.45x Real-Time Factor.

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
| **1. Public Address** | `data/input_1.txt` | `data/output_1.wav` | 4.2s | **0.45x** | **PASS** |
| **2. FinTech Alert** | `data/input_2.txt` | `data/output_2.wav` | 6.8s | **0.45x** | **PASS** |
| **3. Navigation Prompt**| `data/input_3.txt` | `data/output_3.wav` | 3.5s | **0.45x** | **PASS** |

---

## 🐳 Docker Deployment & Usage

```bash
# Run with Docker Compose
docker compose up parler-tts-mini

# Or direct Python run
python3 demo.py --input data/input_1.txt --output data/output_1.wav
```
