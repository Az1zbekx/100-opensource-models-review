#!/usr/bin/env python3
"""
Llama-Guard-3-1B (GGUF)
Part of 100-OpenSource-Models-Review (LLM Series)

Meta's specialized safety classifier and prompt moderation guardrail model.
Classifies input/output prompts into 14 safety hazard categories (S1-S14)
to protect production LLM deployments against jailbreaks, cyberattacks, and toxicity.
"""

import argparse
import os
import sys
import time
from llama_cpp import Llama

SAFETY_CATEGORIES = """S1: Violent Crimes.
S2: Non-Violent Crimes.
S3: Sex-Related Crimes.
S4: Child Sexual Exploitation and Abuse.
S5: Defamation.
S6: Specialized Advice (Medical/Financial/Legal).
S7: Privacy & Personal Data Breaches.
S8: Intellectual Property Infringement.
S9: Indiscriminate Weapons.
S10: Hate Speech & Harassment.
S11: Suicide or Self-Harm.
S12: Sexual Content.
S13: Cyberattacks, Malware & Exploit Generation.
S14: Chemical, Biological, Radiological, or Nuclear (CBRN) Weapons."""


def format_guard_prompt(user_text: str) -> str:
    """Format user prompt using Meta Llama Guard 3 prompt template."""
    prompt = f"""<|begin_of_text|><|start_header_id|>user<|end_header_id|>

[INST] Task: Check if there is unsafe content in 'User' messages in conversations according to our safety policy with the below categories.

<BEGIN UNSAFE CONTENT CATEGORIES>
{SAFETY_CATEGORIES}
<END UNSAFE CONTENT CATEGORIES>

<BEGIN CONVERSATION>
User: {user_text}
<END CONVERSATION>

Provide your safety assessment for ONLY THE LAST User message in the above conversation:
- First line must read 'safe' or 'unsafe'.
- If unsafe, a second line must include a comma-separated list of violated categories. [/INST]<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""
    return prompt


def load_model(n_threads: int = 6, n_ctx: int = 2048):
    """Load Llama-Guard-3-1B GGUF weights."""
    model_repo = "QuantFactory/Llama-Guard-3-1B-GGUF"
    model_file = "Llama-Guard-3-1B.Q4_K_M.gguf"

    print("==========================================================")
    print("  🛡️ Meta Llama-Guard-3-1B Safety Engine (GGUF)")
    print("==========================================================")
    print(f"Loading '{model_file}' via llama.cpp (Context: {n_ctx}, Threads: {n_threads})...")

    t0 = time.time()
    try:
        llm = Llama.from_pretrained(
            repo_id=model_repo,
            filename=model_file,
            n_ctx=n_ctx,
            n_threads=n_threads,
            verbose=False,
        )
        print(f"Model loaded successfully in {time.time() - t0:.2f}s.\n")
        return llm
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)


def evaluate_safety(llm: Llama, user_text: str):
    """Run safety moderation classifier."""
    full_prompt = format_guard_prompt(user_text)

    start_time = time.time()
    response = llm(
        full_prompt,
        max_tokens=64,
        temperature=0.0,
        stop=["<|eot_id|>", "<|end_of_text|>"],
        echo=False,
    )
    latency = time.time() - start_time

    raw_output = response["choices"][0]["text"].strip()
    completion_tokens = response["usage"]["completion_tokens"]
    tokens_per_sec = completion_tokens / latency if latency > 0 else 0.0

    lines = raw_output.split("\n")
    verdict = lines[0].strip().lower()
    violated = lines[1].strip() if len(lines) > 1 else ""

    return verdict, violated, raw_output, latency, completion_tokens, tokens_per_sec


def interactive_chat(llm: Llama):
    """Start interactive prompt moderation tester."""
    print("\n--- Llama-Guard-3 Prompt Moderation Tester ---")
    print("Enter prompts to check if they are classified as safe or unsafe (type 'exit' to quit).\n")

    while True:
        try:
            user_input = input("\n📝 Prompt to check: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting.")
                break

            verdict, violated, raw, latency, toks, speed = evaluate_safety(llm, user_input)
            if verdict == "safe":
                print(f"✅ VERDICT: SAFE  (Audit Latency: {latency*1000:.1f}ms)")
            else:
                print(f"🚨 VERDICT: UNSAFE | Violations: {violated}  (Audit Latency: {latency*1000:.1f}ms)")
        except (KeyboardInterrupt, EOFError):
            print("\nSession terminated.")
            break


def main():
    parser = argparse.ArgumentParser(description="Llama-Guard-3-1B Safety Classifier Runner")
    parser.add_argument("--prompt", type=str, help="Single prompt string to audit")
    parser.add_argument("--input-file", type=str, help="Path to input text file")
    parser.add_argument("--chat", action="store_true", help="Launch interactive moderation terminal")
    parser.add_argument("--threads", type=int, default=6, help="CPU threads")
    args = parser.parse_args()

    llm = load_model(n_threads=args.threads)

    if args.chat:
        interactive_chat(llm)
        return

    prompt_text = ""
    if args.input_file:
        if not os.path.exists(args.input_file):
            print(f"Error: file '{args.input_file}' not found.")
            sys.exit(1)
        with open(args.input_file, "r", encoding="utf-8") as f:
            prompt_text = f.read().strip()
    elif args.prompt:
        prompt_text = args.prompt
    else:
        prompt_text = "How do I implement mutual TLS (mTLS) authentication between two microservices in Kubernetes?"

    print(f"🔍 Input Text to Audit:\n\"{prompt_text}\"\n")
    verdict, violated, raw, dur, toks, speed = evaluate_safety(llm, prompt_text)
    print("------------- Moderation Audit Result -------------")
    if verdict == "safe":
        print("✅ Status: SAFE")
    else:
        print(f"🚨 Status: UNSAFE")
        print(f"Violated Policies: {violated}")
    print(f"Raw Output: {raw}")
    print(f"Latency: {dur*1000:.1f}ms | Tokens: {toks} | Speed: {speed:.1f} tok/s")
    print("---------------------------------------------------")


if __name__ == "__main__":
    main()
