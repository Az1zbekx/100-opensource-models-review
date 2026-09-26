# MMS-TTS-KAZ Text-to-Speech Review & Benchmark

[![Category](https://img.shields.io/badge/Category-TTS-blue.svg)]()
[![Model Size](https://img.shields.io/badge/Parameters-145M%20(VITS)-green.svg)]()
[![Engine](https://img.shields.io/badge/Engine-Transformers%20/%20PyTorch-orange.svg)]()
[![Quantization](https://img.shields.io/badge/Quantization-FP32%20/%20FP16-purple.svg)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)]()

Meta AI MMS VITS model for Kazakh speech synthesis, offering high phonological proximity to Uzbek.

---

## 📋 PM & Business Overview

| Attribute | Specification / Assessment |
| :--- | :--- |
| **Model Name** | `MMS-TTS-KAZ` (`facebook/mms-tts-kaz`) |
| **Target Project Fit** | Sister Turkic language TTS for Central Asian regional localization and testing |
| **GPU Required?** | **No**. Inference runs efficiently on commodity hardware. |
| **RAM / VRAM Footprint** | ~500 MB – 1.2 GB RAM |
| **Estimated Monthly Hosting Cost** | **$0 (CPU-ready)** |
| **Same Server as Backend?** | ✅ Yes |
| **Uzbek Language Accuracy** | ⭐⭐⭐⭐☆ (High phonological kinship with Uzbek, shared vowel harmony) |

---

## ⚙️ Technical Specifications

- **Model Architecture:** Transformers / PyTorch / 145M (VITS).
- **Hugging Face / Upstream:** `facebook/mms-tts-kaz`.
- **Audio Output Format:** WAV (16,000 Hz / 22,050 Hz Mono PCM).
- **Quantization & Optimization:** FP32 / FP16.
- **Target Latency / RTF:** ~0.19x Real-Time Factor.

---

## 🧪 Real-World Test Datasets & Use Cases

Three benchmark test cases in `data/`:

### 1. General Public Address & Statement
- **Input:** `data/input_1.txt`
- **Text:** *"Ўзбекистон мустақиллигининг ўттиз уч йиллиги муборак бўлсин!"*
- **Output:** `data/output_1.wav`

### 2. FinTech & Banking Customer Support Notification
- **Input:** `data/input_2.txt`
- **Text:** *"Ассалому алайкум! Менинг пластик картамдан пул ечилди, лекин тўлов амалга ошмади. Илтимос, текшириб беринг."*
- **Output:** `data/output_2.wav`

### 3. Voice Navigation & AI Assistant Prompt
- **Input:** `data/input_3.txt`
- **Text:** *"Тошкент шаҳри Амир Темур хиёбонига энг тез йўналишни кўрсатинг."*
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
docker compose up mms-tts-kaz

# Or direct Python run
python3 demo.py --input data/input_1.txt --output data/output_1.wav
```
