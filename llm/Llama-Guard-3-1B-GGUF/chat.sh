#!/usr/bin/env bash
# Llama-Guard-3-1B-GGUF Interactive Safety Moderation Terminal
# Usage: ./chat.sh [--threads 6]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

docker run -it --rm \
  -v "${SCRIPT_DIR}:/app" \
  -v "${HOME}/.cache/huggingface:/root/.cache/huggingface" \
  ml-base-cpu:latest \
  python3 /app/demo.py --chat "$@"
