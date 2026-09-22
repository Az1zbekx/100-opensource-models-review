# YOLOv8n Object Detection Model

This project uses **YOLOv8n**, a lightweight object-detection model from Ultralytics. YOLOv8n is designed for fast object detection in images, videos, and live camera streams while requiring relatively low computational resources.

---

## Table of Contents

- [About YOLOv8n](#about-yolov8n)
- [Supported Tasks](#supported-tasks)
- [Model Capabilities](#model-capabilities)
- [Dataset Information](#dataset-information)
- [Technical Specifications](#technical-specifications)
- [Model Comparison](#model-comparison)
- [Installation](#installation)
- [Running Locally](#running-locally)
- [Hardware Requirements](#hardware-requirements)
- [Server and GPU Recommendations](#server-and-gpu-recommendations)
- [Cloud GPU Providers](#cloud-gpu-providers)
- [Cost Considerations](#cost-considerations)
- [Model Export and Optimization](#model-export-and-optimization)
- [Official Resources](#official-resources)
- [License](#license)

---

## About YOLOv8n

YOLOv8n is the **nano** variant of the YOLOv8 (`You Only Look Once`) family of computer vision models developed by Ultralytics.

YOLO models are designed to detect objects in images, videos, and live camera streams. During a single inference process, the model can:

- Detect where an object is located
- Identify the object class or category
- Return a confidence score for each detected object
- Return bounding-box coordinates for every detection

YOLOv8n is lightweight, fast, and resource-efficient. It is suitable for:

- Real-time camera monitoring
- Image and video analysis
- Security-camera object detection
- Person and vehicle detection
- Smart-city and traffic monitoring
- Warehouse and manufacturing monitoring
- Retail and store analytics
- Edge-device inference
- MVPs, demos, and prototypes
- Object detection on PCs or servers with limited resources

---

## Supported Tasks

The YOLOv8 family supports multiple computer-vision tasks.

| Task | Description | Model Example |
|---|---|---|
| Object Detection | Detects objects, identifies their classes, and returns bounding boxes | `yolov8n.pt` |
| Image Classification | Identifies which category or class an image belongs to | `yolov8n-cls.pt` |
| Instance Segmentation | Separates objects at pixel level and generates masks | `yolov8n-seg.pt` |
| Pose Estimation | Detects human-body keypoints | `yolov8n-pose.pt` |
| Object Tracking | Tracks objects across video frames and assigns IDs | YOLOv8 + tracker |
| Oriented Bounding Boxes | Detects rotated objects using angled bounding boxes | `yolov8n-obb.pt` |

The primary model used for object detection is:

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
```

`yolov8n.pt` is a pretrained YOLOv8 nano model for object-detection tasks.

---

## Model Capabilities

### Object Detection

Object detection is the task of finding objects inside an image or video.

The standard YOLOv8n model can detect common objects such as:

- Person (`person`)
- Car (`car`)
- Motorcycle (`motorcycle`)
- Bus (`bus`)
- Truck (`truck`)
- Bicycle (`bicycle`)
- Dog, cat, horse, cow, sheep, elephant, and other animals
- Mobile phone (`cell phone`)
- Laptop (`laptop`)
- Television (`tv`)
- Chair (`chair`)
- Book (`book`)
- Clock (`clock`)
- Backpack, handbag, and suitcase
- Sports equipment
- Food items
- Other daily objects included in the COCO dataset

Example prediction result:

```json
{
  "class_name": "person",
  "confidence": 0.93,
  "bbox": {
    "x1": 110,
    "y1": 80,
    "x2": 420,
    "y2": 630
  }
}
```

Where:

| Field | Description |
|---|---|
| `class_name` | Name of the detected object class |
| `confidence` | Model confidence score between 0 and 1 |
| `bbox` | Bounding-box coordinates of the detected object |
| `x1`, `y1` | Top-left corner of the bounding box |
| `x2`, `y2` | Bottom-right corner of the bounding box |

### Limitations

The standard `yolov8n.pt` model recognizes the classes included in the dataset on which it was pretrained.

If an object is not present in the COCO dataset, the standard model may not detect it correctly. Examples include:

- Custom factory components
- Local product types
- Company logos
- Specialized documents
- Medical-image objects
- Specialized construction equipment
- Safety helmets or specific uniforms
- License plates
- Product defects
- Custom machinery parts

For specialized object-detection tasks, a custom dataset should be created and the YOLOv8n model should be fine-tuned.

---

## Dataset Information

### COCO 2017 Dataset

The default `yolov8n.pt` model is pretrained on the **COCO 2017** dataset.

COCO stands for **Common Objects in Context**. It is one of the most widely used open datasets for computer vision, object detection, segmentation, keypoint detection, and image captioning.

| Metric | Information |
|---|---:|
| Dataset name | COCO 2017 |
| Full name | Common Objects in Context |
| Main tasks | Object Detection, Segmentation, Keypoints, Captioning |
| Object classes | 80 |
| Train2017 images | 118,287 |
| Val2017 images | 5,000 |
| Test2017 images | More than 40,000 |
| Total images | More than 200,000 |
| Annotation types | Bounding boxes, segmentation masks, keypoints |

The COCO dataset includes 80 categories. Some examples are:

```text
person, bicycle, car, motorcycle, airplane,
bus, train, truck, boat, traffic light,
fire hydrant, stop sign, dog, cat, horse,
sheep, cow, elephant, bear, zebra, giraffe,
backpack, umbrella, handbag, tie, suitcase,
frisbee, skis, snowboard, sports ball,
kite, baseball bat, skateboard, surfboard,
bottle, cup, fork, knife, spoon, bowl,
banana, apple, sandwich, orange, broccoli,
carrot, hot dog, pizza, donut, cake,
chair, couch, bed, dining table, toilet,
tv, laptop, mouse, keyboard, cell phone,
microwave, oven, toaster, refrigerator,
book, clock, vase, scissors, teddy bear,
hair drier, toothbrush
```

---

## Technical Specifications

### YOLOv8n Specifications

| Metric | YOLOv8n |
|---|---:|
| Model type | Object Detection |
| Variant | Nano (`n`) |
| Standard input resolution | 640 × 640 px |
| Number of parameters | Approximately 3.2 million |
| Computational complexity | Approximately 8.7 GFLOPs |
| COCO `mAP50-95` | 37.3 |
| COCO `mAP50` | 52.8 |
| Main strength | Fast, lightweight, resource-efficient |
| Main use case | Real-time and edge inference |
| Model file | `yolov8n.pt` |
| Pretraining dataset | COCO 2017 |
| Framework | PyTorch / Ultralytics |
| Detection architecture | Anchor-free object detector |

`mAP50-95` is a common object-detection metric that measures the overall quality of a model. A higher value usually indicates better object-detection accuracy.

YOLOv8n is optimized for speed and low resource usage. However, its accuracy may be lower than larger YOLOv8 models.

---

## Model Comparison

| Model | Parameters | FLOPs | COCO mAP50-95 | Recommended Use Case |
|---|---:|---:|---:|---|
| YOLOv8n | 3.2M | 8.7B | 37.3 | Fast inference, edge devices, demos |
| YOLOv8s | 11.2M | 28.6B | 44.9 | Small and medium-sized projects |
| YOLOv8m | 25.9M | 78.9B | 50.2 | Projects requiring higher accuracy |
| YOLOv8l | 43.7M | 165.2B | 52.9 | Larger GPU and production workloads |
| YOLOv8x | 68.2M | 257.8B | 53.9 | Maximum accuracy requirements |

> YOLOv8n is optimized for speed and efficiency, while YOLOv8x is optimized for maximum accuracy.

---

## Installation

### Requirements

- Python 3.8 or newer
- `pip`
- Git
- At least 8 GB RAM
- NVIDIA GPU and CUDA-compatible PyTorch for GPU acceleration
- Windows 10/11, Ubuntu, macOS, or another supported Linux distribution

### Install Ultralytics

```bash
pip install ultralytics
```

### Verify Installation

```bash
yolo checks
```

---

## Running Locally

### Python Example

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model("image.jpg", conf=0.5)

for result in results:
    print(result.boxes)
```

The model file is downloaded automatically when it is used for the first time.

### Command-Line Usage

Run inference on an image:

```bash
yolo predict model=yolov8n.pt source="image.jpg"
```

Run inference on a video:

```bash
yolo predict model=yolov8n.pt source="video.mp4"
```

Run inference using a webcam:

```bash
yolo predict model=yolov8n.pt source=0
```

By default, output files are saved in:

```text
runs/detect/predict/
```

---

## Verification & Test Results (Real Webcam & CCTV Surveillance Data)

Inference testing was conducted using genuine hardware-captured imagery—specifically direct laptop webcams and elevated security CCTV control room feeds—to rigorously evaluate operator presence detection and security lockout automation.

| Test Image | Sensor Source / Environment | Detected Operators | Vigilance State | Station Security | Output Artifact |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `test_1.jpg` | **Laptop Webcam (Frontal)**: User working directly in front of laptop screen | 1 | `PRESENT (ACTIVE)` | `OPERATIONAL` | `data/output_1.jpg` |
| `test_2.jpg` | **CCTV Control Room (Surveillance)**: Wide-angle security camera of monitoring facility | 1 | `PRESENT (ACTIVE)` | `OPERATIONAL` | `data/output_2.jpg` |
| `test_3.jpg` | **Webcam / Desk Sensor**: Empty operator workstation with chair and dual monitors | 0 | `AWAY / ABSENT` | `LOCKED` (Timeout) | `data/output_3.jpg` |

> **Audit Summary:** YOLOv8n flawlessly detected the operator in close-range laptop webcam captures and wide-angle CCTV surveillance rooms. In the vacant scene (`test_3.jpg`), it verified zero presence and triggered the `Station Security: LOCKED` state without false positives.

---

## Hardware Requirements

### Image Inference Only

| Resource | Minimum Requirement | Recommended |
|---|---|---|
| CPU | 2–4 cores | Intel Core i5 or AMD Ryzen 5 |
| RAM | 4 GB | 8–16 GB |
| Storage | 5 GB free space | 20 GB SSD |
| GPU | Not required | NVIDIA GPU optional |
| Operating system | Windows / Linux / macOS | Ubuntu or Windows 11 |

CPU-based inference works for individual images, but may be slow for large videos or real-time camera streams.

### Video and Real-Time Inference

| Resource | Minimum Requirement | Recommended |
|---|---|---|
| CPU | 4 cores | 6–8 core CPU |
| RAM | 8 GB | 16 GB or more |
| Storage | 20 GB SSD | 50 GB+ NVMe SSD |
| GPU | NVIDIA GTX 1650 4 GB | RTX 3060 12 GB or RTX 4060 Ti 16 GB |
| VRAM | 4 GB | 8–12 GB |
| Operating system | Windows 10/11 or Ubuntu | Ubuntu 22.04/24.04 |

### Custom Training

| Resource | Minimum Requirement | Recommended |
|---|---|---|
| CPU | 6 cores | 8+ cores |
| RAM | 16 GB | 32 GB |
| GPU | NVIDIA GPU with 6 GB VRAM | RTX 3060 12 GB or better |
| VRAM | 6 GB | 12–24 GB |
| Storage | 50 GB SSD | 100 GB+ NVMe SSD |

An NVIDIA CUDA GPU is strongly recommended for training custom datasets. CPU-based training is possible but significantly slower.

---

## Server and GPU Recommendations

### Basic Inference Server

For image upload and low-volume image analysis:

| Resource | Recommendation |
|---|---|
| CPU | 2–4 vCPUs |
| RAM | 4–8 GB |
| Storage | 30–50 GB NVMe SSD |
| GPU | Not required |
| Operating system | Ubuntu 22.04 LTS or Ubuntu 24.04 LTS |

This configuration is suitable for demos, APIs, small websites, and low-volume image inference.

### Real-Time Video or Camera Server

For continuous video analysis, IP cameras, or real-time detection:

| Resource | Recommendation |
|---|---|
| CPU | 8 vCPUs |
| RAM | 16–32 GB |
| Storage | 100 GB+ NVMe SSD |
| GPU | NVIDIA T4, L4, A10, RTX 3060, RTX 4060 Ti, or RTX 4070 |
| VRAM | Minimum 8 GB; 12 GB or more recommended |
| Operating system | Ubuntu Server 22.04 or Ubuntu Server 24.04 |

### Fine-Tuning and Training Server

| Scenario | Recommended GPU |
|---|---|
| Small dataset and YOLOv8n training | RTX 3060 12 GB |
| Comfortable development and training | RTX 4060 Ti 16 GB |
| Large dataset or high-resolution training | RTX 3090 24 GB |
| Powerful local training workstation | RTX 4090 24 GB |
| Cloud training | NVIDIA A10, L4, A100, or H100 |

---

## Cloud GPU Providers

| Platform | Best For | Link |
|---|---|---|
| RunPod | Hourly GPUs, Docker, Jupyter, inference, and training | [RunPod](https://www.runpod.io/) |
| Vast.ai | GPU marketplace with potentially lower-cost instances | [Vast.ai](https://vast.ai/) |
| Lambda Cloud | GPU cloud for AI and machine-learning workloads | [Lambda Cloud](https://lambdalabs.com/service/gpu-cloud) |
| Google Cloud GPU | Large-scale and scalable production infrastructure | [Google Cloud GPU](https://cloud.google.com/gpu) |
| AWS EC2 GPU | Enterprise and production deployment | [AWS EC2 Accelerated Computing](https://aws.amazon.com/ec2/instance-types/accelerated-computing/) |
| Microsoft Azure GPU VM | AI deployment using Azure infrastructure | [Azure GPU Virtual Machines](https://azure.microsoft.com/products/virtual-machines/gpu) |
| Paperspace | GPU development environment | [Paperspace](https://www.paperspace.com/) |
| Hugging Face Spaces | Demos and small ML applications | [Hugging Face Spaces](https://huggingface.co/spaces) |

> Cloud GPU pricing depends on the GPU type, region, storage, network traffic, and instance type. Always check the official pricing page of the selected provider before deployment.

---

## Cost Considerations

### Local Computer Option

| Option | Cost Type | Suitable For |
|---|---|---|
| Existing CPU computer | Almost no additional cost | Testing, image inference, demos |
| GTX 1650 / GTX 1660 | Budget GPU investment | Basic video inference |
| RTX 3060 12 GB | Strong price-to-performance option | Development, training, and inference |
| RTX 4060 Ti 16 GB | More VRAM | Larger models and datasets |
| RTX 3090 / RTX 4090 | Higher-cost option | Professional local training |

A local setup does not require recurring cloud GPU payments, and project data remains on the local machine. However, it has upfront hardware costs, electricity costs, cooling requirements, and maintenance considerations.

### Cloud Option

| Scenario | Recommendation | Cost Model |
|---|---|---|
| One-time training | RunPod, Vast.ai, Lambda Cloud | Hourly GPU billing |
| Testing and demos | Hugging Face Spaces or temporary GPU instances | Free, minimal, or usage-based |
| Small API | Standard CPU VPS | Monthly VPS billing |
| Continuous video inference | Dedicated GPU server | Monthly GPU-server cost |
| Large-scale production | AWS, Google Cloud, Azure | Scalable but generally more expensive |

### Cost Optimization

- Use a lightweight model such as YOLOv8n
- Avoid renting a GPU if CPU inference is sufficient for image-only processing
- Turn on cloud GPUs only when training is needed
- Use spot or preemptible GPU instances when possible
- Reduce image size during inference when appropriate
- Process selected video frames instead of processing every frame
- Export the model to ONNX, OpenVINO, or TensorRT
- Use batching when processing multiple images at once
- Store only necessary images and inference results

---

## Model Export and Optimization

YOLOv8n can be exported to several formats for deployment and optimization.

### ONNX Export

```bash
yolo export model=yolov8n.pt format=onnx
```

ONNX can be useful for optimized CPU inference and cross-platform deployment.

### TensorRT Export

```bash
yolo export model=yolov8n.pt format=engine device=0
```

TensorRT is recommended for high-performance inference on NVIDIA GPUs.

### OpenVINO Export

```bash
yolo export model=yolov8n.pt format=openvino
```

OpenVINO is useful for inference on Intel CPUs, Intel GPUs, and Intel edge devices.

---

## Official Resources

- [Ultralytics YOLOv8 Documentation](https://docs.ultralytics.com/models/yolov8/)
- [Ultralytics GitHub Repository](https://github.com/ultralytics/ultralytics)
- [Ultralytics YOLOv8 on Hugging Face](https://huggingface.co/Ultralytics/YOLOv8)
- [YOLOv8n ONNX Model on Hugging Face](https://huggingface.co/webnn/yolov8n)
- [COCO Dataset Official Website](https://cocodataset.org/)
- [COCO Dataset Download Page](https://cocodataset.org/#download)
- [Ultralytics COCO Dataset Documentation](https://docs.ultralytics.com/datasets/detect/coco/)
- [Roboflow Universe Datasets](https://universe.roboflow.com/)
- [Hugging Face Datasets](https://huggingface.co/datasets)

---

## License

Ultralytics YOLO source code and pretrained models are generally distributed under the **AGPL-3.0** license.

If this project is open source, it must comply with AGPL-3.0 requirements. If YOLO is used inside a closed-source or commercial product, an Ultralytics Enterprise License may be required.

For official licensing information, see:

- [Ultralytics License Information](https://www.ultralytics.com/license)
- [Ultralytics Pricing and License Plans](https://www.ultralytics.com/pricing)