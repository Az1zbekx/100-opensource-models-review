#!/usr/bin/env python3
import os
import sys
import time
import json
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

def load_reranker():
    model_name = "BAAI/bge-reranker-v2-m3"
    print("==========================================================")
    print("  🎯 BGE-Reranker-v2-M3 Cross-Encoder Benchmark Suite")
    print("==========================================================")
    print(f"Loading '{model_name}' on CPU...")
    t0 = time.time()
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    model.eval()
    print(f"Reranker loaded in {time.time() - t0:.2f}s.\n")
    return tokenizer, model

def compute_rerank_scores(query: str, passages: list, tokenizer, model, max_length: int = 4096):
    pairs = [[query, p] for p in passages]
    inputs = tokenizer(
        pairs,
        padding=True,
        truncation=True,
        max_length=max_length,
        return_tensors="pt",
    )
    with torch.no_grad():
        logits = model(**inputs, return_dict=True).logits.view(-1).float()
        scores = torch.sigmoid(logits).cpu().numpy().tolist()
    return scores

def main():
    data_dir = "data"
    tokenizer, model = load_reranker()
    results = []

    # Test 1: Hard Negatives (Python KeyError)
    print("▶ Running Test 1: Hard Negatives (Python KeyError)...")
    q1 = "How to fix a Python KeyError when accessing a dictionary?"
    cands1 = [
        "To avoid KeyError in Python, use the .get(key, default) method or check if 'key in my_dict' before accessing.",
        "In Python, a ValueError is raised when an operation receives an argument that has the right type but an inappropriate value.",
        "A dictionary in Python is an unordered collection of data values used to store data values like a map.",
        "To generate cryptographic keys in Python, use the cryptography library's Fernet module."
    ]
    t0 = time.time()
    scores1 = compute_rerank_scores(q1, cands1, tokenizer, model)
    dur1 = time.time() - t0
    ranked1 = sorted(zip(cands1, scores1), key=lambda x: x[1], reverse=True)
    out1_lines = [f"Query: {q1}", f"Latency: {dur1*1000:.1f}ms", "Ranked Candidates:"]
    for c, sc in ranked1:
        out1_lines.append(f"  [{sc*100:5.2f}%] {c}")
    with open(os.path.join(data_dir, "output_1_hard_negatives.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(out1_lines) + "\n")
    results.append({
        "test": "input_1_hard_negatives.txt",
        "duration_s": round(dur1, 2),
        "top_score_pct": round(ranked1[0][1]*100, 2),
        "top_correct": (ranked1[0][0] == cands1[0]),
        "output_file": "output_1_hard_negatives.txt"
    })
    print(f"  ✓ Finished in {dur1:.2f}s | Top: {ranked1[0][1]*100:.1f}% -> {ranked1[0][0][:45]}...\n")

    # Test 2: Multilingual Uzbek LLC Charter Capital
    print("▶ Running Test 2: Multilingual Uzbek Corporate Legal Rerank...")
    q2 = "O'zbekistonda MChJ ustav fondining minimal miqdori qancha?"
    cands2 = [
        "O'zbekiston Respublikasining 'Mas'uliyati cheklangan hamda qo'shimcha mas'uliyatli jamiyatlar to'g'risida'gi Qonuniga muvofiq, MChJ ustav fondining eng kam miqdori ta'sischilar tomonidan belgilanadi va qonunchilikda unga minimal chegara talab etilmaydi.",
        "Aksiyadorlik jamiyatlari (AJ) uchun ustav kapitalining minimal miqdori bazaviy hisoblash miqdorining 400 baravaridan kam bo'lmasligi lozim.",
        "Для регистрации индивидуального предпринимателя в Узбекистане необходимо подать заявление через портал интерактивных государственных услуг."
    ]
    t0 = time.time()
    scores2 = compute_rerank_scores(q2, cands2, tokenizer, model)
    dur2 = time.time() - t0
    ranked2 = sorted(zip(cands2, scores2), key=lambda x: x[1], reverse=True)
    out2_lines = [f"Query: {q2}", f"Latency: {dur2*1000:.1f}ms", "Ranked Candidates:"]
    for c, sc in ranked2:
        out2_lines.append(f"  [{sc*100:5.2f}%] {c}")
    with open(os.path.join(data_dir, "output_2_multilingual_rerank.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(out2_lines) + "\n")
    results.append({
        "test": "input_2_multilingual_rerank.txt",
        "duration_s": round(dur2, 2),
        "top_score_pct": round(ranked2[0][1]*100, 2),
        "top_correct": (ranked2[0][0] == cands2[0]),
        "output_file": "output_2_multilingual_rerank.txt"
    })
    print(f"  ✓ Finished in {dur2:.2f}s | Top: {ranked2[0][1]*100:.1f}% -> {ranked2[0][0][:45]}...\n")

    # Test 3: Code Documentation (Async Stream JSON)
    print("▶ Running Test 3: Code Documentation Rerank...")
    q3 = "How to parse JSON in Node.js asynchronously from a file stream?"
    cands3 = [
        "Use stream-json or JSONStream packages in Node.js to pipe a fs.createReadStream into a parser to handle multi-gigabyte JSON files without memory bloat.",
        "In Python, use json.loads() or json.load() to deserialize JSON formatted strings or file pointers.",
        "JSON.stringify() converts a JavaScript object into a JSON string synchronously."
    ]
    t0 = time.time()
    scores3 = compute_rerank_scores(q3, cands3, tokenizer, model)
    dur3 = time.time() - t0
    ranked3 = sorted(zip(cands3, scores3), key=lambda x: x[1], reverse=True)
    out3_lines = [f"Query: {q3}", f"Latency: {dur3*1000:.1f}ms", "Ranked Candidates:"]
    for c, sc in ranked3:
        out3_lines.append(f"  [{sc*100:5.2f}%] {c}")
    with open(os.path.join(data_dir, "output_3_code_doc_rerank.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(out3_lines) + "\n")
    results.append({
        "test": "input_3_code_doc_rerank.txt",
        "duration_s": round(dur3, 2),
        "top_score_pct": round(ranked3[0][1]*100, 2),
        "top_correct": (ranked3[0][0] == cands3[0]),
        "output_file": "output_3_code_doc_rerank.txt"
    })
    print(f"  ✓ Finished in {dur3:.2f}s | Top: {ranked3[0][1]*100:.1f}% -> {ranked3[0][0][:45]}...\n")

    # Test 4: Adversarial Semantic Polarity (Profit vs Loss)
    print("▶ Running Test 4: Adversarial Semantic Polarity...")
    q4 = "Did the company make a financial profit and positive earnings this quarter?"
    cands4 = [
        "The company reported record quarterly net revenue and strong net profitability of 10 million dollars.",
        "The company reported a devastating quarterly net loss of 10 million dollars and negative operational cash flow.",
        "The company announced a new office opening in Berlin with 50 new software engineering hires.",
        "PostgreSQL database vacuuming recovers dead tuples to optimize table storage."
    ]
    t0 = time.time()
    scores4 = compute_rerank_scores(q4, cands4, tokenizer, model)
    dur4 = time.time() - t0
    ranked4 = sorted(zip(cands4, scores4), key=lambda x: x[1], reverse=True)
    out4_lines = [f"Query: {q4}", f"Latency: {dur4*1000:.1f}ms", "Ranked Candidates:"]
    for c, sc in ranked4:
        out4_lines.append(f"  [{sc*100:5.2f}%] {c}")
    with open(os.path.join(data_dir, "output_4_adversarial_semantic_trap.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(out4_lines) + "\n")
    results.append({
        "test": "input_4_adversarial_semantic_trap.txt",
        "duration_s": round(dur4, 2),
        "positive_score_pct": round(scores4[0]*100, 2),
        "loss_negative_score_pct": round(scores4[1]*100, 2),
        "margin_delta_pct": round((scores4[0] - scores4[1])*100, 2),
        "top_correct": (ranked4[0][0] == cands4[0]),
        "output_file": "output_4_adversarial_semantic_trap.txt"
    })
    print(f"  ✓ Finished in {dur4:.2f}s | Profit: {scores4[0]*100:.1f}% vs Loss: {scores4[1]*100:.1f}% (Margin: {(scores4[0]-scores4[1])*100:.1f}%)\n")

    with open(os.path.join(data_dir, "benchmark_metrics.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("All BGE-Reranker-v2-M3 tests completed successfully.")

if __name__ == "__main__":
    main()
