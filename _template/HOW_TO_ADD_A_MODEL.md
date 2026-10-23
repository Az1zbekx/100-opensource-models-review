# How to Add a New Model

This document outlines the standard procedure for adding a new model to the  repository.

---

## 1. Directory Structure

Each model must be placed in its respective category directory (, , , or ).



---

## 2. Category Execution Model

- **CV Models ()**:
  - Run natively on the host using the shared virtual environment ().
  - Native host execution is required for low-latency camera access (), GUI rendering (), and local GPU acceleration without container pass-through overhead.
- **LLM, STT, and TTS Models (, , )**:
  - Run containerized via Docker and .
  - Must inherit from  or .

---

## 3. Required Files

### A. 
Every model README must follow this exact section structure:
1. **Model Overview & Architecture**: Parameters, license, context window, quantization format.
2. **Benchmark & Resource Usage**: Measured latency, throughput (FPS or tokens/sec), RAM and VRAM footprints on the test environment (NVIDIA GTX 1650 4GB VRAM / CPU).
3. **Production Deployment & Sizing**: Recommended cloud VM specs, monthly estimated cost, scale feasibility.
4. **Quickstart & Usage**: Exact terminal commands to run .

### B. 
- Self-contained and minimal.
- Supports both headless batch execution (for automated tests) and interactive mode.
- Downloads weights on demand to  or Hugging Face cache (never commit binary weights to Git).
- No verbose boilerplate comments.

### C. 
- Pins only packages strictly required on top of  or .

### D.  (for LLM, STT, TTS)


---

## 4. Verification Checklist

- [ ]  executes cleanly without unhandled exceptions.
- [ ] No binary weight files (, , , ) are committed to Git.
- [ ]  adheres to the 4-section standard.
- [ ] Model is registered in root  Model Index table.
- [ ] If LLM/TTS/STT: Docker service generated via .
