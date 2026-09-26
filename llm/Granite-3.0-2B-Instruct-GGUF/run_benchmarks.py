#!/usr/bin/env python3
import os
import sys
import time
import json
from llama_cpp import Llama

def format_granite_prompt(user_text: str, system_prompt: str = "You are Granite, an AI model developed by IBM. You are a helpful, respectful, and honest assistant specialized in enterprise architecture, compliance, and systems engineering.") -> str:
    prompt = f"<|start_of_role|>system<|end_of_role|>{system_prompt}<|end_of_text|>\n"
    prompt += f"<|start_of_role|>user<|end_of_role|>{user_text}<|end_of_text|>\n"
    prompt += "<|start_of_role|>assistant<|end_of_role|>"
    return prompt

def main():
    data_dir = "data"
    test_files = [
        ("input_1_architecture_summary.txt", "output_1_architecture_summary.txt", 1024, 0.2),
        ("input_2_uzbek_comprehension.txt", "output_2_uzbek_comprehension.txt", 600, 0.2),
        ("input_3_logic_deduction.txt", "output_3_logic_deduction.txt", 800, 0.1),
        ("input_4_sql_rbac_policy.txt", "output_4_sql_rbac_policy.txt", 1024, 0.2),
    ]

    print("==========================================================")
    print("  🔷 IBM Granite-3.0-2B Benchmark Suite Runner")
    print("==========================================================")
    
    t0 = time.time()
    llm = Llama.from_pretrained(
        repo_id="bartowski/granite-3.0-2b-instruct-GGUF",
        filename="granite-3.0-2b-instruct-Q4_K_M.gguf",
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
        formatted = format_granite_prompt(prompt_text)
        
        start_time = time.time()
        output = llm(
            formatted,
            max_tokens=max_tok,
            temperature=temp,
            top_p=0.9,
            stop=["<|end_of_text|>"],
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
    print("All Granite-3.0-2B tests completed successfully.")

if __name__ == "__main__":
    main()
