#!/usr/bin/env python3
"""
BGE-M3 (BAAI General Embedding - Multi-Lingual, Multi-Functionality, Multi-Granularity)
Part of 100-OpenSource-Models-Review (LLM / RAG Series)

World SOTA multilingual semantic embedding model.
1024-dimensional vector embeddings, 8192 token context window, 100+ languages (Uzbek, Russian, English).
Calculates dense semantic representations and cosine similarity rankings for high-accuracy RAG.
"""

import argparse
import os
import sys
import time
import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer


def load_model():
    """Load BGE-M3 model and tokenizer."""
    model_name = "BAAI/bge-m3"
    print("==========================================================")
    print("  🌐 BGE-M3 Multilingual Semantic Embedding Engine")
    print("==========================================================")
    print(f"Loading '{model_name}' on CPU...")

    t0 = time.time()
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)
        model.eval()
        print(f"Model loaded successfully in {time.time() - t0:.2f}s.\n")
        return tokenizer, model
    except Exception as e:
        print(f"Error loading BGE-M3: {e}")
        sys.exit(1)


def get_embeddings(texts: list, tokenizer, model, max_length: int = 8192):
    """Compute normalized dense embeddings for list of texts."""
    inputs = tokenizer(
        texts,
        padding=True,
        truncation=True,
        max_length=max_length,
        return_tensors="pt",
    )
    with torch.no_grad():
        outputs = model(**inputs)
        # BGE-M3 uses CLS token [:, 0] as dense representation
        embeddings = outputs.last_hidden_state[:, 0]
        # L2 Normalize
        embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
    return embeddings.cpu().numpy()


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Compute cosine similarity matrix."""
    return np.dot(a, b.T)


def interactive_session(tokenizer, model):
    """Interactive semantic similarity search."""
    print("\n--- BGE-M3 Interactive Semantic Retrieval Session ---")
    print("Compare semantic similarity between any query and candidate sentences.")

    docs = [
        "Kubernetes container pods are automatically scheduled across cluster nodes.",
        "O'zbekistonda raqamli iqtisodiyot va IT xizmatlari jadal rivojlanmoqda.",
        "PostgreSQL relational database handles ACID transactions with MVCC concurrency.",
        "Bugun Toshkentda havo quyoshli va iliq bo'lishi kutilmoqda.",
    ]
    print("\nInitial Knowledge Base:")
    for idx, d in enumerate(docs, 1):
        print(f"  [{idx}] {d}")

    while True:
        try:
            query = input("\n🔍 Enter search query (or 'exit' to quit): ").strip()
            if not query:
                continue
            if query.lower() in ["exit", "quit"]:
                print("Exiting.")
                break

            t0 = time.time()
            all_texts = [query] + docs
            embs = get_embeddings(all_texts, tokenizer, model)
            elapsed = time.time() - t0

            q_emb = embs[0:1]
            doc_embs = embs[1:]
            scores = cosine_similarity(q_emb, doc_embs)[0]

            ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
            print(f"\n🏆 Semantic Match Results (Latency: {elapsed*1000:.1f}ms):")
            for doc, score in ranked:
                bar = "█" * int(score * 20)
                print(f"  Score: {score:.4f} | {bar:<20} | {doc}")
        except (KeyboardInterrupt, EOFError):
            print("\nSession terminated.")
            break


def main():
    parser = argparse.ArgumentParser(description="BGE-M3 Multilingual Embedding Runner")
    parser.add_argument("--query", type=str, help="Search query")
    parser.add_argument("--candidates", nargs="+", help="Candidate documents to rank")
    parser.add_argument("--input-file", type=str, help="File containing queries / sentences to embed")
    parser.add_argument("--chat", action="store_true", help="Launch interactive semantic matcher")
    args = parser.parse_args()

    tokenizer, model = load_model()

    if args.chat:
        interactive_session(tokenizer, model)
        return

    if args.query and args.candidates:
        all_texts = [args.query] + args.candidates
        t0 = time.time()
        embs = get_embeddings(all_texts, tokenizer, model)
        elapsed = time.time() - t0

        scores = cosine_similarity(embs[0:1], embs[1:])[0]
        ranked = sorted(zip(args.candidates, scores), key=lambda x: x[1], reverse=True)

        print(f"Query: \"{args.query}\"")
        print(f"Embedding Latency: {elapsed*1000:.1f}ms\n")
        print("Ranked Matches:")
        for doc, sc in ranked:
            print(f"  [{sc:.4f}] {doc}")
        return

    # Default evaluation test
    sentences = [
        "Sun'iy intellekt va mashinali o'rganish texnologiyalari.",
        "Artificial intelligence and deep machine learning algorithms.",
        "Bugun tushlikka nima ovqat pishiramiz?",
        "PostgreSQL ma'lumotlar bazasi indekslari va tranzaksiyalari.",
    ]
    print("Testing Cross-Lingual Semantic Similarity Matrix:")
    for idx, s in enumerate(sentences, 1):
        print(f"  [{idx}] {s}")

    t0 = time.time()
    embs = get_embeddings(sentences, tokenizer, model)
    elapsed = time.time() - t0
    matrix = cosine_similarity(embs, embs)

    print(f"\nEmbedding Matrix Computed in {elapsed*1000:.1f}ms:")
    print(f"Vector Dimensions: {embs.shape[1]}")
    print("\nCosine Similarity Matrix:")
    header = "      " + " ".join([f"[{i+1}]   " for i in range(len(sentences))])
    print(header)
    for i, row in enumerate(matrix):
        row_str = f"[{i+1}]   " + " ".join([f"{val:.3f} " for val in row])
        print(row_str)

    print("\nNotice high similarity between [1] (Uzbek AI) and [2] (English AI) despite different languages!")


if __name__ == "__main__":
    main()
