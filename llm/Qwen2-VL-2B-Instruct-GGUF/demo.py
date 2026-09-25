#!/usr/bin/env python3
"""
Qwen2-VL-2B-Instruct (GGUF)
Part of 100-OpenSource-Models-Review (LLM / Multimodal Series)

Alibaba's Vision-Language Model (VLM).
Processes high-resolution images, document OCR, chart analysis, and spatial reasoning.
Supports dual-modal prompts (image + text instruction) using llama.cpp and Qwen2-VL mmproj.
"""

import argparse
import base64
import os
import sys
import time
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
from llama_cpp.llama_chat_format import Qwen25VLChatHandler


def encode_image_to_base64(image_path: str) -> str:
    """Read local image and encode to base64 data URI."""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    ext = os.path.splitext(image_path)[1].lower().replace(".", "")
    if ext == "jpg":
        ext = "jpeg"
    return f"data:image/{ext};base64,{encoded_string}"


def load_model(n_threads: int = 6, n_ctx: int = 4096):
    """Download and load Qwen2-VL-2B GGUF and vision projector."""
    model_repo = "bartowski/Qwen2-VL-2B-Instruct-GGUF"
    model_file = "Qwen2-VL-2B-Instruct-Q4_K_M.gguf"
    mmproj_file = "mmproj-Qwen2-VL-2B-Instruct-f16.gguf"

    print("==========================================================")
    print("  👁️ Qwen2-VL-2B Multimodal Vision-Language Engine")
    print("==========================================================")
    print(f"Loading '{model_file}' and '{mmproj_file}' via llama.cpp...")

    t0 = time.time()
    try:
        model_path = hf_hub_download(repo_id=model_repo, filename=model_file)
        mmproj_path = hf_hub_download(repo_id=model_repo, filename=mmproj_file)

        chat_handler = Qwen25VLChatHandler(clip_model_path=mmproj_path, verbose=False)
        llm = Llama(
            model_path=model_path,
            chat_handler=chat_handler,
            n_ctx=n_ctx,
            n_threads=n_threads,
            verbose=False,
        )
        print(f"Vision model loaded successfully in {time.time() - t0:.2f}s.\n")
        return llm
    except Exception as e:
        print(f"Error loading multimodal model: {e}")
        sys.exit(1)


def run_inference(llm: Llama, prompt: str, image_path: str = None, max_tokens: int = 1024, temperature: float = 0.2):
    """Run multimodal inference."""
    content = []
    if image_path and os.path.exists(image_path):
        data_uri = encode_image_to_base64(image_path)
        content.append({"type": "image_url", "image_url": {"url": data_uri}})
    content.append({"type": "text", "text": prompt})

    messages = [
        {"role": "system", "content": "You are a helpful and precise vision-language assistant."},
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


def interactive_chat(llm: Llama, max_tokens: int = 1024, temperature: float = 0.2):
    """Interactive visual QA session."""
    print("\n--- Qwen2-VL Interactive Vision-Language Session ---")
    print("Provide an image path or ask questions (type 'exit' to quit).\n")

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
            print(f"\n👁️ Qwen2-VL:\n{ans}\n")
            print(f"[⏱️ {dur:.2f}s | ⚡ {speed:.1f} tok/s | 🔢 {toks} tokens]")
        except (KeyboardInterrupt, EOFError):
            print("\nSession terminated.")
            break


def main():
    parser = argparse.ArgumentParser(description="Qwen2-VL-2B-Instruct Inference Runner")
    parser.add_argument("--prompt", type=str, default="Describe everything visible in this scene in concise technical detail.", help="Text prompt")
    parser.add_argument("--image", type=str, help="Path to image file")
    parser.add_argument("--chat", action="store_true", help="Launch interactive visual session")
    parser.add_argument("--tokens", type=int, default=1024, help="Max generated tokens")
    parser.add_argument("--temp", type=float, default=0.2, help="Sampling temperature")
    parser.add_argument("--ctx", type=int, default=4096, help="Context window")
    parser.add_argument("--threads", type=int, default=6, help="CPU threads")
    args = parser.parse_args()

    llm = load_model(n_threads=args.threads, n_ctx=args.ctx)

    if args.chat:
        interactive_chat(llm, max_tokens=args.tokens, temperature=args.temp)
        return

    print(f"🖼️ Image: {args.image if args.image else 'None (Text-only query)'}")
    print(f"📝 Prompt:\n{args.prompt}\n")
    print("⏳ Running multimodal perception...")
    ans, dur, toks, speed = run_inference(llm, args.prompt, args.image, max_tokens=args.tokens, temperature=args.temp)
    print("\n---------------- Response ----------------")
    print(ans)
    print("------------------------------------------")
    print(f"Tokens: {toks} | Time: {dur:.2f}s | Speed: {speed:.1f} tok/s")


if __name__ == "__main__":
    main()
