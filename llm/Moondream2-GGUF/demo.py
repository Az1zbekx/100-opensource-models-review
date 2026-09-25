#!/usr/bin/env python3
"""
Moondream2 (GGUF)
Part of 100-OpenSource-Models-Review (LLM / Lightweight VLM Series)

Ultra-lightweight Tiny Vision-Language Model (~1.86B parameters).
Specialized for instant visual reasoning, scene captioning, and QA on edge devices and CPUs.
Supports multimodal chat and single-image queries via llama.cpp MoondreamChatHandler.
"""

import argparse
import base64
import os
import sys
import time
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
from llama_cpp.llama_chat_format import MoondreamChatHandler


def encode_image_to_base64(image_path: str) -> str:
    """Read local image and encode to base64 data URI."""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    ext = os.path.splitext(image_path)[1].lower().replace(".", "")
    if ext == "jpg":
        ext = "jpeg"
    return f"data:image/{ext};base64,{encoded_string}"


def load_model(n_threads: int = 6, n_ctx: int = 2048):
    """Download and load Moondream2 GGUF and vision projector."""
    model_repo = "moondream/moondream2-gguf"
    model_file = "moondream2-text-model-f16.gguf"
    mmproj_file = "moondream2-mmproj-f16.gguf"

    print("==========================================================")
    print("  🌙 Moondream2 Tiny Edge Vision Engine (GGUF)")
    print("==========================================================")
    print(f"Loading '{model_file}' and '{mmproj_file}' via llama.cpp...")

    t0 = time.time()
    try:
        model_path = hf_hub_download(repo_id=model_repo, filename=model_file)
        mmproj_path = hf_hub_download(repo_id=model_repo, filename=mmproj_file)

        chat_handler = MoondreamChatHandler(clip_model_path=mmproj_path, verbose=False)
        llm = Llama(
            model_path=model_path,
            chat_handler=chat_handler,
            n_ctx=n_ctx,
            n_threads=n_threads,
            verbose=False,
        )
        print(f"Moondream2 loaded successfully in {time.time() - t0:.2f}s.\n")
        return llm
    except Exception as e:
        print(f"Error loading Moondream2: {e}")
        sys.exit(1)


def run_inference(llm: Llama, prompt: str, image_path: str = None, max_tokens: int = 512, temperature: float = 0.2):
    """Run visual perception inference."""
    content = []
    if image_path and os.path.exists(image_path):
        data_uri = encode_image_to_base64(image_path)
        content.append({"type": "image_url", "image_url": {"url": data_uri}})
    content.append({"type": "text", "text": prompt})

    messages = [
        {"role": "user", "content": content},
    ]

    start_time = time.time()
    response = llm.create_chat_completion(
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    latency = time.time() - start_time

    answer = response["choices"][0]["message"]["content"].strip()
    completion_tokens = response["usage"]["completion_tokens"]
    tokens_per_sec = completion_tokens / latency if latency > 0 else 0.0

    return answer, latency, completion_tokens, tokens_per_sec


def interactive_chat(llm: Llama, max_tokens: int = 512, temperature: float = 0.2):
    """Interactive visual QA session."""
    print("\n--- Moondream2 Interactive Vision Session ---")
    print("Commands:")
    print("  image <path>  : Load and attach a new image")
    print("  <question>    : Ask a question about the current image")
    print("  exit          : Quit session\n")

    current_image = None
    while True:
        try:
            cmd = input("\n[image <path> | or ask prompt]: ").strip()
            if not cmd:
                continue
            if cmd.lower() in ["exit", "quit"]:
                print("Exiting session.")
                break
            if cmd.startswith("image "):
                path = cmd.split(" ", 1)[1].strip()
                if os.path.exists(path):
                    current_image = path
                    print(f"Attached image: {path}")
                else:
                    print(f"Error: image not found: {path}")
                continue

            ans, dur, toks, speed = run_inference(llm, cmd, current_image, max_tokens=max_tokens, temperature=temperature)
            print(f"\n🌙 Moondream2:\n{ans}\n")
            print(f"[⏱️ {dur:.2f}s | ⚡ {speed:.1f} tok/s | 🔢 {toks} tokens]")
        except (KeyboardInterrupt, EOFError):
            print("\nSession terminated.")
            break


def main():
    parser = argparse.ArgumentParser(description="Moondream2 Edge VLM Runner")
    parser.add_argument("--prompt", type=str, default="Describe this image concisely.", help="Text prompt")
    parser.add_argument("--image", type=str, help="Path to image file")
    parser.add_argument("--chat", action="store_true", help="Launch interactive visual session")
    parser.add_argument("--tokens", type=int, default=512, help="Max generated tokens")
    parser.add_argument("--temp", type=float, default=0.2, help="Sampling temperature")
    parser.add_argument("--ctx", type=int, default=2048, help="Context window")
    parser.add_argument("--threads", type=int, default=6, help="CPU threads")
    args = parser.parse_args()

    llm = load_model(n_threads=args.threads, n_ctx=args.ctx)

    if args.chat:
        interactive_chat(llm, max_tokens=args.tokens, temperature=args.temp)
        return

    print(f"🖼️ Image: {args.image if args.image else 'None'}")
    print(f"📝 Prompt:\n{args.prompt}\n")
    print("⏳ Running tiny visual reasoning...")
    ans, dur, toks, speed = run_inference(llm, args.prompt, args.image, max_tokens=args.tokens, temperature=args.temp)
    print("\n---------------- Response ----------------")
    print(ans)
    print("------------------------------------------")
    print(f"Tokens: {toks} | Time: {dur:.2f}s | Speed: {speed:.1f} tok/s")


if __name__ == "__main__":
    main()
