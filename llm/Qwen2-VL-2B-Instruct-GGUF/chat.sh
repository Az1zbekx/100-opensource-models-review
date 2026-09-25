#!/usr/bin/env bash
# Qwen2-VL-2B-Instruct-GGUF Interactive Multimodal Terminal Chat
# Usage: ./chat.sh [--image /path/to/image.jpg] [--tokens 1024] [--threads 6]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

docker run -it --rm \
  -v "${SCRIPT_DIR}:/app" \
  -v "${HOME}/.cache/huggingface:/root/.cache/huggingface" \
  ml-base-cpu:latest \
  python3 /app/demo.py --chat "$@"
