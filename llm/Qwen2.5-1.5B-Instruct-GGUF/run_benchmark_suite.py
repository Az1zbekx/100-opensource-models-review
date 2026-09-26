import os
import sys
import time
import json
from llama_cpp import Llama

def build_chatml_prompt(user_text: str, system_prompt: str = "You are a helpful, precise, and concise AI assistant.") -> str:
    return (
        f"<|im_start|>system\n{system_prompt}<|im_end|>\n"
        f"<|im_start|>user\n{user_text}<|im_end|>\n"
        f"<|im_start|>assistant\n"
    )

def main():
    data_dir = "data"
    test_files = [
        ("hard_2_algo_amortized.txt", "hard_2_output.txt", 1024, 0.2),
        ("hard_3_logic_knights.txt", "hard_3_output.txt", 1024, 0.2),
        ("hard_4_uzbek_logic_puzzle.txt", "hard_4_output.txt", 1024, 0.2),
        ("olympiad_1_aime_game_theory.txt", "olympiad_1_output.txt", 1024, 0.2),
        ("olympiad_2_aime_logarithms.txt", "olympiad_2_output.txt", 1024, 0.2),
        ("olympiad_3_math_legendre.txt", "olympiad_3_output.txt", 1024, 0.2),
    ]

    print("==========================================================")
    print("  Qwen2.5-1.5B-Instruct-GGUF Benchmark Suite Runner")
    print("==========================================================")
    
    t0 = time.time()
    llm = Llama.from_pretrained(
        repo_id="Qwen/Qwen2.5-1.5B-Instruct-GGUF",
        filename="qwen2.5-1.5b-instruct-q4_k_m.gguf",
        n_ctx=4096,
        n_threads=6,
        verbose=False
    )
    print(f"Model loaded in {time.time() - t0:.2f}s.\n")

    results = []

    for inp_name, out_name, max_tok, temp in test_files:
        inp_path = os.path.join(data_dir, inp_name)
        out_path = os.path.join(data_dir, out_name)
        if not os.path.exists(inp_path):
            print(f"Skipping {inp_name}: file not found.")
            continue
        
        with open(inp_path, "r", encoding="utf-8") as f:
            prompt_text = f.read().strip()
            
        print(f"▶ Running: {inp_name} (max_tokens={max_tok})...")
        formatted = build_chatml_prompt(prompt_text)
        
        start_time = time.time()
        output = llm(
            formatted,
            max_tokens=max_tok,
            temperature=temp,
            stop=["<|im_end|>", "<|endoftext|>"],
            echo=False
        )
        duration = time.time() - start_time
        res_text = output["choices"][0]["text"].strip()
        usage = output.get("usage", {})
        completion_tokens = usage.get("completion_tokens", 0)
        speed = completion_tokens / duration if duration > 0 else 0
        
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(res_text + "\n")
            
        meta = {
            "test": inp_name,
            "duration_s": round(duration, 2),
            "tokens": completion_tokens,
            "speed_tok_s": round(speed, 2),
            "output_file": out_name
        }
        results.append(meta)
        print(f"  ✓ Finished in {duration:.2f}s | {completion_tokens} toks | {speed:.1f} tok/s -> {out_name}\n")

    with open(os.path.join(data_dir, "benchmark_metrics.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("All tests completed successfully. Summary saved to benchmark_metrics.json.")

if __name__ == "__main__":
    main()
