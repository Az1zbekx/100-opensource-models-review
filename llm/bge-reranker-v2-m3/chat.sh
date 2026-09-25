#!/usr/bin/env bash
# BGE-Reranker-v2-M3 Interactive Cross-Encoder Reranking
# Usage: ./chat.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

docker run -it --rm \
  -v "${SCRIPT_DIR}:/app" \
  -v "${HOME}/.cache/huggingface:/root/.cache/huggingface" \
  ml-base-cpu:latest \
  python3 /app/demo.py --chat "$@"
