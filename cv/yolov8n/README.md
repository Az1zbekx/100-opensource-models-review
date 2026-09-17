# Model Review 1/100: YOLOv8n (Real-Time Person Detection)

## 📋 Executive Summary (For PMs & Tech Leads)

| Metric | Assessment |
|---|---|
| **Primary Use Cases** | Security surveillance, foot-traffic counting, presence detection, safety monitoring. |
| **GPU Required?** | **No** — runs in real-time on a standard CPU. |
| **Cloud/Server Cost** | **$0 additional** (can run on existing application servers). |
| **Deployment Strategy** | ✅ Can be embedded directly into the main backend (monolithic) for a single camera. |
| **Scaling (5-10+ cameras)** | Requires separating the model into a standalone Microservice/API on a GPU-backed server. |

---

## 1. Model Overview

**YOLO (You Only Look Once)** is a family of end-to-end neural network architectures optimized for real-time object detection. Unlike classic two-stage detectors, YOLO processes the entire image in a single forward pass, predicting bounding boxes and class probabilities simultaneously. 

*   **Model Variant:** YOLOv8n (Nano)
*   **Developer:** Ultralytics
*   **Architecture:** Anchor-free detection head with a modified CSPNet backbone.
*   **Parameters:** ~3.2 Million (lightest in the v8 family).
*   **Weights Size:** ~6 MB
*   **Pre-trained On:** COCO Dataset (80 object classes).
*   **License:** AGPL-3.0 (Ultralytics).

---

## 2. Business Capabilities & Use Cases

While this specific implementation filters solely for the `person` class, the model natively supports multiple computer vision tasks:

*   **Multi-Object Tracking:** Detects 80 different classes out of the box (vehicles, animals, electronics, furniture).
*   **Custom Fine-Tuning:** Can be retrained on proprietary datasets (e.g., detecting factory safety helmets, defective products on a conveyor belt).
*   **Advanced Variants:** The YOLOv8 family also supports Instance Segmentation (`YOLOv8-seg`) and Pose Estimation (`YOLOv8-pose`) without changing the core deployment infrastructure.

---

## 3. Architecture & Deployment Strategies

When moving this model from a local environment to production, there are two primary deployment architectures depending on the project scale:

### A) Embedded in Project (Monolithic)
*   **Best for:** Low-traffic internal tools, single-camera monitoring, edge devices (IoT).
*   **How it works:** The YOLOv8 model is loaded directly inside the main application's process (e.g., inside a Django or FastAPI backend).
*   **Pros:** Zero network latency between the app and the model; cheapest to host.
*   **Cons:** Model inference blocks the main application thread; scaling the app means unnecessarily duplicating the model memory.

### B) Standalone API / Microservice (Recommended for Scale)
*   **Best for:** Multi-camera systems, public SaaS, enterprise production.
*   **How it works:** The main application has no AI code. The YOLOv8 model is wrapped in its own FastAPI service, containerized via Docker, and deployed on a separate GPU server. The main app sends images/frames via HTTP or WebSockets to this API.
*   **Pros:** Independent scaling (you can scale the AI API without touching the main backend); prevents backend crashes if the model runs out of memory.
*   **Optimization:** In this setup, raw `.pt` PyTorch weights should be exported to **ONNX** (CPU/universal) or **TensorRT** (NVIDIA GPU) formats for significantly faster inference.

---

## 4. Hardware Requirements & Cloud Costs

### Local / Edge Deployment (Current Implementation)
*   **Compute:** Modern CPU (No GPU required).
*   **RAM:** 2–4 GB.
*   **Disk:** < 50 MB total for model and core dependencies.

### Cloud Deployment (If scaling to a Standalone GPU Server)
YOLOv8n is extremely lightweight. If processing multiple high-resolution video streams in parallel, a dedicated GPU is required. Below are estimated monthly costs for running a standalone AI server 24/7 (based on RunPod pricing as of 2026):

| Server Configuration | Hourly Rate | Est. Monthly Cost (24/7) | Best For |
|---|---|---|---|
| **CPU Only (No GPU)** | ~$0.05 | ~$36 | 1-2 concurrent streams |
| **RTX 3050 / 4060** | ~$0.20 | ~$145 | 4-8 parallel streams |
| **RTX A5000 (24GB)** | ~$0.27 | ~$197 | Heavy traffic, multiple models |
| **RTX 3090 / 4090** | $0.46 - $0.69 | $336 - $504 | Fine-tuning / Heavy Inference |

> **Note:** For this specific single-camera implementation, cloud GPU costs are **$0**. A GPU is only necessary when actively retraining the model (fine-tuning) or handling a massive scale of video feeds.

---

## 5. Implementation Details & Limitations

This repository implements a lightweight **Presence Detection State Machine** using the laptop's webcam. 

*   **Logic:** Frames are processed in real-time. If a `person` is detected (`confidence > 0.5`), a bounding box is drawn.
*   **Debounce Mechanism:** To prevent UI "flickering" when a person is at the edge of the frame, the code requires `N` consecutive frames yielding the same result before officially changing the state from `PRESENT` to `ABSENT`.
*   **Observed Limitations:** 
    *   Struggles with distant objects and severe motion blur.
    *   Single-frame confidence can drop unexpectedly in poor lighting.

---

## 6. How to Run

There are two ways to spin up this project locally.

### Option A: Native Environment (With GUI / Video Output)
Recommended if you want to visually see the bounding boxes on your screen.

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the script
python demo.py
```
*(Press `q` in the video window to exit).*

### Option B: Docker (Headless Mode)
Recommended for server deployment testing. This runs the model without rendering a GUI window, outputting state changes (`Person entered`, `Person left`) directly to the console.

```bash
docker compose up --build
```
*(Note: X11 GUI forwarding is intentionally disabled in the Docker setup to ensure cross-platform compatibility across Linux, Mac, and Windows servers).*