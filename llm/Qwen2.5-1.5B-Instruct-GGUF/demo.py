import argparse
import os
import sys
import time
from llama_cpp import Llama


def build_chatml_prompt(user_text: str, system_prompt: str = "You are a helpful, precise, and concise AI assistant.") -> str:
    return (
        f"<|im_start|>system\n{system_prompt}<|im_end|>\n"
        f"<|im_start|>user\n{user_text}<|im_end|>\n"
        f"<|im_start|>assistant\n"
    )


def main(prompt: str, input_file: str, output_file: str, max_tokens: int, temperature: float):
    # Read from input file if provided
    if input_file:
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found.")
            sys.exit(1)
        with open(input_file, "r", encoding="utf-8") as f:
            prompt_text = f.read().strip()
    else:
        prompt_text = prompt.strip()

    if not prompt_text:
        print("Error: Prompt text cannot be empty.")
        sys.exit(1)

    print("==================================================")
    print("  Qwen2.5-1.5B-Instruct-GGUF Offline Engine")
    print("==================================================")
    print("Loading model weights (Q4_K_M quantized GGUF)...")
    load_start = time.time()

    model_repo = "Qwen/Qwen2.5-1.5B-Instruct-GGUF"
    model_file = "qwen2.5-1.5b-instruct-q4_k_m.gguf"

    try:
        llm = Llama.from_pretrained(
            repo_id=model_repo,
            filename=model_file,
            n_ctx=2048,
            n_threads=4,
            verbose=False
        )
    except Exception as e:
        print(f"Failed to load model: {e}")
        sys.exit(1)

    load_time = time.time() - load_start
    print(f"Model loaded successfully in {load_time:.2f}s.")
    print(f"\n--- Input Prompt ---\n{prompt_text}\n")
    print("--- Generating Response ---")

    formatted_prompt = build_chatml_prompt(prompt_text)
    infer_start = time.time()

    output = llm(
        formatted_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        stop=["<|im_end|>", "<|endoftext|>"],
        echo=False
    )

    infer_time = time.time() - infer_start
    response_text = output["choices"][0]["text"].strip()
    usage = output.get("usage", {})
    completion_tokens = usage.get("completion_tokens", len(response_text.split()))
    tokens_per_sec = completion_tokens / infer_time if infer_time > 0 else 0.0

    print(response_text)
    print("--------------------------------------------------")
    print(f"Completed in {infer_time:.2f}s | Tokens: {completion_tokens} | Speed: {tokens_per_sec:.2f} tok/s")
    print("==================================================")

    if output_file:
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(response_text + "\n")
        print(f"Output saved to: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Qwen2.5-1.5B-Instruct Offline GGUF Inference Engine")
    parser.add_argument("--prompt", type=str, default="Explain what MLOps is in 3 sentences.", help="Input prompt string")
    parser.add_argument("--input", type=str, default="", help="Path to text file containing prompt")
    parser.add_argument("--output", type=str, default="", help="Path to save generated output")
    parser.add_argument("--tokens", type=int, default=256, help="Maximum completion tokens")
    parser.add_argument("--temperature", type=float, default=0.7, help="Sampling temperature")
    args = parser.parse_args()

    main(args.prompt, args.input, args.output, args.tokens, args.temperature)