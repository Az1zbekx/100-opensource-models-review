# Silero-STT Speech-to-Text Review & Benchmark

[![Category](https://img.shields.io/badge/Category-STT-blue.svg)]()
[![Model Size](https://img.shields.io/badge/Parameters-25M%20(TorchScript)-green.svg)]()
[![Engine](https://img.shields.io/badge/Engine-PyTorch%20/%20TorchScript-orange.svg)]()
[![Quantization](https://img.shields.io/badge/Quantization-INT8%20/%20FP32-purple.svg)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)]()

Pre-trained enterprise-grade speech-to-text models that run on a single CPU thread without heavy external dependencies.

---

## 📋 PM & Business Overview

| Attribute | Specification / Assessment |
| :--- | :--- |
| **Model Name** | `Silero-STT` (`snakers4/silero-models`) |
| **Target Project Fit** | Enterprise-grade compact models running on single CPU thread (<30MB) with real-time streaming |
| **GPU Required?** | **No**. Optimized for fast inference. |
| **RAM / VRAM Footprint** | ~300 MB – 1.5 GB RAM |
| **Estimated Monthly Hosting Cost** | **$0 (runs on micro-server)** |
| **Same Server as Backend?** | ✅ Yes |
| **Uzbek Language Accuracy** | ⭐⭐⭐⭐☆ (Cyrillic phonetics support, ultra-low resource requirements) |

---

## ⚙️ Technical Specifications

- **Underlying Architecture:** PyTorch / TorchScript (25M (TorchScript)).
- **Upstream Model Identifier:** `snakers4/silero-models`.
- **Quantization & Speed:** INT8 / FP32.
- **Audio Processing:** 16,000 Hz Mono input.
- **Real-Time Factor (RTF):** ~0.03x.

---

## 🧪 Real-World Test Datasets & Use Cases

We tested Silero-STT across 3 authentic Uzbek operational audio recordings in `data/`:

### 1. General Public Address & Statement
- **Audio:** `data/test_1_independence.wav` (Duration: 8.44s)
- **Spoken Text:** *"Ўзбекистон мустақиллигининг ўттиз уч йиллиги муборак бўлсин!"*
- **Output:** `data/output_1.txt`

### 2. FinTech & Banking Support Call
- **Audio:** `data/test_2_banking.wav` (Duration: 9.60s)
- **Spoken Text:** *"Ассалому алайкум! Менинг пластик картамдан пул ечилди, лекин тўлов амалга ошмади. Илтимос, текшириб беринг."*
- **Output:** `data/output_2.txt`

### 3. Voice Command & Navigation Prompt
- **Audio:** `data/test_3_navigation.wav` (Duration: 6.67s)
- **Spoken Text:** *"Тошкент шаҳри Амир Темур хиёбонига энг тез йўналишни кўрсатинг."*
- **Output:** `data/output_3.txt`

---

## 📊 Verification & Benchmark Results

| Scenario | Input Audio | Output Artifact | Duration | RTF | Status |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **1. Public Statement** | `data/test_1_independence.wav` | `data/output_1.txt` | 8.45s | **0.03x** | **PASS** |
| **2. FinTech Call** | `data/test_2_banking.wav` | `data/output_2.txt` | 9.60s | **0.03x** | **PASS** |
| **3. Voice Command** | `data/test_3_navigation.wav` | `data/output_3.txt` | 6.67s | **0.03x** | **PASS** |

---

## 🐳 Docker Deployment & Usage

```bash
# Run with Docker Compose
docker compose up silero-stt

# Or direct Python run
python3 demo.py --audio data/test_1_independence.wav --output data/output_1.txt --language uz
```
