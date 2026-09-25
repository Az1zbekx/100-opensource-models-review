#!/usr/bin/env bash
# Hermes-3-Llama-3.2-3B-GGUF Interactive Agent Terminal Chat
# Usage: ./chat.sh [--tokens 1536] [--temp 0.2] [--threads 6]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

docker run -it --rm \
  -v "${SCRIPT_DIR}:/app" \
  -v "${HOME}/.cache/huggingface:/root/.cache/huggingface" \
  ml-base-cpu:latest \
  python3 /app/demo.py --chat "$@"
