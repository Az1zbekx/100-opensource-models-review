#!/usr/bin/env bash
# Mistral-7B-Instruct-v0.3-GGUF Interactive Terminal Chat
# Usage: ./chat.sh [--tokens 1536] [--temp 0.3] [--threads 6]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

docker run -it --rm \
  -v "${SCRIPT_DIR}:/app" \
  -v "${HOME}/.cache/huggingface:/root/.cache/huggingface" \
  ml-base-cpu:latest \
  python3 /app/demo.py --chat "$@"
