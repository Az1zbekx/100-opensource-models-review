#!/usr/bin/env python3
import os
import sys
import time
import json
import base64
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
from llama_cpp.llama_chat_format import MoondreamChatHandler

def encode_image_to_base64(image_path: str) -> str:
    """Read local image and encode to base64 data URI."""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    ext = os.path.splitext(image_path)[1].lower().replace(".", "")
    if ext == "jpg":
        ext = "jpeg"
    return f"data:image/{ext};base64,{encoded_string}"

def main():
    data_dir = "data"
    test_cases = [
        ("input_1_quick_caption.txt", "test_intersection.jpg", "output_1_quick_caption.txt", 256, 0.2),
        ("input_2_vehicle_color_qa.txt", "test_intersection.jpg", "output_2_vehicle_color_qa.txt", 256, 0.2),
        ("input_3_office_presence.txt", "test_office.jpg", "output_3_office_presence.txt", 256, 0.2),
        ("input_4_uzbek_edge_vqa.txt", "test_office.jpg", "output_4_uzbek_edge_vqa.txt", 256, 0.2),
    ]

    print("==========================================================")
    print("  🌙 Moondream2 Tiny Edge VLM Benchmark Runner")
    print("==========================================================")
    
    model_repo = "moondream/moondream2-gguf"
    model_file = "moondream2-text-model-f16.gguf"
    mmproj_file = "moondream2-mmproj-f16.gguf"

    t0 = time.time()
    print("Downloading/locating model weights and vision projector...")
    model_path = hf_hub_download(repo_id=model_repo, filename=model_file)
    mmproj_path = hf_hub_download(repo_id=model_repo, filename=mmproj_file)

    print("Initializing MoondreamChatHandler and Llama engine...")
    chat_handler = MoondreamChatHandler(clip_model_path=mmproj_path, verbose=False)
    llm = Llama(
        model_path=model_path,
        chat_handler=chat_handler,
        n_ctx=2048,
        n_threads=6,
        verbose=False,
    )
    print(f"Moondream2 loaded successfully in {time.time() - t0:.2f}s.\n")

    results = []

    for inp_name, img_name, out_name, max_tok, temp in test_cases:
        inp_path = os.path.join(data_dir, inp_name)
        img_path = os.path.join(data_dir, img_name)
        out_path = os.path.join(data_dir, out_name)

        if not os.path.exists(inp_path):
            print(f"Skipping {inp_name}: prompt file not found.")
            continue
        if not os.path.exists(img_path):
            print(f"Skipping {inp_name}: image file '{img_name}' not found.")
            continue

        with open(inp_path, "r", encoding="utf-8") as f:
            prompt_text = f.read().strip()

        print(f"▶ Running: {inp_name} with {img_name} (max_tokens={max_tok})...")
        data_uri = encode_image_to_base64(img_path)
        
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": data_uri}},
                    {"type": "text", "text": prompt_text}
                ]
            }
        ]

        start_time = time.time()
        response = llm.create_chat_completion(
            messages=messages,
            max_tokens=max_tok,
            temperature=temp,
            top_p=0.9,
        )
        duration = time.time() - start_time
        res_text = response["choices"][0]["message"]["content"].strip()
        usage = response.get("usage", {})
        completion_tokens = usage.get("completion_tokens", 0)
        speed = completion_tokens / duration if duration > 0 else 0

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(res_text + "\n")

        meta = {
            "test": inp_name,
            "image": img_name,
            "duration_s": round(duration, 2),
            "tokens": completion_tokens,
            "speed_tok_s": round(speed, 2),
            "output_file": out_name
        }
        results.append(meta)
        print(f"  ✓ Finished in {duration:.2f}s | {completion_tokens} toks | {speed:.1f} tok/s -> {out_name}\n")

    with open(os.path.join(data_dir, "benchmark_metrics.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("All Moondream2 tests completed successfully.")

if __name__ == "__main__":
    main()
