#!/usr/bin/env bash
# Qwen2.5-1.5B-Instruct-GGUF Interactive Terminal Chat
# Usage: ./chat.sh [--tokens 1024] [--temperature 0.7]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

docker run -it --rm \
  -v "${SCRIPT_DIR}:/app" \
  -v "${HOME}/.cache/huggingface:/root/.cache/huggingface" \
  ml-base-cpu:latest \
  python3 /app/demo.py --chat "$@"
