#!/usr/bin/env python3
"""
Mistral-7B-Instruct-v0.3 (GGUF)
Part of 100-OpenSource-Models-Review (LLM Series)

The European Flagship 7B Model by Mistral AI.
Features 32k context length, function calling support, and Tekken tokenizer.
Renowned for crisp, non-bloated, highly fluent instruction following.
"""

import argparse
import os
import sys
import time
from llama_cpp import Llama


def format_mistral_prompt(user_text: str, system_prompt: str = "You are a helpful, professional, and direct AI assistant.") -> str:
    """Format prompt with Mistral v0.3 [INST] template."""
    prompt = "<s>[INST] "
    if system_prompt:
        prompt += f"{system_prompt}\n\n"
    prompt += f"{user_text} [/INST]"
    return prompt


def load_model(n_threads: int = 6, n_ctx: int = 4096):
    """Load Mistral-7B-Instruct-v0.3 GGUF weights."""
    model_repo = "bartowski/Mistral-7B-Instruct-v0.3-GGUF"
    model_file = "Mistral-7B-Instruct-v0.3-Q4_K_M.gguf"

    print("==========================================================")
    print("  🌪️ Mistral-7B-Instruct-v0.3 Engine (GGUF)")
    print("==========================================================")
    print(f"Loading '{model_file}' via llama.cpp (Context: {n_ctx}, Threads: {n_threads})...")

    t0 = time.time()
    try:
        llm = Llama(
            model_path=None,
        ) if False else Llama.from_pretrained(
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


def run_inference(llm: Llama, user_prompt: str, max_tokens: int = 1536, temperature: float = 0.3):
    """Run inference."""
    full_prompt = format_mistral_prompt(user_prompt)

    start_time = time.time()
    response = llm(
        full_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=0.9,
        stop=["</s>", "[INST]"],
        echo=False,
    )
    latency = time.time() - start_time

    answer = response["choices"][0]["text"].strip()
    completion_tokens = response["usage"]["completion_tokens"]
    tokens_per_sec = completion_tokens / latency if latency > 0 else 0.0

    return answer, latency, completion_tokens, tokens_per_sec


def interactive_chat(llm: Llama, max_tokens: int = 1536, temperature: float = 0.3):
    """Start interactive terminal session."""
    print("\n--- Mistral-7B-Instruct-v0.3 Interactive Session ---")
    print("Type your message (or type 'exit' or 'quit' to terminate).\n")

    history = "<s>[INST] You are a helpful assistant. [/INST] Understood. How can I assist you today?</s>"
    while True:
        try:
            user_input = input("\n👤 User: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting session.")
                break

            prompt = f"{history}[INST] {user_input} [/INST]"
            start_time = time.time()
            res = llm(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=0.9,
                stop=["</s>", "[INST]"],
                echo=False,
            )
            elapsed = time.time() - start_time
            reply = res["choices"][0]["text"].strip()
            toks = res["usage"]["completion_tokens"]
            speed = toks / elapsed if elapsed > 0 else 0

            print(f"\n🌪️ Mistral:\n{reply}\n")
            print(f"[⏱️ {elapsed:.2f}s | ⚡ {speed:.1f} tok/s | 🔢 {toks} tokens]")
            history = f"{prompt} {reply}</s>"
        except (KeyboardInterrupt, EOFError):
            print("\nSession terminated.")
            break


def main():
    parser = argparse.ArgumentParser(description="Mistral-7B-Instruct-v0.3 Inference Runner")
    parser.add_argument("--prompt", type=str, help="Single prompt string to test")
    parser.add_argument("--input-file", type=str, help="Path to input text file")
    parser.add_argument("--chat", action="store_true", help="Launch interactive multi-turn session")
    parser.add_argument("--tokens", type=int, default=1536, help="Max generated tokens")
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
        prompt_text = "Analyze the key differences between monolithic architectures and event-driven microservices for a high-traffic fintech application."

    print(f"📝 Prompt:\n{prompt_text}\n")
    print("⏳ Generating response...")
    ans, dur, toks, speed = run_inference(llm, prompt_text, max_tokens=args.tokens, temperature=args.temp)
    print("\n---------------- Response ----------------")
    print(ans)
    print("------------------------------------------")
    print(f"Tokens: {toks} | Time: {dur:.2f}s | Speed: {speed:.1f} tok/s")


if __name__ == "__main__":
    main()
