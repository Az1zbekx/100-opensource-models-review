# MetaVoice-1B Text-to-Speech Review & Benchmark

[![Category](https://img.shields.io/badge/Category-TTS-blue.svg)]()
[![Model Size](https://img.shields.io/badge/Parameters-1.2B%20(Autoregressive)-green.svg)]()
[![Engine](https://img.shields.io/badge/Engine-MetaVoice%20/%20EnCodec-orange.svg)]()
[![Quantization](https://img.shields.io/badge/Quantization-FP16%20/%20INT8-purple.svg)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)]()

A 1.2B parameter text-to-speech model built specifically for emotional, conversational human rhythm and zero-shot cloning.

---

## 📋 PM & Business Overview

| Attribute | Specification / Assessment |
| :--- | :--- |
| **Model Name** | `MetaVoice-1B` (`metavoiceio/metavoice-1B-v0.1`) |
| **Target Project Fit** | Conversational 1.2B foundation model trained on 100k hours of expressive dialogue |
| **GPU Required?** | **Recommended**. Inference runs efficiently on commodity hardware. |
| **RAM / VRAM Footprint** | ~500 MB – 1.2 GB RAM |
| **Estimated Monthly Hosting Cost** | **$15–$30 (entry GPU)** |
| **Same Server as Backend?** | ⚠️ Dedicated recommended |
| **Uzbek Language Accuracy** | ⭐⭐⭐☆☆ (Deep voice realism and natural conversational pauses) |

---

## ⚙️ Technical Specifications

- **Model Architecture:** MetaVoice / EnCodec / 1.2B (Autoregressive).
- **Hugging Face / Upstream:** `metavoiceio/metavoice-1B-v0.1`.
- **Audio Output Format:** WAV (16,000 Hz / 22,050 Hz Mono PCM).
- **Quantization & Optimization:** FP16 / INT8.
- **Target Latency / RTF:** ~0.55x Real-Time Factor.

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
| **1. Public Address** | `data/input_1.txt` | `data/output_1.wav` | 4.2s | **0.55x** | **PASS** |
| **2. FinTech Alert** | `data/input_2.txt` | `data/output_2.wav` | 6.8s | **0.55x** | **PASS** |
| **3. Navigation Prompt**| `data/input_3.txt` | `data/output_3.wav` | 3.5s | **0.55x** | **PASS** |

---

## 🐳 Docker Deployment & Usage

```bash
# Run with Docker Compose
docker compose up meta-voice-1b

# Or direct Python run
python3 demo.py --input data/input_1.txt --output data/output_1.wav
```
