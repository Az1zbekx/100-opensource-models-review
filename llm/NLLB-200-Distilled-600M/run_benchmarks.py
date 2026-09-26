#!/usr/bin/env python3
import os
import sys
import time
import json
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

LANGUAGES = {
    "uz_latn": "uzn_Latn",
    "uz_cyrl": "uzn_Cyrl",
    "en": "eng_Latn",
    "ru": "rus_Cyrl",
}

def load_nllb():
    model_name = "facebook/nllb-200-distilled-600M"
    print("==========================================================")
    print("  🌍 Meta NLLB-200 Machine Translation Benchmark Suite")
    print("==========================================================")
    print(f"Loading '{model_name}' on CPU...")
    t0 = time.time()
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    model.eval()
    print(f"NLLB-200 loaded in {time.time() - t0:.2f}s.\n")
    return tokenizer, model

def translate(text: str, src_code: str, tgt_code: str, tokenizer, model, max_length: int = 512):
    tokenizer.src_lang = src_code
    inputs = tokenizer(text, return_tensors="pt", max_length=max_length, truncation=True)
    forced_bos_token_id = tokenizer.convert_tokens_to_ids(tgt_code)

    t0 = time.time()
    with torch.no_grad():
        generated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=forced_bos_token_id,
            max_length=max_length,
            num_beams=4,
            early_stopping=True,
        )
    latency = time.time() - t0
    result = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    tok_count = len(generated_tokens[0])
    speed = tok_count / latency if latency > 0 else 0
    return result, latency, tok_count, speed

def main():
    data_dir = "data"
    test_cases = [
        ("input_1_uzb_to_eng.txt", "uzn_Latn", "eng_Latn", "output_1_uzb_to_eng.txt"),
        ("input_2_eng_to_uzb.txt", "eng_Latn", "uzn_Latn", "output_2_eng_to_uzb.txt"),
        ("input_3_rus_to_uzb.txt", "rus_Cyrl", "uzn_Latn", "output_3_rus_to_uzb.txt"),
        ("input_4_uzb_cyrl_to_latn.txt", "uzn_Cyrl", "uzn_Latn", "output_4_uzb_cyrl_to_latn.txt"),
    ]

    tokenizer, model = load_nllb()
    results = []

    for inp_name, src_code, tgt_code, out_name in test_cases:
        inp_path = os.path.join(data_dir, inp_name)
        out_path = os.path.join(data_dir, out_name)

        if not os.path.exists(inp_path):
            print(f"Skipping {inp_name}: file not found.")
            continue

        with open(inp_path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        print(f"▶ Running {inp_name} [{src_code} -> {tgt_code}]...")
        res, dur, toks, speed = translate(text, src_code, tgt_code, tokenizer, model)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"Source [{src_code}]:\n{text}\n\nTranslation [{tgt_code}]:\n{res}\n")

        meta = {
            "test": inp_name,
            "src_lang": src_code,
            "tgt_lang": tgt_code,
            "duration_s": round(dur, 2),
            "tokens": toks,
            "speed_tok_s": round(speed, 2),
            "output_file": out_name
        }
        results.append(meta)
        print(f"  ✓ Finished in {dur:.2f}s | {toks} toks | {speed:.1f} tok/s -> {out_name}\n")

    with open(os.path.join(data_dir, "benchmark_metrics.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("All NLLB-200 tests completed successfully.")

if __name__ == "__main__":
    main()
