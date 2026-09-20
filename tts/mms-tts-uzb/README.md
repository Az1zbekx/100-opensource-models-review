# MMS Uzbek Cyrillic Text-to-Speech Model

This project uses the `facebook/mms-tts-uzb-script_cyrillic` model for Uzbek text-to-speech synthesis.

The model converts Uzbek text written in the **Cyrillic script** into speech audio. It is part of Meta AI's **Massively Multilingual Speech (MMS)** project and is available through the Hugging Face Transformers library.

---

## Table of Contents

- [About the Model](#about-the-model)
- [Model Capabilities](#model-capabilities)
- [Supported Language and Script](#supported-language-and-script)
- [Model Architecture](#model-architecture)
- [Dataset and Training Information](#dataset-and-training-information)
- [Technical Information](#technical-information)
- [Installation](#installation)
- [Local Usage](#local-usage)
- [Hardware Requirements](#hardware-requirements)
- [Server Deployment](#server-deployment)
- [Cloud Providers](#cloud-providers)
- [Cost Considerations](#cost-considerations)
- [Limitations](#limitations)
- [Official Resources](#official-resources)
- [License](#license)

---

## About the Model

`facebook/mms-tts-uzb-script_cyrillic` is an Uzbek text-to-speech model released by Meta AI as part of the **Massively Multilingual Speech (MMS)** project.

The model accepts Uzbek text written in the Cyrillic script and generates a speech waveform that can be saved as an audio file such as `.wav`.

The model is based on the VITS architecture and can be used for:

- Uzbek text-to-speech applications
- Voice assistants
- Accessibility tools
- Audio content generation
- Reading text aloud
- Educational applications
- Automated voice notifications
- IVR and call-center prototypes
- Chatbot voice output
- Demo and research projects

The model is available through Hugging Face and can be loaded using the `transformers` Python library.

---

## Model Capabilities

The MMS Uzbek Cyrillic TTS model can:

- Convert Uzbek Cyrillic text into speech
- Generate waveform audio from text input
- Run locally without a paid TTS API
- Run on CPU for small workloads
- Use GPU acceleration for faster inference or high-volume workloads
- Generate `.wav` audio output
- Be integrated into Python applications, APIs, bots, and web services
- Be deployed in Docker containers or cloud servers

Example input text:

```text
Салом, бу ўзбек тили учун матнни нутққа айлантириш намунаси.
```

Example output:

```text
output.wav
```

The generated file contains synthesized Uzbek speech.

---

## Supported Language and Script

| Property | Value |
|---|---|
| Language | Uzbek |
| ISO 639-3 Language Code | `uzb` |
| Supported Script | Cyrillic |
| Hugging Face Model Name | `facebook/mms-tts-uzb-script_cyrillic` |
| Task | Text-to-Speech |
| Output Type | Audio waveform |
| Common Output Format | WAV |
| Main Framework | Hugging Face Transformers |
| Architecture | VITS |

> Important: This model is specifically designed for Uzbek text written in the Cyrillic script. Uzbek text written in Latin script may need to be converted to Cyrillic before inference for more reliable output.

Example of script conversion:

```text
Latin:   Salom, dunyo!
Cyrillic: Салом, дунё!
```

---

## Model Architecture

The model uses the **VITS** architecture.

VITS stands for:

```text
Variational Inference with adversarial learning for end-to-end Text-to-Speech
```

VITS is an end-to-end text-to-speech architecture that generates speech waveforms directly from input text.

The architecture combines several important components:

- Text tokenizer
- Text encoder
- Variational autoencoder components
- Posterior encoder
- Conditional prior
- Decoder
- Flow-based transformation
- Adversarial training components

Unlike older TTS pipelines that require separate text analysis, acoustic modeling, and vocoder stages, VITS is designed as an end-to-end speech-synthesis approach.

The output of the model is a waveform, which can be saved as a `.wav` audio file.

---

## Dataset and Training Information

This checkpoint is part of the Meta AI **Massively Multilingual Speech (MMS)** project.

MMS is a multilingual speech-research initiative created to expand speech technology coverage across a large number of languages.

| Property | Information |
|---|---|
| Project | Massively Multilingual Speech (MMS) |
| Developed by | Meta AI |
| Model family | MMS-TTS |
| Uzbek model checkpoint | `mms-tts-uzb-script_cyrillic` |
| Language | Uzbek |
| Script | Cyrillic |
| Task | Text-to-Speech |
| Architecture | VITS |
| Training approach | Part of the multilingual MMS speech initiative |
| TTS language coverage | More than 1,100 languages in the MMS-TTS collection |

The public model card identifies this checkpoint as the Uzbek Cyrillic TTS checkpoint in the broader MMS project. However, it does not provide a complete public, checkpoint-specific list of every training dataset, number of Uzbek audio hours, speaker identities, audio licenses, or detailed training hyperparameters.

Therefore, this model should be described as an **MMS Uzbek Cyrillic TTS checkpoint**, rather than claiming that it was trained on one specific named Uzbek dataset.

For research details about MMS, see the official paper:

```text
Scaling Speech Technology to 1,000+ Languages
```

---

## Technical Information

| Property | Value |
|---|---|
| Model name | `facebook/mms-tts-uzb-script_cyrillic` |
| Developer | Meta AI |
| Project | Massively Multilingual Speech (MMS) |
| Model type | Text-to-Speech |
| Pipeline | `text-to-audio` |
| Language | Uzbek |
| Script | Cyrillic |
| Architecture | VITS |
| Library | Hugging Face Transformers |
| PyTorch support | Yes |
| Safetensors support | Yes |
| Input | Uzbek Cyrillic text |
| Output | Speech waveform |
| Recommended audio format | WAV |
| Transformers availability | Version 4.33 or newer |
| License | CC-BY-NC-4.0 |

---

## Installation

### Requirements

- Python 3.9 or newer recommended
- `pip`
- PyTorch
- Hugging Face Transformers
- Accelerate
- SciPy or SoundFile for saving audio
- At least 4 GB RAM for basic local inference
- NVIDIA GPU is optional but recommended for faster inference

### Install Dependencies

```bash
pip install --upgrade transformers accelerate torch scipy
```

Alternatively, install `soundfile` for saving WAV files:

```bash
pip install --upgrade transformers accelerate torch soundfile
```

---

## Local Usage

### Basic Python Example

```python
import torch
import scipy
from transformers import VitsModel, AutoTokenizer

MODEL_ID = "facebook/mms-tts-uzb-script_cyrillic"

model = VitsModel.from_pretrained(MODEL_ID)
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

text = "Салом, бу ўзбек тили учун матнни нутққа айлантириш намунаси."

inputs = tokenizer(text, return_tensors="pt")

with torch.no_grad():
    output = model(**inputs).waveform

audio = output.squeeze().cpu().numpy()

scipy.io.wavfile.write(
    "uzbek_speech.wav",
    rate=model.config.sampling_rate,
    data=audio
)
```

After running the script, the generated audio file will be saved as:

```text
uzbek_speech.wav
```

### Using GPU

If CUDA and a compatible NVIDIA GPU are available, move the model and input tensors to GPU:

```python
import torch
import scipy
from transformers import VitsModel, AutoTokenizer

MODEL_ID = "facebook/mms-tts-uzb-script_cyrillic"

device = "cuda" if torch.cuda.is_available() else "cpu"

model = VitsModel.from_pretrained(MODEL_ID).to(device)
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

text = "Салом, бу GPU орқали яратилган ўзбекча овоз намунасидир."

inputs = tokenizer(text, return_tensors="pt").to(device)

with torch.no_grad():
    output = model(**inputs).waveform

audio = output.squeeze().cpu().numpy()

scipy.io.wavfile.write(
    "uzbek_speech_gpu.wav",
    rate=model.config.sampling_rate,
    data=audio
)
```

### Saving Audio with SoundFile

```python
import soundfile as sf

sf.write(
    "uzbek_speech.wav",
    audio,
    model.config.sampling_rate
)
```

---

## Hardware Requirements

### Basic Local Inference

| Resource | Minimum Requirement | Recommended |
|---|---|---|
| CPU | 2 cores | 4+ cores |
| RAM | 4 GB | 8 GB |
| Storage | 2 GB free space | 5 GB SSD |
| GPU | Not required | NVIDIA GPU optional |
| Operating System | Windows, Linux, or macOS | Ubuntu or Windows 11 |

A CPU is sufficient for individual texts and small prototypes. Speech generation may take longer on low-power CPUs.

### Faster Inference

| Resource | Minimum Requirement | Recommended |
|---|---|---|
| CPU | 4 cores | 6–8 cores |
| RAM | 8 GB | 16 GB |
| Storage | 10 GB SSD | 20 GB NVMe SSD |
| GPU | NVIDIA GPU with 4 GB VRAM | RTX 3060 12 GB or better |
| VRAM | 4 GB | 8 GB+ |
| Operating System | Windows or Ubuntu | Ubuntu 22.04/24.04 |

For most small and medium TTS projects, a high-end GPU is not required. An NVIDIA T4, RTX 3060, RTX 4060, or similar GPU is usually sufficient for scalable inference.

### Fine-Tuning

| Resource | Minimum Requirement | Recommended |
|---|---|---|
| CPU | 6 cores | 8+ cores |
| RAM | 16 GB | 32 GB |
| GPU | NVIDIA GPU with 8 GB VRAM | RTX 3090/4090 with 24 GB VRAM |
| VRAM | 8 GB | 16–24 GB |
| Storage | 50 GB SSD | 100 GB+ NVMe SSD |

Fine-tuning a TTS model requires an aligned dataset containing audio files and their correct text transcriptions. Audio quality, speaker consistency, text normalization, and recording conditions strongly affect output quality.

---

## Server Deployment

### Basic Text-to-Speech API

For low-volume usage, such as generating audio from short text requests:

| Resource | Recommendation |
|---|---|
| CPU | 2–4 vCPUs |
| RAM | 4–8 GB |
| Storage | 30 GB SSD |
| GPU | Not required |
| Operating System | Ubuntu 22.04 LTS or Ubuntu 24.04 LTS |

This configuration is suitable for:

- Testing
- Personal projects
- Small APIs
- Small chatbot voice features
- Generating short audio files
- Low-volume text-to-speech requests

### High-Volume or Real-Time TTS API

For multiple users, frequent requests, longer text, or lower response latency:

| Resource | Recommendation |
|---|---|
| CPU | 4–8 vCPUs |
| RAM | 16 GB |
| Storage | 50–100 GB NVMe SSD |
| GPU | NVIDIA T4, L4, A10, RTX 3060, RTX 4060, or RTX 4070 |
| VRAM | 8 GB+ |
| Operating System | Ubuntu Server 22.04 or 24.04 |

For production systems, it is recommended to add:

- FastAPI or Flask for API development
- Docker for containerization
- Nginx as a reverse proxy
- HTTPS using Let’s Encrypt
- Redis or a message queue for handling multiple requests
- Object storage for generated audio files
- Request limits and authentication
- Monitoring and logging

---

## Cloud Providers

| Platform | Best For | Link |
|---|---|---|
| Hugging Face Spaces | TTS demos and small applications | [Hugging Face Spaces](https://huggingface.co/spaces) |
| RunPod | Hourly GPU instances for inference and development | [RunPod](https://www.runpod.io/) |
| Vast.ai | Lower-cost GPU marketplace | [Vast.ai](https://vast.ai/) |
| Lambda Cloud | AI and machine-learning GPU infrastructure | [Lambda Cloud](https://lambdalabs.com/service/gpu-cloud) |
| Google Cloud | Scalable cloud deployment | [Google Cloud GPU](https://cloud.google.com/gpu) |
| AWS | Enterprise infrastructure and production services | [AWS EC2 Accelerated Computing](https://aws.amazon.com/ec2/instance-types/accelerated-computing/) |
| Microsoft Azure | Cloud deployment using Azure services | [Azure GPU Virtual Machines](https://azure.microsoft.com/products/virtual-machines/gpu) |

> GPU pricing changes frequently and depends on region, GPU type, disk storage, network traffic, and billing type. Always review the provider’s official pricing page before starting deployment.

---

## Cost Considerations

### Local Deployment

| Setup | Cost Level | Suitable For |
|---|---|---|
| Existing computer with CPU | Very low | Testing and personal projects |
| CPU VPS | Low monthly cost | Small TTS API |
| GTX 1650 / RTX 2060 | Budget GPU | Faster local inference |
| RTX 3060 / RTX 4060 | Medium investment | Development and higher-volume inference |
| RTX 3090 / RTX 4090 | High investment | Fine-tuning and professional development |

For basic inference, a GPU is not mandatory. A CPU server can be enough if the number of requests is low and real-time response is not required.

### Cloud Deployment

| Scenario | Recommendation | Cost Model |
|---|---|---|
| Personal testing | Local CPU or Hugging Face demo | Free or very low cost |
| Small API | CPU VPS | Monthly billing |
| Temporary high-speed inference | RunPod or Vast.ai | Hourly GPU billing |
| Training or fine-tuning | RunPod, Vast.ai, Lambda Cloud | Hourly GPU billing |
| Enterprise deployment | AWS, Google Cloud, Azure | Scalable but higher cost |

### Cost Optimization

- Use CPU inference for low request volume
- Use GPU only for high-volume or low-latency applications
- Cache generated audio for repeated text
- Limit maximum text length per request
- Split long text into sentences or smaller chunks
- Remove temporary audio files after a defined period
- Use object storage instead of local disk for large audio collections
- Turn off cloud GPU instances when they are not needed
- Use a queue system for batch audio generation

---

## Limitations

- The model is designed for Uzbek text in the **Cyrillic script**
- Uzbek Latin text may require Cyrillic conversion for better pronunciation
- Generated voice quality can vary depending on input spelling and punctuation
- The model may not pronounce foreign names, technical words, URLs, abbreviations, and numbers naturally
- Long text should be split into smaller sentences or paragraphs
- The model may not provide multiple speaker voices
- The model may not provide emotional or expressive voice control
- The model may produce pronunciation errors for uncommon words
- The public model card does not provide a full checkpoint-specific dataset description

For improved results:

- Use correct Uzbek Cyrillic spelling
- Add punctuation marks
- Split long text into short sentences
- Normalize numbers, dates, currencies, abbreviations, and URLs before synthesis
- Convert Latin Uzbek text into Cyrillic when using this checkpoint
- Test the output with real examples from the target application

---

## Official Resources

- [MMS Uzbek Cyrillic TTS Model on Hugging Face](https://huggingface.co/facebook/mms-tts-uzb-script_cyrillic)
- [MMS-TTS Model Collection on Hugging Face](https://huggingface.co/facebook/mms-tts)
- [Hugging Face MMS Documentation](https://huggingface.co/docs/transformers/en/model_doc/mms)
- [Hugging Face VITS Documentation](https://huggingface.co/docs/transformers/en/model_doc/vits)
- [MMS Language Coverage Overview](https://dl.fbaipublicfiles.com/mms/misc/language_coverage_mms.html)
- [MMS Research Paper: Scaling Speech Technology to 1,000+ Languages](https://arxiv.org/abs/2305.13516)
- [Hugging Face Transformers](https://github.com/huggingface/transformers)
- [PyTorch](https://pytorch.org/)

---

## License

This model is distributed under the **CC-BY-NC-4.0** license.

This license allows use, sharing, and adaptation under the terms of the license, but it is intended for **non-commercial use**.

Before using this model in a paid product, commercial application, production service, or revenue-generating platform, review the official license carefully and obtain appropriate legal guidance if necessary.

Official license information:

- [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/)
- [Model License Information on Hugging Face](https://huggingface.co/facebook/mms-tts-uzb-script_cyrillic)