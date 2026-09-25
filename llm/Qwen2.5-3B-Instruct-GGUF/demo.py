#!/usr/bin/env python3
"""
Qwen2.5-3B-Instruct (GGUF)
Part of 100-OpenSource-Models-Review (LLM Series)

Alibaba Cloud's sweet-spot 3B foundation language model.
Trained on 18T tokens with deep multilingual capabilities (including Uzbek & Turkic languages),
advanced instruction compliance, coding, math, and structured JSON generation.
"""

import argparse
import os
import sys
import time
from llama_cpp import Llama


def format_qwen_prompt(user_text: str, system_prompt: str = "You are Qwen, created by Alibaba Cloud. You are a helpful, accurate, and concise AI assistant.") -> str:
    """Format prompt with ChatML template used by Qwen2.5."""
    prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n"
    prompt += f"<|im_start|>user\n{user_text}<|im_end|>\n"
    prompt += "<|im_start|>assistant\n"
    return prompt


def load_model(n_threads: int = 6, n_ctx: int = 4096):
    """Load Qwen2.5-3B-Instruct GGUF weights."""
    model_repo = "Qwen/Qwen2.5-3B-Instruct-GGUF"
    model_file = "qwen2.5-3b-instruct-q4_k_m.gguf"

    print("==========================================================")
    print("  🌐 Alibaba Qwen2.5-3B Multilingual Powerhouse (GGUF)")
    print("==========================================================")
    print(f"Loading '{model_file}' via llama.cpp (Context: {n_ctx}, Threads: {n_threads})...")

    t0 = time.time()
    try:
        llm = Llama.from_pretrained(
            repo_id=model_repo,
            filename=model_file,
            n_ctx=n_ctx,
            n_threads=n_threads,
            verbose=False,
        )
        print(f"Model loaded successfully in {time.time() - t0:.2f}s.\n")
        return llm
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)


def run_inference(llm: Llama, user_prompt: str, max_tokens: int = 1024, temperature: float = 0.3):
    """Run inference."""
    full_prompt = format_qwen_prompt(user_prompt)

    start_time = time.time()
    response = llm(
        full_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=0.9,
        stop=["<|im_end|>", "<|endoftext|>"],
        echo=False,
    )
    latency = time.time() - start_time

    answer = response["choices"][0]["text"].strip()
    completion_tokens = response["usage"]["completion_tokens"]
    tokens_per_sec = completion_tokens / latency if latency > 0 else 0.0

    return answer, latency, completion_tokens, tokens_per_sec


def interactive_chat(llm: Llama, max_tokens: int = 1024, temperature: float = 0.3):
    """Start interactive terminal session."""
    print("\n--- Qwen2.5-3B Interactive Session ---")
    print("Type your message (or type 'exit' or 'quit' to terminate).\n")

    history = "<|im_start|>system\nYou are a helpful and concise multilingual assistant.<|im_end|>\n"
    while True:
        try:
            user_input = input("\n👤 User: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting session.")
                break

            history += f"<|im_start|>user\n{user_input}<|im_end|>\n<|im_start|>assistant\n"
            start_time = time.time()
            res = llm(
                history,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=0.9,
                stop=["<|im_end|>", "<|endoftext|>"],
                echo=False,
            )
            elapsed = time.time() - start_time
            reply = res["choices"][0]["text"].strip()
            toks = res["usage"]["completion_tokens"]
            speed = toks / elapsed if elapsed > 0 else 0

            print(f"\n🌐 Qwen2.5:\n{reply}\n")
            print(f"[⏱️ {elapsed:.2f}s | ⚡ {speed:.1f} tok/s | 🔢 {toks} tokens]")
            history += f"{reply}<|im_end|>\n"
        except (KeyboardInterrupt, EOFError):
            print("\nSession terminated.")
            break


def main():
    parser = argparse.ArgumentParser(description="Qwen2.5-3B-Instruct Inference Runner")
    parser.add_argument("--prompt", type=str, help="Single prompt string to test")
    parser.add_argument("--input-file", type=str, help="Path to input text file")
    parser.add_argument("--chat", action="store_true", help="Launch interactive multi-turn session")
    parser.add_argument("--tokens", type=int, default=1024, help="Max generated tokens")
    parser.add_argument("--temp", type=float, default=0.3, help="Sampling temperature")
    parser.add_argument("--ctx", type=int, default=4096, help="Context window")
    parser.add_argument("--threads", type=int, default=6, help="CPU threads")
    args = parser.parse_args()

    llm = load_model(n_threads=args.threads, n_ctx=args.ctx)

    if args.chat:
        interactive_chat(llm, max_tokens=args.tokens, temperature=args.temp)
        return

    prompt_text = ""
    if args.input_file:
        if not os.path.exists(args.input_file):
            print(f"Error: file '{args.input_file}' not found.")
            sys.exit(1)
        with open(args.input_file, "r", encoding="utf-8") as f:
            prompt_text = f.read().strip()
    elif args.prompt:
        prompt_text = args.prompt
    else:
        prompt_text = "Generate a valid JSON object describing a user profile with fields: id, full_name, email, roles (list), and created_at."

    print(f"📝 Prompt:\n{prompt_text}\n")
    print("⏳ Generating response...")
    ans, dur, toks, speed = run_inference(llm, prompt_text, max_tokens=args.tokens, temperature=args.temp)
    print("\n---------------- Response ----------------")
    print(ans)
    print("------------------------------------------")
    print(f"Tokens: {toks} | Time: {dur:.2f}s | Speed: {speed:.1f} tok/s")


if __name__ == "__main__":
    main()
