#!/usr/bin/env python3
"""
StarCoder2-3B (GGUF Q4_K_M)
Part of 100-OpenSource-Models-Review (LLM Series)

Open Code Model by BigCode & Hugging Face.
Trained on The Stack v2 with 100% Permissive Open Source Licenses.
Excels in enterprise-safe code generation, Python/JS/Rust/C++, and Fill-in-the-Middle (FIM).
"""

import argparse
import os
import sys
import time
from llama_cpp import Llama


def load_model(n_threads: int = 6, n_ctx: int = 4096):
    """Load StarCoder2-3B GGUF weights."""
    model_repo = "second-state/StarCoder2-3B-GGUF"
    model_file = "starcoder2-3b-Q4_K_M.gguf"

    print("==========================================================")
    print("  💻 StarCoder2-3B Permissive Code Engine (GGUF)")
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


def run_inference(llm: Llama, user_prompt: str, max_tokens: int = 1024, temperature: float = 0.2):
    """Run code completion/generation."""
    start_time = time.time()
    response = llm(
        user_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=0.9,
        stop=["<|endoftext|>", "\n\n\n\n"],
        echo=False,
    )
    latency = time.time() - start_time

    answer = response["choices"][0]["text"].strip()
    completion_tokens = response["usage"]["completion_tokens"]
    tokens_per_sec = completion_tokens / latency if latency > 0 else 0.0

    return answer, latency, completion_tokens, tokens_per_sec


def interactive_chat(llm: Llama, max_tokens: int = 1024, temperature: float = 0.2):
    """Interactive CLI terminal session."""
    print("----------------------------------------------------------")
    print("  💻 StarCoder2-3B Interaktiv Rejim (Chiqish uchun 'exit')")
    print("----------------------------------------------------------\n")

    while True:
        try:
            user_input = input("\n👤 Siz: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "chiqish", "q"]:
                print("Suhbat yakunlandi. Xayr!")
                break

            print("\n🤖 StarCoder2-3B kod generatsiya qilmoqda...")
            answer, infer_time, tokens, speed = run_inference(
                llm, user_input, max_tokens=max_tokens, temperature=temperature
            )

            print(f"\n💡 [Javob / Kod]:\n{answer}")
            print(f"\n📊 [{infer_time:.2f}s | {tokens} tokens | {speed:.1f} tok/s]")

        except KeyboardInterrupt:
            print("\nSuhbat to'xtatildi.")
            break


def main():
    parser = argparse.ArgumentParser(description="StarCoder2-3B Code Engine")
    parser.add_argument("--prompt", type=str, default="", help="Single prompt string to evaluate")
    parser.add_argument("--input", type=str, default="", help="Path to input text file containing prompt")
    parser.add_argument("--output", type=str, default="", help="Path to save generated output")
    parser.add_argument("--chat", action="store_true", help="Launch interactive terminal chat session")
    parser.add_argument("--tokens", type=int, default=1024, help="Maximum generated tokens (default: 1024)")
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
