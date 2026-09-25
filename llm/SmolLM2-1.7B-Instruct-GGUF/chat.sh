#!/usr/bin/env bash
# SmolLM2-1.7B-Instruct-GGUF Interactive Terminal Chat
# Usage: ./chat.sh [--tokens 1024] [--temp 0.3] [--threads 6]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

docker run -it --rm \
  -v "${SCRIPT_DIR}:/app" \
  -v "${HOME}/.cache/huggingface:/root/.cache/huggingface" \
  ml-base-cpu:latest \
  python3 /app/demo.py --chat "$@"
