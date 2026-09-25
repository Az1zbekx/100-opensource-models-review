#!/usr/bin/env python3
"""
BGE-Reranker-v2-M3 (BAAI Cross-Encoder Reranker)
Part of 100-OpenSource-Models-Review (LLM / RAG Series)

Cross-encoder architecture for ultra-high-precision RAG reranking.
Performs full cross-attention between search queries and candidate passages.
Re-ranks bi-encoder top-k candidates, filtering false positives and ranking true relevant answers at position 1.
"""

import argparse
import os
import sys
import time
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def load_model():
    """Load BGE-Reranker-v2-M3 model and tokenizer."""
    model_name = "BAAI/bge-reranker-v2-m3"
    print("==========================================================")
    print("  🎯 BGE-Reranker-v2-M3 Cross-Encoder Reranker Engine")
    print("==========================================================")
    print(f"Loading '{model_name}' on CPU...")

    t0 = time.time()
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        model.eval()
        print(f"Model loaded successfully in {time.time() - t0:.2f}s.\n")
        return tokenizer, model
    except Exception as e:
        print(f"Error loading BGE-Reranker: {e}")
        sys.exit(1)


def compute_rerank_scores(query: str, passages: list, tokenizer, model, max_length: int = 4096):
    """Compute cross-attention relevance scores."""
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


def interactive_session(tokenizer, model):
    """Interactive RAG reranker."""
    print("\n--- BGE-Reranker Interactive Re-Ranking Session ---")
    print("Test how the cross-encoder precisely ranks candidate answers.")

    passages = [
        "To configure TLS termination on Nginx, specify ssl_certificate and ssl_certificate_key in the server block.",
        "PostgreSQL WAL logs are written before transactions commit to ensure durability.",
        "Nginx worker_processes should typically be set to 'auto' to match the number of available CPU cores.",
        "Docker containers share the host Linux kernel while maintaining process isolation.",
    ]
    print("\nCandidate Passages:")
    for idx, p in enumerate(passages, 1):
        print(f"  [{idx}] {p}")

    while True:
        try:
            query = input("\n🔍 Enter user query (or 'exit' to quit): ").strip()
            if not query:
                continue
            if query.lower() in ["exit", "quit"]:
                print("Exiting.")
                break

            t0 = time.time()
            scores = compute_rerank_scores(query, passages, tokenizer, model)
            elapsed = time.time() - t0

            ranked = sorted(zip(passages, scores), key=lambda x: x[1], reverse=True)
            print(f"\n🎯 Cross-Attention Reranked Results (Latency: {elapsed*1000:.1f}ms):")
            for doc, sc in ranked:
                bar = "█" * int(sc * 25)
                print(f"  Relevance: {sc*100:5.1f}% | {bar:<25} | {doc}")
        except (KeyboardInterrupt, EOFError):
            print("\nSession terminated.")
            break


def main():
    parser = argparse.ArgumentParser(description="BGE-Reranker-v2-M3 Cross-Encoder Runner")
    parser.add_argument("--query", type=str, help="Search query")
    parser.add_argument("--passages", nargs="+", help="Candidate passages to re-rank")
    parser.add_argument("--chat", action="store_true", help="Launch interactive reranking session")
    args = parser.parse_args()

    tokenizer, model = load_model()

    if args.chat:
        interactive_session(tokenizer, model)
        return

    # Default demonstration
    query = "How do I secure an Nginx web server with an SSL certificate?"
    candidates = [
        "PostgreSQL supports streaming replication to create read replicas.",
        "Nginx configuration for HTTPS requires defining listen 443 ssl and pointing to fullchain.pem and privkey.pem.",
        "An Nginx reverse proxy forwards HTTP requests to backend application servers using the proxy_pass directive.",
        "Python virtual environments isolate project dependencies from the system Python installation.",
    ]

    print(f"Query: \"{query}\"\n")
    print("Scoring candidate documents with Cross-Encoder...")
    t0 = time.time()
    scores = compute_rerank_scores(query, candidates, tokenizer, model)
    elapsed = time.time() - t0

    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    print(f"Re-ranking completed in {elapsed*1000:.1f}ms.\n")
    print("Ranked Results:")
    for rank, (cand, score) in enumerate(ranked, 1):
        print(f"  #{rank} [Score: {score*100:.1f}%] {cand}")


if __name__ == "__main__":
    main()
