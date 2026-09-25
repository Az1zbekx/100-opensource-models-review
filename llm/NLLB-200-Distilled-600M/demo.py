#!/usr/bin/env python3
"""
NLLB-200-Distilled-600M (No Language Left Behind)
Part of 100-OpenSource-Models-Review (LLM / NLP Series)

Meta's 200-Language Neural Machine Translation Model.
Native support for Uzbek (uzn_Latn / uzn_Cyrl), Russian (rus_Cyrl), English (eng_Latn), Turkish, etc.
Direct language-pair translation without English as an intermediate pivot.
Lightweight distilled architecture (600M parameters) running swiftly on CPU.
"""

import argparse
import os
import sys
import time
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

LANGUAGES = {
    "uz_latn": "uzn_Latn",
    "uz_cyrl": "uzn_Cyrl",
    "en": "eng_Latn",
    "ru": "rus_Cyrl",
    "tr": "tur_Latn",
    "de": "deu_Latn",
    "fr": "fra_Latn",
    "zh": "zho_Hans",
    "ar": "arb_Arab",
}


def load_model():
    """Load NLLB-200 distilled 600M model and tokenizer."""
    model_name = "facebook/nllb-200-distilled-600M"
    print("==========================================================")
    print("  🌍 Meta NLLB-200 Machine Translation Engine (600M)")
    print("==========================================================")
    print(f"Loading '{model_name}' on CPU...")

    t0 = time.time()
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        model.eval()
        print(f"Model loaded successfully in {time.time() - t0:.2f}s.\n")
        return tokenizer, model
    except Exception as e:
        print(f"Error loading NLLB-200: {e}")
        sys.exit(1)


def translate(text: str, src_lang: str, tgt_lang: str, tokenizer, model, max_length: int = 512):
    """Translate text between source and target language codes."""
    src_code = LANGUAGES.get(src_lang.lower(), src_lang)
    tgt_code = LANGUAGES.get(tgt_lang.lower(), tgt_lang)

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


def interactive_session(tokenizer, model):
    """Interactive multi-language translation console."""
    print("\n--- NLLB-200 Interactive Translation Console ---")
    print("Available shortcuts: uz_latn, uz_cyrl, en, ru, tr, de, fr, zh, ar")
    print("Format: <src_lang> <tgt_lang> <text> (e.g. 'uz_latn en Salom, dunyo!')")
    print("Or type 'exit' to terminate.\n")

    while True:
        try:
            line = input("\n🌐 [src tgt text]: ").strip()
            if not line:
                continue
            if line.lower() in ["exit", "quit"]:
                print("Exiting.")
                break

            parts = line.split(" ", 2)
            if len(parts) < 3:
                print("Format error. Usage: <src_lang> <tgt_lang> <text>")
                continue

            src, tgt, txt = parts[0], parts[1], parts[2]
            res, dur, toks, speed = translate(txt, src, tgt, tokenizer, model)
            print(f"\n✅ [{tgt}]: {res}")
            print(f"[⏱️ {dur*1000:.1f}ms | ⚡ {speed:.1f} tok/s | 🔢 {toks} tokens]")
        except (KeyboardInterrupt, EOFError):
            print("\nSession terminated.")
            break


def main():
    parser = argparse.ArgumentParser(description="NLLB-200-Distilled-600M Translation Runner")
    parser.add_argument("--text", type=str, help="Source text to translate")
    parser.add_argument("--src", type=str, default="uz_latn", help="Source language code (default: uz_latn)")
    parser.add_argument("--tgt", type=str, default="en", help="Target language code (default: en)")
    parser.add_argument("--input-file", type=str, help="Path to input text file")
    parser.add_argument("--chat", action="store_true", help="Launch interactive translation session")
    args = parser.parse_args()

    tokenizer, model = load_model()

    if args.chat:
        interactive_session(tokenizer, model)
        return

    text = ""
    if args.input_file:
        if not os.path.exists(args.input_file):
            print(f"Error: file '{args.input_file}' not found.")
            sys.exit(1)
        with open(args.input_file, "r", encoding="utf-8") as f:
            text = f.read().strip()
    elif args.text:
        text = args.text
    else:
        text = "Sun'iy intellekt texnologiyalari O'zbekistonda yangi ish o'rinlari va innovatsiyalarni yaratishda muhim o'rin tutadi."

    print(f"Source ({args.src}): \"{text}\"")
    print(f"Target Language: {args.tgt}")
    print("⏳ Translating...")
    res, dur, toks, speed = translate(text, args.src, args.tgt, tokenizer, model)
    print("\n---------------- Translation ----------------")
    print(res)
    print("---------------------------------------------")
    print(f"Time: {dur*1000:.1f}ms | Tokens: {toks} | Speed: {speed:.1f} tok/s")


if __name__ == "__main__":
    main()
