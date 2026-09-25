#!/usr/bin/env python3
"""
DeepSeek-R1-Distill-Qwen-1.5B (GGUF Q4_K_M)
Part of 100-OpenSource-Models-Review (LLM Series)

Offline Reasoning Engine with Chain-of-Thought (<think>...</think>) capability.
Supports interactive terminal chat, single-prompt CLI, and automated file-based benchmarks.
"""

import argparse
import os
import sys
import time
from llama_cpp import Llama


def format_deepseek_prompt(user_text: str, system_prompt: str = "") -> str:
    """Format user prompt using official DeepSeek-R1 template."""
    prompt = "<｜begin of sentence｜>"
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
        # Reached token limit while still inside thinking phase
        return raw_text.strip(), "(Model fikrlash bosqichida token limitiga yetdi)"


def load_model(n_threads: int = 4, n_ctx: int = 4096):
    """Load DeepSeek-R1 1.5B Q4_K_M quantized GGUF weights."""
    model_repo = "unsloth/DeepSeek-R1-Distill-Qwen-1.5B-GGUF"
    model_file = "DeepSeek-R1-Distill-Qwen-1.5B-Q4_K_M.gguf"

    print("==========================================================")
    print("  🧠 DeepSeek-R1-Distill-Qwen-1.5B Reasoning Engine (GGUF)")
    print("==========================================================")
    print(f"Loading '{model_file}' via llama.cpp (Context: {n_ctx}, Threads: {n_threads})...")

    t0 = time.time()
    try:
        llm = Llama.from_pretrained(
            repo_id=model_repo,
            filename=model_file,
            n_ctx=n_ctx,
            n_threads=n_threads,
            verbose=False
        )
        print(f"Model loaded successfully in {time.time() - t0:.2f}s.\n")
        return llm
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)


def run_inference(llm, prompt_text: str, max_tokens: int = 1536, temperature: float = 0.6, top_p: float = 0.95):
    """Execute inference and measure reasoning tokens and speed."""
    formatted = format_deepseek_prompt(prompt_text)

    t0 = time.time()
    output = llm(
        formatted,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        repeat_penalty=1.1,
        stop=["<｜end of sentence｜>", "<|endoftext|>"],
        echo=False
    )
    infer_time = time.time() - t0

    raw_response = output["choices"][0]["text"]
    think_trace, final_answer = split_think_and_answer(raw_response)

    usage = output.get("usage", {})
    completion_tokens = usage.get("completion_tokens", len(raw_response.split()))
    tok_per_sec = completion_tokens / max(infer_time, 0.001)

    return think_trace, final_answer, infer_time, completion_tokens, tok_per_sec


def interactive_chat(llm, max_tokens: int = 1536, temperature: float = 0.6):
    """Run an interactive conversation loop in the terminal."""
    print("----------------------------------------------------------")
    print("  💬 Interaktiv Terminal Chat Rejimi (DeepSeek-R1)")
    print("  Savolingizni yozing (Chiqish uchun 'exit' yoki 'quit' deb yozing)")
    print("----------------------------------------------------------\n")

    while True:
        try:
            user_input = input("\n👤 Siz: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "chiqish", "q"]:
                print("Suhbat yakunlandi. Xayr!")
                break

            print("\n🤖 DeepSeek-R1 o'ylamoqda...")
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
    parser = argparse.ArgumentParser(description="DeepSeek-R1-Distill-Qwen-1.5B Reasoning Engine")
    parser.add_argument("--prompt", type=str, default="", help="Single prompt string to evaluate")
    parser.add_argument("--input", type=str, default="", help="Path to input text file containing prompt")
    parser.add_argument("--output", type=str, default="", help="Path to save generated output")
    parser.add_argument("--chat", action="store_true", help="Launch interactive terminal chat session")
    parser.add_argument("--tokens", type=int, default=1536, help="Maximum generated tokens (default: 1536)")
    parser.add_argument("--temp", type=float, default=0.6, help="Sampling temperature (default: 0.6)")
    parser.add_argument("--threads", type=int, default=4, help="CPU threads for inference (default: 4)")

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

    if think_trace:
        print("\n[🤔 Fikrlash Jarayoni / Chain-of-Thought]:")
        print(think_trace)

    print("\n[💡 Yakuniy Javob]:")
    print(answer)

    print("\n----------------------------------------------------------")
    print(f"Bajarildi: {infer_time:.2f}s | Tokenlar: {tokens} | Tezlik: {speed:.2f} tok/s")
    print("==========================================================")

    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(output_output := args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            if think_trace:
                f.write(f"--- Fikrlash Jarayoni (<think>) ---\n{think_trace}\n\n")
            f.write(f"--- Yakuniy Javob ---\n{answer}\n")
        print(f"Natija saqlandi: {args.output}")


if __name__ == "__main__":
    main()
