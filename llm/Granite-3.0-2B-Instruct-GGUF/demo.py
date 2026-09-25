#!/usr/bin/env python3
"""
Granite-3.0-2B-Instruct (GGUF)
Part of 100-OpenSource-Models-Review (LLM Series)

IBM's enterprise-grade open-source foundation language model (Apache 2.0).
Trained on 12T tokens across enterprise, coding, tabular, and regulatory corpora.
Engineered for safe enterprise workflows, RAG, and structured reasoning.
"""

import argparse
import os
import sys
import time
from llama_cpp import Llama


def format_granite_prompt(user_text: str, system_prompt: str = "You are Granite, an AI model developed by IBM. You are a helpful, respectful, and honest assistant.") -> str:
    """Format prompt with IBM Granite 3.0 template."""
    prompt = f"<|start_of_role|>system<|end_of_role|>{system_prompt}<|end_of_text|>\n"
    prompt += f"<|start_of_role|>user<|end_of_role|>{user_text}<|end_of_text|>\n"
    prompt += "<|start_of_role|>assistant<|end_of_role|>"
    return prompt


def load_model(n_threads: int = 6, n_ctx: int = 4096):
    """Load Granite-3.0-2B-Instruct GGUF weights."""
    model_repo = "bartowski/granite-3.0-2b-instruct-GGUF"
    model_file = "granite-3.0-2b-instruct-Q4_K_M.gguf"

    print("==========================================================")
    print("  🔷 IBM Granite-3.0-2B Enterprise Engine (GGUF)")
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
    full_prompt = format_granite_prompt(user_prompt)

    start_time = time.time()
    response = llm(
        full_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=0.9,
        stop=["<|end_of_text|>"],
        echo=False,
    )
    latency = time.time() - start_time

    answer = response["choices"][0]["text"].strip()
    completion_tokens = response["usage"]["completion_tokens"]
    tokens_per_sec = completion_tokens / latency if latency > 0 else 0.0

    return answer, latency, completion_tokens, tokens_per_sec


def interactive_chat(llm: Llama, max_tokens: int = 1024, temperature: float = 0.3):
    """Start interactive terminal session."""
    print("\n--- IBM Granite-3.0-2B Interactive Session ---")
    print("Type your message (or type 'exit' or 'quit' to terminate).\n")

    history = "<|start_of_role|>system<|end_of_role|>You are Granite, developed by IBM. You are a helpful assistant.<|end_of_text|>\n"
    while True:
        try:
            user_input = input("\n👤 User: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting session.")
                break

            history += f"<|start_of_role|>user<|end_of_role|>{user_input}<|end_of_text|>\n<|start_of_role|>assistant<|end_of_role|>"
            start_time = time.time()
            res = llm(
                history,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=0.9,
                stop=["<|end_of_text|>"],
                echo=False,
            )
            elapsed = time.time() - start_time
            reply = res["choices"][0]["text"].strip()
            toks = res["usage"]["completion_tokens"]
            speed = toks / elapsed if elapsed > 0 else 0

            print(f"\n🔷 Granite-3.0:\n{reply}\n")
            print(f"[⏱️ {elapsed:.2f}s | ⚡ {speed:.1f} tok/s | 🔢 {toks} tokens]")
            history += f"{reply}<|end_of_text|>\n"
        except (KeyboardInterrupt, EOFError):
            print("\nSession terminated.")
            break


def main():
    parser = argparse.ArgumentParser(description="Granite-3.0-2B-Instruct Inference Runner")
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
        prompt_text = "What are the core components of an enterprise SLA (Service Level Agreement) for cloud databases?"

    print(f"📝 Prompt:\n{prompt_text}\n")
    print("⏳ Generating response...")
    ans, dur, toks, speed = run_inference(llm, prompt_text, max_tokens=args.tokens, temperature=args.temp)
    print("\n---------------- Response ----------------")
    print(ans)
    print("------------------------------------------")
    print(f"Tokens: {toks} | Time: {dur:.2f}s | Speed: {speed:.1f} tok/s")


if __name__ == "__main__":
    main()
