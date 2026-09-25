#!/usr/bin/env python3
"""
Phi-3.5-mini-instruct (GGUF)
Part of 100-OpenSource-Models-Review (LLM Series)

Microsoft's 3.8B parameter high-density reasoning model.
Trained on synthetic textbooks and curated educational data.
Features 128k context support and strong multi-step logic and mathematical capabilities.
"""

import argparse
import os
import sys
import time
from llama_cpp import Llama


def format_phi_prompt(user_text: str, system_prompt: str = "You are a helpful, precise AI assistant specialized in reasoning, analysis, and concise technical solutions.") -> str:
    """Format prompt with Microsoft Phi-3.5 template."""
    prompt = ""
    if system_prompt:
        prompt += f"<|system|>\n{system_prompt}<|end|>\n"
    prompt += f"<|user|>\n{user_text}<|end|>\n<|assistant|>\n"
    return prompt


def load_model(n_threads: int = 6, n_ctx: int = 4096):
    """Load Phi-3.5-mini-instruct GGUF weights."""
    model_repo = "bartowski/Phi-3.5-mini-instruct-GGUF"
    model_file = "Phi-3.5-mini-instruct-Q4_K_M.gguf"

    print("==========================================================")
    print("  🔬 Microsoft Phi-3.5-mini Reasoning Engine (GGUF)")
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
    """Run reasoning inference."""
    full_prompt = format_phi_prompt(user_prompt)

    start_time = time.time()
    response = llm(
        full_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=0.9,
        stop=["<|end|>", "<|endoftext|>"],
        echo=False,
    )
    latency = time.time() - start_time

    answer = response["choices"][0]["text"].strip()
    completion_tokens = response["usage"]["completion_tokens"]
    tokens_per_sec = completion_tokens / latency if latency > 0 else 0.0

    return answer, latency, completion_tokens, tokens_per_sec


def interactive_chat(llm: Llama, max_tokens: int = 1536, temperature: float = 0.2):
    """Start interactive terminal session."""
    print("\n--- Microsoft Phi-3.5-mini Interactive Session ---")
    print("Type your message (or type 'exit' or 'quit' to terminate).\n")

    history = "<|system|>\nYou are a helpful AI assistant.<|end|>\n"
    while True:
        try:
            user_input = input("\n👤 User: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting session.")
                break

            history += f"<|user|>\n{user_input}<|end|>\n<|assistant|>\n"
            start_time = time.time()
            res = llm(
                history,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=0.9,
                stop=["<|end|>", "<|endoftext|>"],
                echo=False,
            )
            elapsed = time.time() - start_time
            reply = res["choices"][0]["text"].strip()
            toks = res["usage"]["completion_tokens"]
            speed = toks / elapsed if elapsed > 0 else 0

            print(f"\n🔬 Phi-3.5:\n{reply}\n")
            print(f"[⏱️ {elapsed:.2f}s | ⚡ {speed:.1f} tok/s | 🔢 {toks} tokens]")
            history += f"{reply}<|end|>\n"
        except (KeyboardInterrupt, EOFError):
            print("\nSession terminated.")
            break


def main():
    parser = argparse.ArgumentParser(description="Phi-3.5-mini-instruct Inference Runner")
    parser.add_argument("--prompt", type=str, help="Single prompt string to test")
    parser.add_argument("--input-file", type=str, help="Path to input text file")
    parser.add_argument("--chat", action="store_true", help="Launch interactive multi-turn session")
    parser.add_argument("--tokens", type=int, default=1536, help="Max generated tokens")
    parser.add_argument("--temp", type=float, default=0.2, help="Sampling temperature")
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
        prompt_text = "If a train travels 60 miles at 30 mph, and then another 60 miles at 60 mph, what is its average speed for the entire trip? Prove your result step by step."

    print(f"📝 Prompt:\n{prompt_text}\n")
    print("⏳ Generating reasoning response...")
    ans, dur, toks, speed = run_inference(llm, prompt_text, max_tokens=args.tokens, temperature=args.temp)
    print("\n---------------- Response ----------------")
    print(ans)
    print("------------------------------------------")
    print(f"Tokens: {toks} | Time: {dur:.2f}s | Speed: {speed:.1f} tok/s")


if __name__ == "__main__":
    main()
