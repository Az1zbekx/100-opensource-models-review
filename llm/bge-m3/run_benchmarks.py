#!/usr/bin/env python3
import os
import sys
import time
import json
import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer

def load_bge():
    model_name = "BAAI/bge-m3"
    print("==========================================================")
    print("  🌐 BGE-M3 Multilingual Embedding Benchmark Suite")
    print("==========================================================")
    print(f"Loading '{model_name}' on CPU...")
    t0 = time.time()
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    model.eval()
    print(f"BGE-M3 loaded in {time.time() - t0:.2f}s.\n")
    return tokenizer, model

def get_embeddings(texts: list, tokenizer, model, max_length: int = 8192):
    inputs = tokenizer(
        texts,
        padding=True,
        truncation=True,
        max_length=max_length,
        return_tensors="pt",
    )
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state[:, 0]
        embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
    return embeddings.cpu().numpy()

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.dot(a, b.T)

def main():
    data_dir = "data"
    tokenizer, model = load_bge()
    results = []

    # Test 1: Cross-lingual Uzbek to English
    print("▶ Running Test 1: Cross-lingual Search (Uzbek -> English)...")
    q1 = "Taqsimlangan tranzaksiyalarda ACID xususiyatlari qanday ta'minlanadi?"
    targets1 = [
        "Distributed transactions utilize the Two-Phase Commit (2PC) protocol and Paxos consensus to ensure atomicity and consistency across database shards.",
        "CSS Flexbox and Grid layouts enable responsive web design across modern mobile browsers.",
        "Python list comprehensions provide a concise way to create new lists from existing iterables."
    ]
    t0 = time.time()
    embs1 = get_embeddings([q1] + targets1, tokenizer, model)
    scores1 = cosine_similarity(embs1[0:1], embs1[1:])[0]
    dur1 = time.time() - t0
    
    ranking1 = sorted(zip(targets1, scores1), key=lambda x: x[1], reverse=True)
    out1_lines = [f"Query: {q1}", f"Latency: {dur1*1000:.1f}ms", "Rankings:"]
    for t, s in ranking1:
        out1_lines.append(f"  [{s:.4f}] {t}")
    with open(os.path.join(data_dir, "output_1_crosslingual_search.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(out1_lines) + "\n")
    results.append({
        "test": "input_1_crosslingual_search.txt",
        "duration_s": round(dur1, 2),
        "top_match_score": round(float(ranking1[0][1]), 4),
        "top_match_correct": (ranking1[0][0] == targets1[0]),
        "output_file": "output_1_crosslingual_search.txt"
    })
    print(f"  ✓ Finished in {dur1:.2f}s | Top score: {ranking1[0][1]:.4f} (Correct: {ranking1[0][0] == targets1[0]})\n")

    # Test 2: Long Context Embedding
    print("▶ Running Test 2: Long Context Document Embedding...")
    with open(os.path.join(data_dir, "input_2_long_context_doc.txt"), "r", encoding="utf-8") as f:
        doc2 = f.read().strip()
    t0 = time.time()
    embs2 = get_embeddings([doc2], tokenizer, model)
    dur2 = time.time() - t0
    norm2 = float(np.linalg.norm(embs2[0]))
    dim2 = int(embs2.shape[1])
    out2 = f"Document Length: {len(doc2)} characters\nVector Dimensions: {dim2}\nL2 Norm: {norm2:.4f}\nLatency: {dur2*1000:.1f}ms\nFirst 10 dimensions: {embs2[0][:10].tolist()}"
    with open(os.path.join(data_dir, "output_2_long_context_doc.txt"), "w", encoding="utf-8") as f:
        f.write(out2 + "\n")
    results.append({
        "test": "input_2_long_context_doc.txt",
        "duration_s": round(dur2, 2),
        "vector_dim": dim2,
        "l2_norm": round(norm2, 4),
        "output_file": "output_2_long_context_doc.txt"
    })
    print(f"  ✓ Finished in {dur2:.2f}s | Dim: {dim2} | Norm: {norm2:.4f}\n")

    # Test 3: Fine-grained Distinction (Semantic Opposition)
    print("▶ Running Test 3: Fine-grained Distinction...")
    pair_a = [
        "The company reported record quarterly net revenue of 10 million dollars.",
        "The company reported a devastating quarterly net loss of 10 million dollars."
    ]
    pair_b = [
        "User authentication succeeded and an access token was generated.",
        "User authentication failed and an access denied error was logged."
    ]
    t0 = time.time()
    embs3_a = get_embeddings(pair_a, tokenizer, model)
    embs3_b = get_embeddings(pair_b, tokenizer, model)
    sim_a = float(cosine_similarity(embs3_a[0:1], embs3_a[1:2])[0][0])
    sim_b = float(cosine_similarity(embs3_b[0:1], embs3_b[1:2])[0][0])
    dur3 = time.time() - t0
    out3 = f"Pair A (Revenue vs Loss):\n  Sentence 1: {pair_a[0]}\n  Sentence 2: {pair_a[1]}\n  Similarity: {sim_a:.4f}\n\nPair B (Auth Success vs Failure):\n  Sentence 1: {pair_b[0]}\n  Sentence 2: {pair_b[1]}\n  Similarity: {sim_b:.4f}"
    with open(os.path.join(data_dir, "output_3_fine_grained_distinction.txt"), "w", encoding="utf-8") as f:
        f.write(out3 + "\n")
    results.append({
        "test": "input_3_fine_grained_distinction.txt",
        "duration_s": round(dur3, 2),
        "pair_a_similarity": round(sim_a, 4),
        "pair_b_similarity": round(sim_b, 4),
        "output_file": "output_3_fine_grained_distinction.txt"
    })
    print(f"  ✓ Finished in {dur3:.2f}s | Pair A Sim: {sim_a:.4f} | Pair B Sim: {sim_b:.4f}\n")

    # Test 4: Uzbek Legal Clause Retrieval
    print("▶ Running Test 4: Uzbek Legal Clause Retrieval...")
    q4 = "Mehnat shartnomasini xodimning tashabbusi bilan bekor qilish tartibi va muddatlari qanday?"
    targets4 = [
        "Xodim noaniq muddatli mehnat shartnomasini, shuningdek muddati tugashidan oldin muddatli mehnat shartnomasini ikki hafta oldin ish beruvchini yozma ravishda ogohlantirib bekor qilishga haqli.",
        "Xodimlarga yillik asosiy mehnat ta'tili davomiyligi kamida yigirma bir kalendar kundan iborat bo'lishi kafolatlanadi.",
        "Dasturchilar masofadan ishlash rejimida Git orqali kodlarni doimiy ravishda pull request qilib tekshiruvdan o'tkazishlari lozim.",
        "Ish beruvchi xodimga ish haqini har yarim oyda kamida bir marta to'lashi shart, kechiktirilgan har bir kun uchun kompensatsiya to'lanadi."
    ]
    t0 = time.time()
    embs4 = get_embeddings([q4] + targets4, tokenizer, model)
    scores4 = cosine_similarity(embs4[0:1], embs4[1:])[0]
    dur4 = time.time() - t0
    ranking4 = sorted(zip(targets4, scores4), key=lambda x: x[1], reverse=True)
    out4_lines = [f"Query: {q4}", f"Latency: {dur4*1000:.1f}ms", "Rankings:"]
    for t, s in ranking4:
        out4_lines.append(f"  [{s:.4f}] {t}")
    with open(os.path.join(data_dir, "output_4_uzbek_law_retrieval.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(out4_lines) + "\n")
    results.append({
        "test": "input_4_uzbek_law_retrieval.txt",
        "duration_s": round(dur4, 2),
        "top_match_score": round(float(ranking4[0][1]), 4),
        "top_match_correct": (ranking4[0][0] == targets4[0]),
        "output_file": "output_4_uzbek_law_retrieval.txt"
    })
    print(f"  ✓ Finished in {dur4:.2f}s | Top score: {ranking4[0][1]:.4f} (Correct: {ranking4[0][0] == targets4[0]})\n")

    with open(os.path.join(data_dir, "benchmark_metrics.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("All BGE-M3 tests completed successfully.")

if __name__ == "__main__":
    main()
