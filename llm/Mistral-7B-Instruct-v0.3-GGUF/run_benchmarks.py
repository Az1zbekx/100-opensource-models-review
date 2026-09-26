#!/usr/bin/env python3
import os
import sys
import time
import json
from llama_cpp import Llama

def format_mistral_prompt(user_text: str, system_prompt: str = "You are an expert software architect and systems engineer. Provide direct, highly technical, and production-grade answers without fluff.") -> str:
    prompt = "<s>[INST] "
    if system_prompt:
        prompt += f"{system_prompt}\n\n"
    prompt += f"{user_text} [/INST]"
    return prompt

def main():
    data_dir = "data"
    test_files = [
        ("input_1_system_architecture.txt", "output_1_system_architecture.txt", 1200, 0.2),
        ("input_2_french_english_technical.txt", "output_2_french_english_technical.txt", 600, 0.1),
        ("input_3_sql_optimization.txt", "output_3_sql_optimization.txt", 1200, 0.2),
        ("input_4_uzbek_distributed_saga.txt", "output_4_uzbek_distributed_saga.txt", 1500, 0.2),
    ]

    print("==========================================================")
    print("  🌪️ Mistral-7B-Instruct-v0.3 Benchmark Suite Runner")
    print("==========================================================")
    
    t0 = time.time()
    llm = Llama.from_pretrained(
        repo_id="bartowski/Mistral-7B-Instruct-v0.3-GGUF",
        filename="Mistral-7B-Instruct-v0.3-Q4_K_M.gguf",
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
        formatted = format_mistral_prompt(prompt_text)
        
        start_time = time.time()
        output = llm(
            formatted,
            max_tokens=max_tok,
            temperature=temp,
            top_p=0.9,
            stop=["</s>", "[INST]"],
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
    print("All Mistral-7B tests completed successfully.")

if __name__ == "__main__":
    main()
