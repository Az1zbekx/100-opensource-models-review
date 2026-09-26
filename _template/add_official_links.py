#!/usr/bin/env python3
"""
Adds official clickable web links (Hugging Face / GitHub / Ultralytics)
and weights download instructions to every model README across CV, LLM, TTS, and STT.
"""

import os

REPO_ROOT = "/home/az1z6ekx/100-opensource-models-review"

MODEL_LINKS = {
    # CV
    "yolov3-tiny": ("https://github.com/ultralytics/yolov3", "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov3-tiny.pt"),
    "yolov4-tiny": ("https://github.com/AlexeyAB/darknet", "https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights"),
    "yolov5n": ("https://github.com/ultralytics/yolov5", "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov5nu.pt"),
    "yolov5s": ("https://github.com/ultralytics/yolov5", "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov5su.pt"),
    "yolov5m": ("https://github.com/ultralytics/yolov5", "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov5mu.pt"),
    "yolov6n": ("https://github.com/meituan/YOLOv6", "https://github.com/meituan/YOLOv6/releases/download/0.4.0/yolov6n.pt"),
    "yolov6s": ("https://github.com/meituan/YOLOv6", "https://github.com/meituan/YOLOv6/releases/download/0.4.0/yolov6s.pt"),
    "yolov7-tiny": ("https://github.com/WongKinYiu/yolov7", "https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7-tiny.pt"),
    "yolov8n": ("https://github.com/ultralytics/ultralytics", "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n.pt"),
    "yolov8s": ("https://github.com/ultralytics/ultralytics", "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8s.pt"),
    "yolov8m": ("https://github.com/ultralytics/ultralytics", "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8m.pt"),
    "yolov9t": ("https://github.com/WongKinYiu/yolov9", "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov9t.pt"),
    "yolov9s": ("https://github.com/WongKinYiu/yolov9", "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov9s.pt"),
    "yolov10n": ("https://github.com/THU-MIG/yolov10", "https://github.com/jameslahm/yolov10/releases/download/v1.0/yolov10n.pt"),
    "yolov10s": ("https://github.com/THU-MIG/yolov10", "https://github.com/jameslahm/yolov10/releases/download/v1.0/yolov10s.pt"),
    "yolo11n": ("https://github.com/ultralytics/ultralytics", "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt"),
    "yolo11s": ("https://github.com/ultralytics/ultralytics", "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11s.pt"),
    "yolo11m": ("https://github.com/ultralytics/ultralytics", "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11m.pt"),
    "yolo11n-pose": ("https://github.com/ultralytics/ultralytics", "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n-pose.pt"),
    "yolo11n-seg": ("https://github.com/ultralytics/ultralytics", "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n-seg.pt"),
    "yolov8s-worldv2": ("https://github.com/AILab-CVC/YOLO-World", "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8s-worldv2.pt"),
    "depth-anything-v2-small": ("https://huggingface.co/depth-anything/Depth-Anything-V2-Small", "https://github.com/DepthAnything/Depth-Anything-V2"),
    "insightface-arcface": ("https://github.com/deepinsight/insightface", "https://github.com/deepinsight/insightface/tree/master/python-package"),
    "bytetrack-mot": ("https://github.com/ifzhang/ByteTrack", "https://github.com/ifzhang/ByteTrack"),
    "opencv-video-stream": ("https://github.com/opencv/opencv", "https://opencv.org"),
    "yolo-object-detection": ("https://github.com/ultralytics/ultralytics", "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n.pt"),
    "yolo-pose-sleeping": ("https://github.com/ultralytics/ultralytics", "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-pose.pt"),

    # LLM
    "DeepSeek-Coder-V2-Lite-Instruct-GGUF": ("https://huggingface.co/bartowski/DeepSeek-Coder-V2-Lite-Instruct-GGUF", "https://github.com/deepseek-ai/DeepSeek-Coder-V2"),
    "DeepSeek-R1-Distill-Llama-8B-GGUF": ("https://huggingface.co/bartowski/DeepSeek-R1-Distill-Llama-8B-GGUF", "https://github.com/deepseek-ai/DeepSeek-R1"),
    "DeepSeek-R1-Distill-Qwen-1.5B-GGUF": ("https://huggingface.co/bartowski/DeepSeek-R1-Distill-Qwen-1.5B-GGUF", "https://github.com/deepseek-ai/DeepSeek-R1"),
    "Gemma-2-2B-Instruct-GGUF": ("https://huggingface.co/bartowski/gemma-2-2b-it-GGUF", "https://huggingface.co/google/gemma-2-2b-it"),
    "Granite-3.0-2B-Instruct-GGUF": ("https://huggingface.co/bartowski/granite-3.0-2b-instruct-GGUF", "https://huggingface.co/ibm-granite/granite-3.0-2b-instruct"),
    "Hermes-3-Llama-3.2-3B-GGUF": ("https://huggingface.co/NousResearch/Hermes-3-Llama-3.2-3B-GGUF", "https://huggingface.co/NousResearch/Hermes-3-Llama-3.2-3B"),
    "Llama-3.1-8B-Instruct-GGUF": ("https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF", "https://huggingface.co/meta-llama/Meta-Llama-3.1-8B-Instruct"),
    "Llama-3.2-1B-Instruct-GGUF": ("https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF", "https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct"),
    "Llama-Guard-3-1B-GGUF": ("https://huggingface.co/bartowski/Llama-Guard-3-1B-GGUF", "https://huggingface.co/meta-llama/Llama-Guard-3-1B"),
    "Mistral-7B-Instruct-v0.3-GGUF": ("https://huggingface.co/bartowski/Mistral-7B-Instruct-v0.3-GGUF", "https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3"),
    "Moondream2-GGUF": ("https://huggingface.co/vikhyatk/moondream2", "https://github.com/vikhyat/moondream"),
    "NLLB-200-Distilled-600M": ("https://huggingface.co/facebook/nllb-200-distilled-600M", "https://github.com/facebookresearch/fairseq/tree/nllb"),
    "Phi-3.5-mini-instruct-GGUF": ("https://huggingface.co/bartowski/Phi-3.5-mini-instruct-GGUF", "https://huggingface.co/microsoft/Phi-3.5-mini-instruct"),
    "Qwen2-VL-2B-Instruct-GGUF": ("https://huggingface.co/Qwen/Qwen2-VL-2B-Instruct-GGUF", "https://github.com/QwenLM/Qwen2-VL"),
    "Qwen2.5-1.5B-Instruct-GGUF": ("https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF", "https://github.com/QwenLM/Qwen2.5"),
    "Qwen2.5-3B-Instruct-GGUF": ("https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF", "https://github.com/QwenLM/Qwen2.5"),
    "Qwen2.5-Coder-1.5B-Instruct-GGUF": ("https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF", "https://github.com/QwenLM/Qwen2.5-Coder"),
    "SmolLM2-1.7B-Instruct-GGUF": ("https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B-Instruct-GGUF", "https://github.com/huggingface/smollm"),
    "StarCoder2-3B-GGUF": ("https://huggingface.co/bartowski/starcoder2-3b-GGUF", "https://github.com/bigcode-project/starcoder2"),
    "bge-m3": ("https://huggingface.co/BAAI/bge-m3", "https://github.com/FlagOpen/FlagEmbedding"),
    "bge-reranker-v2-m3": ("https://huggingface.co/BAAI/bge-reranker-v2-m3", "https://github.com/FlagOpen/FlagEmbedding"),

    # TTS
    "bark-small": ("https://huggingface.co/suno/bark-small", "https://github.com/suno-ai/bark"),
    "chattts": ("https://huggingface.co/2noise/ChatTTS", "https://github.com/2noise/ChatTTS"),
    "coqui-tts-vits": ("https://github.com/coqui-ai/TTS", "https://huggingface.co/coqui/tts-vits"),
    "coqui-xtts-v2": ("https://huggingface.co/coqui/XTTS-v2", "https://github.com/coqui-ai/TTS"),
    "cosyvoice-300m": ("https://huggingface.co/FunAudioLLM/CosyVoice-300M", "https://github.com/FunAudioLLM/CosyVoice"),
    "e2-tts": ("https://huggingface.co/SWivid/E2-TTS", "https://github.com/SWivid/F5-TTS"),
    "espeak-ng": ("https://github.com/espeak-ng/espeak-ng", "https://github.com/espeak-ng/espeak-ng/releases"),
    "f5-tts": ("https://huggingface.co/SWivid/F5-TTS", "https://github.com/SWivid/F5-TTS"),
    "fastspeech2": ("https://github.com/espnet/espnet", "https://huggingface.co/espnet/fastspeech2"),
    "fish-speech-1.5": ("https://huggingface.co/fishaudio/fish-speech-1.5", "https://github.com/fishaudio/fish-speech"),
    "glow-tts": ("https://github.com/jaywalnut310/glow-tts", "https://github.com/jaywalnut310/glow-tts"),
    "matcha-tts": ("https://huggingface.co/shivammehta25/Matcha-TTS", "https://github.com/shivammehta25/Matcha-TTS"),
    "meta-voice-1b": ("https://huggingface.co/metavoiceio/metavoice-1B-v0.1", "https://github.com/metavoiceio/metavoice-src"),
    "mms-tts-kaz": ("https://huggingface.co/facebook/mms-tts-kaz", "https://github.com/facebookresearch/fairseq/tree/main/examples/mms"),
    "mms-tts-uzb": ("https://huggingface.co/facebook/mms-tts-uzb-script_cyrillic", "https://github.com/facebookresearch/fairseq/tree/main/examples/mms"),
    "mms-tts-uzb-latin": ("https://huggingface.co/facebook/mms-tts-uzb-script_latin", "https://github.com/facebookresearch/fairseq/tree/main/examples/mms"),
    "openvoice-v2": ("https://huggingface.co/myshell-ai/OpenVoice-v2", "https://github.com/myshell-ai/OpenVoice"),
    "parler-tts-mini": ("https://huggingface.co/parler-tts/parler-tts-mini-v1", "https://github.com/huggingface/parler-tts"),
    "piper-tts": ("https://github.com/rhasspy/piper", "https://huggingface.co/rhasspy/piper-voices"),
    "seamless-m4t-tts": ("https://huggingface.co/facebook/seamless-m4t-v2-large", "https://github.com/facebookresearch/seamless_communication"),
    "sherpa-onnx-offline-tts": ("https://github.com/k2-fsa/sherpa-onnx", "https://k2-fsa.github.io/sherpa/onnx/tts/"),
    "speecht5-tts": ("https://huggingface.co/microsoft/speecht5_tts", "https://github.com/microsoft/SpeechT5"),
    "styletts2": ("https://huggingface.co/yl4579/StyleTTS2-LibriTTS", "https://github.com/yl4579/StyleTTS2"),
    "tacotron2": ("https://github.com/NVIDIA/DeepLearningExamples/tree/master/PyTorch/SpeechSynthesis/Tacotron2", "https://pytorch.org/hub/nvidia_deeplearningexamples_tacotron2/"),
    "tortoise-tts": ("https://github.com/neonbjb/tortoise-tts", "https://huggingface.co/jbetker/tortoise-tts-eval"),
    "valle-x": ("https://github.com/Plachtaa/VALL-E-X", "https://github.com/microsoft/unilm/tree/master/valle"),

    # STT
    "conformer-ctc": ("https://huggingface.co/nvidia/stt_en_conformer_ctc_small", "https://github.com/NVIDIA/NeMo"),
    "data2vec-audio-large": ("https://huggingface.co/facebook/data2vec-audio-large-960h", "https://github.com/facebookresearch/fairseq/tree/main/examples/data2vec"),
    "FasterWhisper": ("https://huggingface.co/Systran/faster-whisper-small", "https://github.com/SYSTRAN/faster-whisper"),
    "funasr-paraformer": ("https://huggingface.co/FunASR/paraformer-large", "https://github.com/modelscope/FunASR"),
    "hubert-large-ls960": ("https://huggingface.co/facebook/hubert-large-ls960-ft", "https://github.com/facebookresearch/fairseq/tree/main/examples/hubert"),
    "insanely-fast-whisper": ("https://github.com/Vaibhavs10/insanely-fast-whisper", "https://huggingface.co/openai/whisper-large-v3"),
    "mms-1b-all": ("https://huggingface.co/facebook/mms-1b-all", "https://github.com/facebookresearch/fairseq/tree/main/examples/mms"),
    "moonshine-base": ("https://huggingface.co/UsefulSensors/moonshine-base", "https://github.com/usefulsensors/moonshine"),
    "moonshine-tiny": ("https://huggingface.co/UsefulSensors/moonshine-tiny", "https://github.com/usefulsensors/moonshine"),
    "nemo-canary-1b": ("https://huggingface.co/nvidia/canary-1b", "https://github.com/NVIDIA/NeMo"),
    "seamless-m4t-stt": ("https://huggingface.co/facebook/seamless-m4t-v2-large", "https://github.com/facebookresearch/seamless_communication"),
    "sensevoice-small": ("https://huggingface.co/FunAudioLLM/SenseVoiceSmall", "https://github.com/FunAudioLLM/SenseVoice"),
    "sherpa-onnx-offline-stt": ("https://github.com/k2-fsa/sherpa-onnx", "https://k2-fsa.github.io/sherpa/onnx/"),
    "silero-stt": ("https://github.com/snakers4/silero-models", "https://pytorch.org/hub/snakers4_silero-models_stt/"),
    "vosk-api-uz": ("https://alphacephei.com/vosk/models", "https://github.com/alphacep/vosk-api"),
    "wav2vec2-large-xlsr-uz": ("https://huggingface.co/facebook/wav2vec2-large-xlsr-53", "https://github.com/facebookresearch/fairseq/tree/main/examples/wav2vec"),
    "wavlm-large": ("https://huggingface.co/microsoft/wavlm-large", "https://github.com/microsoft/unilm/tree/master/wavlm"),
    "whisper-base": ("https://huggingface.co/openai/whisper-base", "https://github.com/openai/whisper"),
    "whisper-cpp": ("https://github.com/ggerganov/whisper.cpp", "https://huggingface.co/ggerganov/whisper.cpp"),
    "whisper-diarization": ("https://huggingface.co/pyannote/speaker-diarization-3.1", "https://github.com/MahmoudAshraf97/whisper-diarization"),
    "whisper-large-v3-turbo": ("https://huggingface.co/openai/whisper-large-v3-turbo", "https://github.com/openai/whisper"),
    "whisper-medium": ("https://huggingface.co/openai/whisper-medium", "https://github.com/openai/whisper"),
    "whisper-small-uz": ("https://huggingface.co/openai/whisper-small", "https://github.com/openai/whisper"),
    "whisper-timestamped": ("https://github.com/linto-ai/whisper-timestamped", "https://huggingface.co/openai/whisper-small"),
    "whisper-tiny": ("https://huggingface.co/openai/whisper-tiny", "https://github.com/openai/whisper"),
    "zipformer-transducer": ("https://github.com/k2-fsa/icefall", "https://k2-fsa.github.io/icefall/recipes/librispeech/zipformer.html"),
}

