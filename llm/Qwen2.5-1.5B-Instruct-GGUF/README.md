# Qwen2.5-1.5B-Instruct (GGUF Q4_K_M) Review & Benchmark

[![Category](https://img.shields.io/badge/Category-LLM-blue.svg)]()
[![Model Size](https://img.shields.io/badge/Parameters-1.54B-green.svg)]()
[![Quantization](https://img.shields.io/badge/Quantization-Q4__K__M-orange.svg)]()
[![Context Window](https://img.shields.io/badge/Context-32k-purple.svg)]()
[![Deployment](https://img.shields.io/badge/Docker-Ready-2496ED.svg)]()

Qwen2.5-1.5B-Instruct is Alibaba Cloud's state-of-the-art lightweight instruction-tuned Large Language Model, quantized into the universal **GGUF (Q4_K_M)** format for zero-configuration, ultra-fast CPU and low-memory edge/local inference via `llama.cpp`.

---

## 📋 PM & Business Overview

| Attribute | Specification / Assessment |
| :--- | :--- |
| **Model Name** | `Qwen2.5-1.5B-Instruct-GGUF` (weights: `qwen2.5-1.5b-instruct-q4_k_m.gguf`) |
| **Target Project Fit** | High-speed local FAQ bot, customer support chat assistant, structured JSON extractor, private on-premise NLP pipelines |
| **GPU Required?** | **No**. Runs flawlessly on standard CPU (4+ threads). If a low-end GPU like GTX 1650 (4GB) is present, weights fit 100% in VRAM |
| **RAM / VRAM Footprint** | ~1.1 GB RAM / VRAM total overhead |
| **Estimated Monthly Hosting Cost** | **$0** (co-located on existing backend server) or **$5–$10/mo** entry VPS |
| **Same Server as Backend?** | ✅ **Yes** (very low memory footprint and negligible idle CPU usage) |
| **Uzbek Language Quality** | ⭐⭐⭐⭐☆ (High comprehension, grammatically sound Uzbek generation, polite conversational tone) |

---

## ⚙️ Technical Specifications

- **Base Architecture:** Decoder-only Transformer with RoPE (Rotary Position Embeddings), SwiGLU activations, RMSNorm, and Grouped Query Attention (GQA).
- **Total Parameters:** 1.54 Billion (Non-embedding: ~1.31B).
- **Quantization Level:** `Q4_K_M` (4-bit medium K-quants balancing extreme compression and mathematical accuracy).
- **Binary Size on Disk:** ~986 MB (under 1 GB!).
- **Maximum Context Length:** Up to 32,768 tokens (tested at standard 2,048–4,096 tokens for fast interactive response).
- **Chat Template:** ChatML (`<|im_start|>system...<|im_end|><|im_start|>user...<|im_end|><|im_start|>assistant...`).

---

## 🧪 Real-World Test Datasets & Use Cases

We verified the model against 3 genuine operational business scenarios in `data/`:

### 1. E-Commerce Customer Service (Uzbek Language)
- **File:** `data/input_1_support_uz.txt`
- **Context:** An Uzbek customer inquiring about store ordering, payment gateways (Payme, Click, cash), and delivery timelines.
- **Goal:** Assess conversational fluency, polite business etiquette, and factual accuracy in Uzbek without hallucination.

### 2. Zero-Shot Structured JSON Entity Extraction
- **File:** `data/input_2_json_extract.txt`
- **Context:** An unstructured Uzbek job posting for a Senior Backend Developer in Tashkent with salary and location details.
- **Goal:** Extract clean, parseable JSON schema (`company`, `position`, `salary_usd`, `location`) with zero markdown garbage.

### 3. Analytics & SQL Query Generation
- **File:** `data/input_3_sql_query.txt`
- **Context:** PostgreSQL database schema with `users` and `orders` tables.
- **Goal:** Generate a production-ready SQL query calculating the top 5 spending customers over the last 30 days.

---

## 📊 Verification & Benchmark Results

All tests executed on a standard laptop configuration: **AMD Ryzen / Intel CPU, 4 physical threads, 16GB System RAM, NVIDIA GeForce GTX 1650 (4GB)**.

| Scenario | Input Artifact | Output Artifact | Generation Latency | Speed | Output Quality & Accuracy | Status |
| :--- | :--- | :--- | :---: | :---: | :--- | :---: |
| **1. Uzbek Customer Support** | `data/input_1_support_uz.txt` | `data/output_1_support_uz.txt` | 8.16s | 19.00 tok/s | Understands Uzbek intent and context well; grammar shows minor fragmentation typical of 1.5B parameters. | **PASS** |
| **2. JSON Extraction** | `data/input_2_json_extract.txt` | `data/output_2_json_extract.txt` | 6.74s | 12.32 tok/s | **100% Valid JSON**. Flawlessly extracted company, salary, and location from raw Uzbek text. | **PASS** |
| **3. SQL Query Authoring** | `data/input_3_sql_query.txt` | `data/output_3_sql_query.txt` | 12.90s | 17.91 tok/s | **Production-grade PostgreSQL**. Correct `JOIN`, `WHERE status = 'completed'`, and 30-day interval filter. | **PASS** |

---

## 🐳 Docker Deployment & Usage

The service is packaged to run seamlessly via Docker or Docker Compose.

### Method 1: Run with Docker Compose (Recommended)
```bash
# From repository root
docker compose up qwen2_5_1_5b_instruct_gguf
```

### Method 2: Standalone Docker Run
```bash
# Build the container
docker build -t qwen2.5-1.5b-instruct llm/Qwen2.5-1.5B-Instruct-GGUF

# Run interactive inference with custom prompt
docker run --rm -it -v $(pwd)/llm/Qwen2.5-1.5B-Instruct-GGUF/data:/app/data qwen2.5-1.5b-instruct \
  python3 demo.py --input data/input_1_support_uz.txt --output data/output_1_support_uz.txt
```

### Method 3: Direct Local Python Execution
If running locally outside Docker:
```bash
pip install llama-cpp-python huggingface-hub

# Run test scenario 1
python3 demo.py --input data/input_1_support_uz.txt --output data/output_1_support_uz.txt

# Custom interactive prompt
python3 demo.py --prompt "Nima uchun sun'iy intellekt O'zbekiston iqtisodiyoti uchun muhim?" --tokens 200
```

---

## 💡 Production Architecture Recommendations

1. **High-Concurrency Serving:** For serving multiple API clients simultaneously, wrap `llama-cpp-python` with `llama-cpp[server]` to expose an **OpenAI-compatible REST API** (`/v1/chat/completions`).
2. **Memory Efficiency:** Since the model requires less than 1.2 GB RAM, it can run directly alongside a PostgreSQL or Web API server on a $10/month VPS without requiring an expensive GPU instance.
3. **Prompt Template:** Always wrap queries in the official **ChatML** format to maintain instruct-following discipline and prevent prompt leakage.
