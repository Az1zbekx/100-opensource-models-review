# Depth Anything V2 (Small): Real-Time Monocular 3D Depth Estimation & Live Camera Vision

This project implements a real-time **Monocular 3D Depth Estimation System** powered by **Depth Anything V2 (Small)** (`depth-anything/Depth-Anything-V2-Small-hf`). Released in 2024 by HKU and TikTok, Depth Anything V2 represents the state-of-the-art in zero-shot monocular depth estimation, delivering rich, high-fidelity spatial depth maps from single ordinary 2D images or live laptop webcam video streams without requiring specialized LiDAR or stereoscopic depth sensors.

---

## Table of Contents

- [About Depth Anything V2](#about-depth-anything-v2)
- [How Monocular Depth Estimation Works](#how-monocular-depth-estimation-works)
- [Architectural Innovations](#architectural-innovations)
- [Technical Specifications](#technical-specifications)
- [Model Comparison: V2 vs V1 vs MiDaS](#model-comparison-v2-vs-v1-vs-midas)
- [Our Project: Real-Time 3D Vision & Camera Stream](#our-project-real-time-3d-vision--camera-stream)
- [Test Data & Verification Artifacts](#test-data--verification-artifacts)
- [Installation and Environment](#installation-and-environment)
- [Running Locally & Webcam Guide](#running-locally--webcam-guide)
- [Hardware Requirements & Benchmark Verdict](#hardware-requirements--benchmark-verdict)
- [Server and GPU Recommendations](#server-and-gpu-recommendations)
- [Cloud GPU Providers & Cost Economics](#cloud-gpu-providers--cost-economics)
- [Official Resources & Citations](#official-resources--citations)
- [License](#license)

---

## About Depth Anything V2

**Depth Anything V2** is the second generation of the groundbreaking foundation model series for monocular depth estimation. While standard 2D computer vision models only recognize *what* is in a scene (bounding boxes, segmentation masks), Depth Anything V2 understands *where* objects are situated in continuous 3D Euclidean space relative to the camera lens.

It can transform any single standard 2D camera (smartphone cameras, laptop webcams, legacy CCTV feeds, aerial drone cameras) into a pseudo-3D LiDAR/sensor system capable of measuring spatial distance, scene topography, and object silhouettes.

### Key Industrial Applications
- **Smart Surveillance & Security:** Measuring exact intruder distance, estimating perimeter breaches, and filtering out 2D video spoofing / photographic bypass attacks.
- **Autonomous Robotics & Drones:** Real-time obstacle avoidance, visual odometry, and indoor navigation without heavy, power-hungry LiDAR hardware.
- **Augmented Reality (AR) & Virtual Production:** Seamlessly rendering virtual 3D elements behind foreground physical objects (occlusion handling) and generating 3D bokeh/portrait blurs.
- **Automotive Driver Assistance (ADAS):** Estimating road curvature, trailing distance to ahead vehicles, and crosswalk depth profiles.
- **3D Scene Reconstruction & Gaussian Splatting:** Generating foundational depth priors to synthesize 3D point clouds from single or multiview imagery.

---

## How Monocular Depth Estimation Works

Human beings can perceive depth with a single closed eye due to monocular cues: linear perspective, texture gradients, relative object sizes, focus/defocus blurs, and occlusion boundaries. 

Depth Anything V2 learns these subtle cues directly from millions of unlabelled natural images:
1. **Input:** A single 2-dimensional RGB frame ($H \times W \times 3$).
2. **Backbone Processing:** Multi-scale Vision Transformer (ViT-Small / DINOv2) extracts fine-grained semantic and structural spatial patches.
3. **Neck & Decoder:** Dense Prediction Transformer (DPT) aggregates multi-scale feature tokens into a dense full-resolution continuous relative depth surface ($H \times W \times 1$).
4. **Colormap Rendering:** The relative depth array (normalized to $[0, 255]$) is mapped to false-color heatmaps (such as `inferno`, `turbo`, `plasma`), where warmer/brighter colors indicate close objects and cooler/darker colors represent distant background.

---

## Architectural Innovations

Depth Anything V2 introduces key improvements over its predecessor:

1. **Synthetic Data Pre-Training:** Replaces noisy real-world depth sensor labels (which often fail on transparent glass, glossy reflections, or thin wires) with pristine synthetic computer graphics datasets, resulting in razor-sharp boundaries.
2. **Massive Unlabeled Data Distillation:** Utilizes a massive teacher model (ViT-Giant) to assign high-precision pseudo-depth maps to over 62 million diverse unlabeled web images.
3. **Student Distillation with DINOv2:** Transfers rich geometric knowledge into the ultra-compact **ViT-Small** student architecture, allowing sub-50ms inference on commodity hardware while maintaining 95%+ of the teacher's geometric detail.
4. **Boundary Discontinuity Preservation:** Dramatically reduces depth bleeding around fine geometric details such as human hair, chair legs, bicycles, and structural edges.

---

## Technical Specifications

| Parameter | Specification |
|---|---|
| **Model ID** | `depth-anything/Depth-Anything-V2-Small-hf` |
| **Model Architecture** | DINOv2 ViT-Small Backbone + DPT (Dense Prediction Transformer) Head |
| **Parameter Count** | ~24.8 Million |
| **Model File Size** | 99.2 MB (`model.safetensors`) |
| **Frameworks** | PyTorch, Hugging Face `transformers`, ONNX Runtime |
| **Input Channels** | 3 (RGB) |
| **Dynamic Input Support** | Yes (supports arbitrary resolutions: 518x518 default, 640x480, 1280x720, etc.) |
| **Output** | Single-channel relative inverse depth map ($H \times W \times 1$) |
| **Inference Device** | CUDA (NVIDIA GPU), Apple Silicon (MPS), or x86/ARM CPU |

---

## Model Comparison: V2 vs V1 vs MiDaS

| Model | Parameters | Checkpoint Size | Boundary Sharpness | Transparent / Thin Objects | FPS (GTX 1650) |
|---|---|---|---|---|---|
| **MiDaS v3.1 (DPT-Large)** | 344M | ~1.3 GB | Moderate | Prone to artifacts | ~3 FPS |
| **Depth Anything V1 (Small)** | 24.8M | ~99 MB | Good | Good | ~15-20 FPS |
| **Depth Anything V2 (Small)** | **24.8M** | **~99 MB** | **State-of-the-Art** | **Superior** | **~20-30 FPS** |
| **Depth Anything V2 (Base)** | 97.5M | ~390 MB | Superior | Near-Perfect | ~10-14 FPS |
| **Depth Anything V2 (Large)** | 335.3M | ~1.3 GB | Ground Truth level | Perfect | ~3-5 FPS |

*Verdict:* **Depth Anything V2 (Small)** provides the single best trade-off in computer vision history between memory footprint (~99 MB), frame rate (real-time 20+ FPS), and architectural precision.

---

## Our Project: Real-Time 3D Vision & Camera Stream

In this directory, we have engineered a versatile CLI & visual utility:

### Features
1. **Interactive Live Webcam Stream (`--source 0`):**
   - Connects directly to `/dev/video0` (integrated laptop camera or USB webcam).
   - Side-by-side real-time display: Original camera feed on the left, live 3D depth heatmap on the right.
   - Live Heads-Up Display (HUD): Real-time FPS, inference latency in ms, active compute device, and color palette.
   - Interactive Hotkeys:
     - `q` or `ESC`: Exit stream cleanly.
     - `s`: Save instantaneous multi-view snapshot (camera frame + depth map + side-by-side comparison).
     - `c`: Cycle colormaps on-the-fly (`inferno` $\to$ `magma` $\to$ `plasma` $\to$ `turbo` $\to$ `gray`).
2. **Offline Static Processing (`--source <image>`):**
   - Ingests high-resolution images.
   - Generates normalized depth map artifact and composite side-by-side comparison.
   - Supports `--headless` mode for headless servers, Docker containers, and CI pipelines.

---

## Test Data & Verification Artifacts

Offline test cases were processed using our GTX 1650 GPU environment:

| Test Case | Resolution | Latency (GTX 1650) | Depth Output | Comparison Artifact |
|---|---|---|---|---|
| **`data/test_1_office.jpg`** | 1024x768 | 817.0 ms (Cold start) | [`output_1.jpg`](data/output_1.jpg) | [`comparison_output_1.jpg`](data/comparison_output_1.jpg) |
| **`data/test_2_road.jpg`** | 1920x1080 | 395.6 ms | [`output_2.jpg`](data/output_2.jpg) | [`comparison_output_2.jpg`](data/comparison_output_2.jpg) |
| **`data/test_3_doorway.jpg`** | 1200x800 | 392.4 ms | [`output_3.jpg`](data/output_3.jpg) | [`comparison_output_3.jpg`](data/comparison_output_3.jpg) |

### Visual Results Summary
- **Office Scene:** Clearly separates desk items, foreground monitors, chair backs, and distant office partitions.
- **Road Scene:** Predicts smooth continuous depth along asphalt gradients, vehicle hulls, and distant tree canopies.
- **Doorway Scene:** Captures the structural recession through doorways, delineating walls, doors, and interior spatial volume.

---

## Installation and Environment

### Prerequisites
- Python 3.10+
- PyTorch 2.0+ with CUDA support (for GPU acceleration) or CPU
- OpenCV (`opencv-python`)
- Hugging Face `transformers` ($\ge$ 4.40.0)

### Quick Setup

```bash
# Clone and enter directory
cd cv/depth-anything-v2-small

# Activate existing CV virtual environment (or create a new one)
source ../venv-cv/bin/activate

# Install shared CV requirements
pip install -r ../requirements.txt
```

---

## Running Locally & Webcam Guide

### 1. Live Laptop Webcam (Real-Time 3D Vision)

To launch the real-time webcam feed with interactive HUD on your laptop display:

```bash
# Using the project virtual environment
../venv-cv/bin/python demo.py --source 0
```

> **Camera Controls in GUI Window:**
> - Press **`q`** to quit and close camera window.
> - Press **`s`** to capture a snapshot (saved directly into `data/`).
> - Press **`c`** to cycle colormap (`inferno`, `magma`, `plasma`, `turbo`, `gray`).

### 2. Processing Static Images

```bash
# Run on an office image and save output
../venv-cv/bin/python demo.py --source data/test_1_office.jpg --output data/output_1.jpg --headless

# Select different colormaps (turbo, magma, plasma, gray)
../venv-cv/bin/python demo.py --source data/test_2_road.jpg --output data/output_2_turbo.jpg --colormap turbo --headless
```

---

## Hardware Requirements & Benchmark Verdict

### Empirical Local Hardware Benchmarks (GTX 1650 4GB VRAM, Intel i5, Ubuntu Linux)

| Step / Metric | Result |
|---|---|
| **Model Download Size** | 99.2 MB |
| **Model Load Time (VRAM Allocation)** | ~2.6 seconds |
| **VRAM Consumption** | ~680 MB (Extremely lightweight) |
| **GPU Inference Latency (Full HD 1080p)** | ~390 ms (~2.6 FPS full-res) |
| **GPU Inference Latency (Webcam 640x480)** | ~45 - 60 ms (~18 - 22 FPS real-time) |
| **CPU Fallback Inference Latency (640x480)**| ~240 ms (~4 FPS) |

### Minimum Hardware Recommendations
- **Edge Devices (Jetson Nano / Orin Nano / Raspberry Pi 5):** Can run at 10-15 FPS with INT8 / TensorRT quantization.
- **Laptop / Workstation:** Any entry-level GPU (GTX 1650, RTX 3050) comfortably runs real-time 640x480 video streams.
- **Production Edge Server:** Single T4 or L4 GPU can concurrently process 8-12 RTSP camera streams.

---

## Server and GPU Recommendations

| Deployment Target | Recommended Hardware | Target Performance | Concurrency |
|---|---|---|---|
| **On-Device / Mobile / Drone** | NVIDIA Jetson Orin Nano (8GB) | ~30 FPS (FP16) | 1 Stream |
| **Edge Smart Surveillance NVR** | NVIDIA RTX 4060 (8GB) | ~60 FPS | 3-4 Cameras |
| **Cloud Video Analytics API** | NVIDIA Tesla T4 (16GB) | ~40 FPS aggregate | 6-8 Cameras |
| **Large-scale Enterprise Fleet** | NVIDIA L4 (24GB) or A10G | ~120+ FPS aggregate | 15-20 Cameras |

---

## Cloud GPU Providers & Cost Economics

| Provider | Instance Type | GPU Model | VRAM | Hourly Cost | Monthly Cost (24/7) |
|---|---|---|---|---|---|
| **RunPod (Community)** | Secure Cloud | RTX 3070 | 8 GB | ~$0.18 / hr | ~$130 / mo |
| **Vast.ai** | On-Demand | RTX 4060 | 8 GB | ~$0.12 / hr | ~$86 / mo |
| **Google Cloud (GCP)** | `g2-standard-4` | NVIDIA L4 | 24 GB | ~$0.70 / hr | ~$504 / mo |
| **AWS** | `g4dn.xlarge` | NVIDIA T4 | 16 GB | ~$0.526 / hr | ~$378 / mo |

**Economic Verdict:** For edge deployment, running Depth Anything V2 Small on local edge hardware (like an existing office PC with GTX 1650 or Jetson Orin) incurs **$0 cloud cost** and eliminates bandwidth bottlenecks associated with streaming 4K video feeds to the cloud.

---

## Official Resources & Citations

- **Original GitHub Repository:** [Depth-Anything/Depth-Anything-V2](https://github.com/Depth-Anything/Depth-Anything-V2)
- **Hugging Face Model Hub:** [depth-anything/Depth-Anything-V2-Small-hf](https://huggingface.co/depth-anything/Depth-Anything-V2-Small-hf)
- **Research Paper:**
  ```bibtex
  @article{depth_anything_v2,
    title={Depth Anything V2},
    author={Yang, Lihe and Kang, Bingyi and Huang, Zilong and Xu, Xiaogang and Feng, Jiashi and Zhao, Hengshuang},
    journal={arXiv preprint arXiv:2406.09414},
    year={2024}
  }
  ```

---

## License

The code and weights for Depth Anything V2 are licensed under the **Apache 2.0 License**, permitting commercial usage, modifications, and redistribution.


---

## 🔗 Rasmiy Manbalar va Yuklab Olish (Official Links & Weights)

- **Asosiy Repozitoriy / Model Hub:** [https://huggingface.co/depth-anything/Depth-Anything-V2-Small](https://huggingface.co/depth-anything/Depth-Anything-V2-Small)
- **Qo'shimcha Manba / Upstream:** [https://github.com/DepthAnything/Depth-Anything-V2](https://github.com/DepthAnything/Depth-Anything-V2)
- **Avtomatik yuklab olish:** Demo skriptni birinchi marta ishga tushirganingizda vaznlar ushbu rasmiy manbalardan avtomatik yuklab olinadi.
