#!/usr/bin/env python3
import os
import sys
import time
import json
from llama_cpp import Llama

def main():
    data_dir = "data"
    test_files = [
        ("input_2_binary_search_tree.txt", "output_2_binary_search_tree.txt", 512, 0.2),
        ("input_3_sql_joins.txt", "output_3_sql_joins.txt", 512, 0.2),
        ("input_4_uzbek_function.txt", "output_4_uzbek_function.txt", 512, 0.2),
    ]

    print("==========================================================")
    print("  StarCoder2-3B Benchmark Runner")
    print("==========================================================")
    
    t0 = time.time()
    llm = Llama.from_pretrained(
        repo_id="second-state/StarCoder2-3B-GGUF",
        filename="starcoder2-3b-Q4_K_M.gguf",
        n_ctx=2048,
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
        
        start_time = time.time()
        output = llm(
            prompt_text,
            max_tokens=max_tok,
            temperature=temp,
            top_p=0.9,
            stop=["<|endoftext|>", "<file_sep>"],
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
    print("All tests completed successfully.")

if __name__ == "__main__":
    main()
