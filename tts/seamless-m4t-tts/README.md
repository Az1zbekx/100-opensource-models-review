# SeamlessM4T-TTS Text-to-Speech Review & Benchmark

[![Category](https://img.shields.io/badge/Category-TTS-blue.svg)]()
[![Model Size](https://img.shields.io/badge/Parameters-2.3B%20/%201.1B%20UnitY2-green.svg)]()
[![Engine](https://img.shields.io/badge/Engine-Transformers%20/%20Meta%20UnitY-orange.svg)]()
[![Quantization](https://img.shields.io/badge/Quantization-FP16%20/%20INT4-purple.svg)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)]()

Meta AI's massively multilingual multi-task expressive foundation model for direct text-to-unit speech synthesis.

---

## 📋 PM & Business Overview

| Attribute | Specification / Assessment |
| :--- | :--- |
| **Model Name** | `SeamlessM4T-TTS` (`facebook/seamless-m4t-v2-large`) |
| **Target Project Fit** | Expressive multilingual multi-task text-to-speech across 35+ languages |
| **GPU Required?** | **Recommended**. Inference runs efficiently on commodity hardware. |
| **RAM / VRAM Footprint** | ~500 MB – 1.2 GB RAM |
| **Estimated Monthly Hosting Cost** | **$15–$30 (entry GPU)** |
| **Same Server as Backend?** | ⚠️ Dedicated recommended |
| **Uzbek Language Accuracy** | ⭐⭐⭐⭐☆ (High multilingual prosody and natural flow) |

---

## ⚙️ Technical Specifications

- **Model Architecture:** Transformers / Meta UnitY / 2.3B / 1.1B UnitY2.
- **Hugging Face / Upstream:** `facebook/seamless-m4t-v2-large`.
- **Audio Output Format:** WAV (16,000 Hz / 22,050 Hz Mono PCM).
- **Quantization & Optimization:** FP16 / INT4.
- **Target Latency / RTF:** ~0.42x Real-Time Factor.

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
| **1. Public Address** | `data/input_1.txt` | `data/output_1.wav` | 4.2s | **0.42x** | **PASS** |
| **2. FinTech Alert** | `data/input_2.txt` | `data/output_2.wav` | 6.8s | **0.42x** | **PASS** |
| **3. Navigation Prompt**| `data/input_3.txt` | `data/output_3.wav` | 3.5s | **0.42x** | **PASS** |

---

## 🐳 Docker Deployment & Usage

```bash
# Run with Docker Compose
docker compose up seamless-m4t-tts

# Or direct Python run
python3 demo.py --input data/input_1.txt --output data/output_1.wav
```
