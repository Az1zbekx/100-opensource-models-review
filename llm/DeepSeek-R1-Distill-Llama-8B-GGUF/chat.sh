#!/usr/bin/env bash
# DeepSeek-R1-Distill-Llama-8B-GGUF Interactive Terminal Chat
# Usage: ./chat.sh [--tokens 2048] [--temp 0.6] [--threads 6]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

docker run -it --rm \
  -v "${SCRIPT_DIR}:/app" \
  -v "${HOME}/.cache/huggingface:/root/.cache/huggingface" \
  ml-base-cpu:latest \
  python3 /app/demo.py --chat "$@"
