#!/usr/bin/env python3
"""
DeepSeek-R1-Distill-Llama-8B (GGUF Q4_K_M)
Part of 100-OpenSource-Models-Review (LLM Series)

High-Performance Reasoning Engine based on Meta Llama-3.1 Architecture.
Distilled from DeepSeek-R1 671B reasoning traces.
Features Chain-of-Thought (<think>...</think>) problem solving, formal logic, and mathematics.
"""

import argparse
import os
import sys
import time
from llama_cpp import Llama


def format_llama_r1_prompt(user_text: str, system_prompt: str = "") -> str:
    """Format user prompt using DeepSeek-R1 Llama chat template."""
    prompt = "<|begin_of_text|>"
    if system_prompt:
        prompt += f"{system_prompt}\n"
    prompt += f"<｜User｜>{user_text}<｜Assistant｜><think>\n"
    return prompt


def split_think_and_answer(raw_text: str):
    """Separate the <think> reasoning trace from the final answer."""
    if "</think>" in raw_text:
        parts = raw_text.split("</think>", 1)
        think_part = parts[0].replace("<think>", "").strip()
        answer_part = parts[1].strip()
        return think_part, answer_part
    else:
        return raw_text.strip(), "(Model fikrlash bosqichida token limitiga yetdi)"


def load_model(n_threads: int = 6, n_ctx: int = 4096):
    """Load DeepSeek-R1 8B Q4_K_M quantized GGUF weights."""
    model_repo = "unsloth/DeepSeek-R1-Distill-Llama-8B-GGUF"
    model_file = "DeepSeek-R1-Distill-Llama-8B-Q4_K_M.gguf"

    print("==========================================================")
    print("  🧠 DeepSeek-R1-Distill-Llama-8B Reasoning Engine (GGUF)")
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
        print("Please verify internet connection or Hugging Face cache access.")
        sys.exit(1)


def run_inference(llm: Llama, user_prompt: str, max_tokens: int = 2048, temperature: float = 0.6):
    """Run reasoning generation and measure latency/throughput."""
    full_prompt = format_llama_r1_prompt(user_prompt)

    start_time = time.time()
    response = llm(
        full_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=0.95,
        stop=["<｜end of sentence｜>", "<|eot_id|>", "User:"],
        echo=False,
    )
    latency = time.time() - start_time

    raw_output = response["choices"][0]["text"]
    completion_tokens = response["usage"]["completion_tokens"]
    tokens_per_sec = completion_tokens / latency if latency > 0 else 0.0

    think_trace, final_answer = split_think_and_answer(raw_output)
    return think_trace, final_answer, latency, completion_tokens, tokens_per_sec


def interactive_chat(llm: Llama, max_tokens: int = 2048, temperature: float = 0.6):
    """Interactive CLI terminal session."""
    print("----------------------------------------------------------")
    print("  💬 Interaktiv Chat Rejimi (Chiqish uchun 'exit' deb yozing)")
    print("----------------------------------------------------------\n")

    while True:
        try:
            user_input = input("\n👤 Siz: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "chiqish", "q"]:
                print("Suhbat yakunlandi. Xayr!")
                break

            print("\n🤖 DeepSeek-R1-Llama-8B o'ylamoqda...")
            think_trace, answer, infer_time, tokens, speed = run_inference(
                llm, user_input, max_tokens=max_tokens, temperature=temperature
            )

            if think_trace:
                print("\n┌── [🤔 Fikrlash Jarayoni / Chain-of-Thought] ─────────────────────────")
                for line in think_trace.split("\n"):
                    print(f"│  {line}")
                print("└──────────────────────────────────────────────────────────────────────")

            print(f"\n💡 [Yakuniy Javob]:\n{answer}")
            print(f"\n📊 [{infer_time:.2f}s | {tokens} tokens | {speed:.1f} tok/s]")

        except KeyboardInterrupt:
            print("\nSuhbat to'xtatildi.")
            break


def main():
    parser = argparse.ArgumentParser(description="DeepSeek-R1-Distill-Llama-8B Reasoning Engine")
    parser.add_argument("--prompt", type=str, default="", help="Single prompt string to evaluate")
    parser.add_argument("--input", type=str, default="", help="Path to input text file containing prompt")
    parser.add_argument("--output", type=str, default="", help="Path to save generated output")
    parser.add_argument("--chat", action="store_true", help="Launch interactive terminal chat session")
    parser.add_argument("--tokens", type=int, default=2048, help="Maximum generated tokens (default: 2048)")
    parser.add_argument("--temp", type=float, default=0.6, help="Sampling temperature (default: 0.6)")
    parser.add_argument("--threads", type=int, default=6, help="CPU threads for inference (default: 6)")

    args = parser.parse_args()

    llm = load_model(n_threads=args.threads)

    # 1. Interactive terminal chat mode
    if args.chat or (not args.prompt and not args.input):
        interactive_chat(llm, max_tokens=args.tokens, temperature=args.temp)
        return

    # 2. File input or CLI prompt mode
    if args.input:
        if not os.path.exists(args.input):
            print(f"Error: Input file '{args.input}' not found.")
            sys.exit(1)
        with open(args.input, "r", encoding="utf-8") as f:
            prompt_text = f.read().strip()
    else:
        prompt_text = args.prompt.strip()

    print(f"--- Kiruvchi So'rov (Prompt) ---\n{prompt_text}\n")
    print("--- Fikrlash va Javob Generatsiyasi Boshlandi ---")

    think_trace, answer, infer_time, tokens, speed = run_inference(
        llm, prompt_text, max_tokens=args.tokens, temperature=args.temp
    )

    print("\n[🤔 Fikrlash Jarayoni / Chain-of-Thought]:")
    print(think_trace)
    print("\n[💡 Yakuniy Javob]:")
    print(answer)

    print("\n----------------------------------------------------------")
    print(f"Bajarildi: {infer_time:.2f}s | Tokenlar: {tokens} | Tezlik: {speed:.2f} tok/s")
    print("==========================================================")

    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(f"=== KIRUVCHI SO'ROV ===\n{prompt_text}\n\n")
            f.write(f"=== FIKRLASH JARAYONI (<think>) ===\n{think_trace}\n\n")
            f.write(f"=== YAKUNIY JAVOB ===\n{answer}\n\n")
            f.write(f"=== STATISTIKA ===\nVaqt: {infer_time:.2f}s\nTokenlar: {tokens}\nTezlik: {speed:.2f} tok/s\n")
        print(f"Natija saqlandi: {args.output}")


if __name__ == "__main__":
    main()
