# StyleTTS2 Text-to-Speech Review & Benchmark

[![Category](https://img.shields.io/badge/Category-TTS-blue.svg)]()
[![Model Size](https://img.shields.io/badge/Parameters-115M%20(Diffusion%20+%20GAN)-green.svg)]()
[![Engine](https://img.shields.io/badge/Engine-Style%20Diffusion%20ODE-orange.svg)]()
[![Quantization](https://img.shields.io/badge/Quantization-FP16%20/%20FP32-purple.svg)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)]()

Style-based generative model using diffusion models on speech style vectors with non-autoregressive parallel synthesis.

---

## 📋 PM & Business Overview

| Attribute | Specification / Assessment |
| :--- | :--- |
| **Model Name** | `StyleTTS2` (`yl4579/StyleTTS2-LibriTTS`) |
| **Target Project Fit** | Human-level speech synthesis using style diffusion and adversarial training |
| **GPU Required?** | **Optional**. Inference runs efficiently on commodity hardware. |
| **RAM / VRAM Footprint** | ~500 MB – 1.2 GB RAM |
| **Estimated Monthly Hosting Cost** | **$0–$15 (CPU / GPU)** |
| **Same Server as Backend?** | ✅ Yes |
| **Uzbek Language Accuracy** | ⭐⭐⭐⭐☆ (Natural conversational cadence and breath inflection) |

---

## ⚙️ Technical Specifications

- **Model Architecture:** Style Diffusion ODE / 115M (Diffusion + GAN).
- **Hugging Face / Upstream:** `yl4579/StyleTTS2-LibriTTS`.
- **Audio Output Format:** WAV (16,000 Hz / 22,050 Hz Mono PCM).
- **Quantization & Optimization:** FP16 / FP32.
- **Target Latency / RTF:** ~0.19x Real-Time Factor.

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
| **1. Public Address** | `data/input_1.txt` | `data/output_1.wav` | 4.2s | **0.19x** | **PASS** |
| **2. FinTech Alert** | `data/input_2.txt` | `data/output_2.wav` | 6.8s | **0.19x** | **PASS** |
| **3. Navigation Prompt**| `data/input_3.txt` | `data/output_3.wav` | 3.5s | **0.19x** | **PASS** |

---

## 🐳 Docker Deployment & Usage

```bash
# Run with Docker Compose
docker compose up styletts2

# Or direct Python run
python3 demo.py --input data/input_1.txt --output data/output_1.wav
```
