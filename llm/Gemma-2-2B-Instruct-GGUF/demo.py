#!/usr/bin/env python3
"""
Gemma-2-2B-Instruct (GGUF)
Part of 100-OpenSource-Models-Review (LLM Series)

Google DeepMind's flagship on-device language model.
Features sliding window attention, logit soft-capping, and high reasoning fidelity.
Optimized for low-latency local edge execution on CPU and low-power hardware.
"""

import argparse
import os
import sys
import time
from llama_cpp import Llama


def format_gemma_prompt(user_text: str, system_prompt: str = "You are a helpful, accurate, and concise AI assistant built by Google.") -> str:
    """Format prompt with Gemma-2 instruction template."""
    prompt = "<bos>"
    if system_prompt:
        prompt += f"<start_of_turn>user\n{system_prompt}\n\n{user_text}<end_of_turn>\n<start_of_turn>model\n"
    else:
        prompt += f"<start_of_turn>user\n{user_text}<end_of_turn>\n<start_of_turn>model\n"
    return prompt


def load_model(n_threads: int = 6, n_ctx: int = 4096):
    """Load Gemma-2-2B-Instruct GGUF weights."""
    model_repo = "bartowski/gemma-2-2b-it-GGUF"
    model_file = "gemma-2-2b-it-Q4_K_M.gguf"

    print("==========================================================")
    print("  💎 Google Gemma-2-2B Compact Engine (GGUF)")
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
    full_prompt = format_gemma_prompt(user_prompt)

    start_time = time.time()
    response = llm(
        full_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=0.9,
        stop=["<end_of_turn>", "<eos>"],
        echo=False,
    )
    latency = time.time() - start_time

    answer = response["choices"][0]["text"].strip()
    completion_tokens = response["usage"]["completion_tokens"]
    tokens_per_sec = completion_tokens / latency if latency > 0 else 0.0

    return answer, latency, completion_tokens, tokens_per_sec


def interactive_chat(llm: Llama, max_tokens: int = 1024, temperature: float = 0.3):
    """Start interactive terminal session."""
    print("\n--- Gemma-2-2B Interactive Session ---")
    print("Type your message (or type 'exit' or 'quit' to terminate).\n")

    history = "<bos>"
    is_first = True
    system_prompt = "You are a helpful, concise AI assistant."

    while True:
        try:
            user_input = input("\n👤 User: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting session.")
                break

            if is_first:
                turn_text = f"{system_prompt}\n\n{user_input}"
                is_first = False
            else:
                turn_text = user_input

            history += f"<start_of_turn>user\n{turn_text}<end_of_turn>\n<start_of_turn>model\n"
            start_time = time.time()
            res = llm(
                history,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=0.9,
                stop=["<end_of_turn>", "<eos>"],
                echo=False,
            )
            elapsed = time.time() - start_time
            reply = res["choices"][0]["text"].strip()
            toks = res["usage"]["completion_tokens"]
            speed = toks / elapsed if elapsed > 0 else 0

            print(f"\n💎 Gemma-2:\n{reply}\n")
            print(f"[⏱️ {elapsed:.2f}s | ⚡ {speed:.1f} tok/s | 🔢 {toks} tokens]")
            history += f"{reply}<end_of_turn>\n"
        except (KeyboardInterrupt, EOFError):
            print("\nSession terminated.")
            break


def main():
    parser = argparse.ArgumentParser(description="Gemma-2-2B-Instruct Inference Runner")
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
        prompt_text = "Explain the difference between process and thread in operating systems in 3 bullet points."

    print(f"📝 Prompt:\n{prompt_text}\n")
    print("⏳ Generating response...")
    ans, dur, toks, speed = run_inference(llm, prompt_text, max_tokens=args.tokens, temperature=args.temp)
    print("\n---------------- Response ----------------")
    print(ans)
    print("------------------------------------------")
    print(f"Tokens: {toks} | Time: {dur:.2f}s | Speed: {speed:.1f} tok/s")


if __name__ == "__main__":
    main()