def update_readmes():
    updated = 0
    for cat in ["cv", "llm", "tts", "stt"]:
        cat_dir = os.path.join(REPO_ROOT, cat)
        models = [d for d in os.listdir(cat_dir) if os.path.isdir(os.path.join(cat_dir, d)) and d != 'venv-cv']
        for m in sorted(models):
            readme_path = os.path.join(cat_dir, m, "README.md")
            if not os.path.exists(readme_path):
                continue
            
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()

            if m in MODEL_LINKS:
                primary_link, secondary_link = MODEL_LINKS[m]
                link_section = f"""

---

## 🔗 Rasmiy Manbalar va Yuklab Olish (Official Links & Weights)

- **Asosiy Repozitoriy / Model Hub:** [{primary_link}]({primary_link})
- **Qo'shimcha Manba / Upstream:** [{secondary_link}]({secondary_link})
- **Avtomatik yuklab olish:** Demo skriptni birinchi marta ishga tushirganingizda vaznlar ushbu rasmiy manbalardan avtomatik yuklab olinadi.
"""
                # Check if already has this exact section
                if "## 🔗 Rasmiy Manbalar va Yuklab Olish" not in content:
                    content = content.strip() + "\n" + link_section
                    with open(readme_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    updated += 1

    print(f"✅ Successfully added official links section to {updated} model READMEs!")

if __name__ == "__main__":
    update_readmes()
