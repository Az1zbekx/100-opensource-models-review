#!/usr/bin/env python3
import os
import sys
import time
import json
from llama_cpp import Llama

def format_hermes_prompt(user_text: str, system_prompt: str = "You are Hermes 3, an advanced autonomous AI assistant capable of structured function calling, JSON schema compliance, and complex agent reasoning.") -> str:
    prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n"
    prompt += f"<|im_start|>user\n{user_text}<|im_end|>\n"
    prompt += "<|im_start|>assistant\n"
    return prompt

def main():
    data_dir = "data"
    test_files = [
        ("input_1_tool_calling.txt", "output_1_tool_calling.txt", 1024, 0.2),
        ("input_2_json_schema.txt", "output_2_json_schema.txt", 1024, 0.1),
        ("input_3_agent_reasoning.txt", "output_3_agent_reasoning.txt", 1024, 0.2),
        ("input_4_uzbek_agent.txt", "output_4_uzbek_agent.txt", 1024, 0.2),
    ]

    print("==========================================================")
    print("  Hermes-3-Llama-3.2-3B Agent Benchmark Runner")
    print("==========================================================")
    
    t0 = time.time()
    llm = Llama.from_pretrained(
        repo_id="NousResearch/Hermes-3-Llama-3.2-3B-GGUF",
        filename="Hermes-3-Llama-3.2-3B.Q4_K_M.gguf",
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
        formatted = format_hermes_prompt(prompt_text)
        
        start_time = time.time()
        output = llm(
            formatted,
            max_tokens=max_tok,
            temperature=temp,
            top_p=0.9,
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
    print("All Hermes-3 tests completed successfully.")

if __name__ == "__main__":
    main()
