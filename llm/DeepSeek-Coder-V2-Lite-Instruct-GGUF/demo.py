#!/usr/bin/env python3
"""
DeepSeek-Coder-V2-Lite-Instruct (GGUF)
Part of 100-OpenSource-Models-Review (LLM Series)

State-of-the-Art Mixture-of-Experts (MoE) Code Model.
16B Total Parameters with 2.4B Active Parameters per token.
Supports 338 programming languages, 128k context window, and advanced code synthesis.
"""

import argparse
import os
import sys
import time
from llama_cpp import Llama


def format_deepseek_prompt(user_text: str, system_prompt: str = "You are an expert AI software engineer, specializing in multiple programming languages, algorithms, and system design.") -> str:
    """Format user prompt using DeepSeek-Coder template."""
    prompt = "<｜begin of sentence｜>"
    if system_prompt:
        prompt += f"{system_prompt}\n"
    prompt += f"<｜User｜>{user_text}<｜Assistant｜>\n"
    return prompt


def load_model(n_threads: int = 6, n_ctx: int = 4096):
    """Load DeepSeek-Coder-V2-Lite GGUF weights."""
    model_repo = "bartowski/DeepSeek-Coder-V2-Lite-Instruct-GGUF"
    model_file = "DeepSeek-Coder-V2-Lite-Instruct-Q4_K_M.gguf"

    print("==========================================================")
    print("  💻 DeepSeek-Coder-V2-Lite MoE Engine (GGUF)")
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


def run_inference(llm: Llama, user_prompt: str, max_tokens: int = 1536, temperature: float = 0.2):
    """Run code generation."""
    full_prompt = format_deepseek_prompt(user_prompt)

    start_time = time.time()
    response = llm(
        full_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=0.9,
        stop=["<｜end of sentence｜>", "<|EOT|>"],
        echo=False,
    )
    latency = time.time() - start_time

    answer = response["choices"][0]["text"].strip()
    completion_tokens = response["usage"]["completion_tokens"]
    tokens_per_sec = completion_tokens / latency if latency > 0 else 0.0

    return answer, latency, completion_tokens, tokens_per_sec


def interactive_chat(llm: Llama, max_tokens: int = 1536, temperature: float = 0.2):
    """Interactive CLI terminal session."""
    print("----------------------------------------------------------")
    print("  💻 DeepSeek-Coder-V2 Interaktiv Rejim (Chiqish uchun 'exit')")
    print("----------------------------------------------------------\n")

    while True:
        try:
            user_input = input("\n👤 Siz: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "chiqish", "q"]:
                print("Suhbat yakunlandi. Xayr!")
                break

            print("\n🤖 DeepSeek-Coder-V2 kod generatsiya qilmoqda...")
            answer, infer_time, tokens, speed = run_inference(
                llm, user_input, max_tokens=max_tokens, temperature=temperature
            )

            print(f"\n💡 [Javob / Kod]:\n{answer}")
            print(f"\n📊 [{infer_time:.2f}s | {tokens} tokens | {speed:.1f} tok/s]")

        except KeyboardInterrupt:
            print("\nSuhbat to'xtatildi.")
            break


def main():
    parser = argparse.ArgumentParser(description="DeepSeek-Coder-V2-Lite-Instruct Code Engine")
    parser.add_argument("--prompt", type=str, default="", help="Single prompt string to evaluate")
    parser.add_argument("--input", type=str, default="", help="Path to input text file containing prompt")
    parser.add_argument("--output", type=str, default="", help="Path to save generated output")
    parser.add_argument("--chat", action="store_true", help="Launch interactive terminal chat session")
    parser.add_argument("--tokens", type=int, default=1536, help="Maximum generated tokens (default: 1536)")
    parser.add_argument("--temp", type=float, default=0.2, help="Sampling temperature (default: 0.2)")
    parser.add_argument("--threads", type=int, default=6, help="CPU threads for inference (default: 6)")

    args = parser.parse_args()

    llm = load_model(n_threads=args.threads)

    if args.chat or (not args.prompt and not args.input):
        interactive_chat(llm, max_tokens=args.tokens, temperature=args.temp)
        return

    if args.input:
        if not os.path.exists(args.input):
            print(f"Error: Input file '{args.input}' not found.")
            sys.exit(1)
        with open(args.input, "r", encoding="utf-8") as f:
            prompt_text = f.read().strip()
    else:
        prompt_text = args.prompt.strip()

    print(f"--- Kiruvchi So'rov (Prompt) ---\n{prompt_text}\n")
    print("--- Kod Generatsiyasi Boshlandi ---")

    answer, infer_time, tokens, speed = run_inference(
        llm, prompt_text, max_tokens=args.tokens, temperature=args.temp
    )

    print("\n[💡 Generatsiya Qilingan Kod / Javob]:")
    print(answer)

    print("\n----------------------------------------------------------")
    print(f"Bajarildi: {infer_time:.2f}s | Tokenlar: {tokens} | Tezlik: {speed:.2f} tok/s")
    print("==========================================================")

    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(f"=== KIRUVCHI SO'ROV ===\n{prompt_text}\n\n")
            f.write(f"=== YAKUNIY JAVOB ===\n{answer}\n\n")
            f.write(f"=== STATISTIKA ===\nVaqt: {infer_time:.2f}s\nTokenlar: {tokens}\nTezlik: {speed:.2f} tok/s\n")
        print(f"Natija saqlandi: {args.output}")


if __name__ == "__main__":
    main()
