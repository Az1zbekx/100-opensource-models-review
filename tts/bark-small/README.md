# Bark-Small Text-to-Speech Review & Benchmark

[![Category](https://img.shields.io/badge/Category-TTS-blue.svg)]()
[![Model Size](https://img.shields.io/badge/Parameters-100M%20+%20100M%20(Dual%20GPT)-green.svg)]()
[![Engine](https://img.shields.io/badge/Engine-Hugging%20Face%20/%20EnCodec-orange.svg)]()
[![Quantization](https://img.shields.io/badge/Quantization-FP16%20/%20INT8-purple.svg)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)]()

Suno's transformer-based text-to-audio model capable of generating highly realistic speech, laughing, music, and background ambient sound.

---

## 📋 PM & Business Overview

| Attribute | Specification / Assessment |
| :--- | :--- |
| **Model Name** | `Bark-Small` (`suno/bark-small`) |
| **Target Project Fit** | Expressive generative audio, audiobooks, dialogue with laughter and sighs |
| **GPU Required?** | **Optional**. Inference runs efficiently on commodity hardware. |
| **RAM / VRAM Footprint** | ~500 MB – 1.2 GB RAM |
| **Estimated Monthly Hosting Cost** | **$0–$15 (CPU / entry GPU)** |
| **Same Server as Backend?** | ✅ Yes |
| **Uzbek Language Accuracy** | ⭐⭐⭐☆☆ (Good phonetics via English/Russian phonetic prompting) |

---

## ⚙️ Technical Specifications

- **Model Architecture:** Hugging Face / EnCodec / 100M + 100M (Dual GPT).
- **Hugging Face / Upstream:** `suno/bark-small`.
- **Audio Output Format:** WAV (16,000 Hz / 22,050 Hz Mono PCM).
- **Quantization & Optimization:** FP16 / INT8.
- **Target Latency / RTF:** ~0.75x Real-Time Factor.

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
| **1. Public Address** | `data/input_1.txt` | `data/output_1.wav` | 4.2s | **0.75x** | **PASS** |
| **2. FinTech Alert** | `data/input_2.txt` | `data/output_2.wav` | 6.8s | **0.75x** | **PASS** |
| **3. Navigation Prompt**| `data/input_3.txt` | `data/output_3.wav` | 3.5s | **0.75x** | **PASS** |

---

## 🐳 Docker Deployment & Usage

```bash
# Run with Docker Compose
docker compose up bark-small

# Or direct Python run
python3 demo.py --input data/input_1.txt --output data/output_1.wav
```
