import argparse
import time
from llama_cpp import Llama

def main(prompt: str, max_tokens: int):
    print("Loading lightweight local LLM (GGUF format)...")
    start_time = time.time()
    
    # Hugging Face'dan avtomatik ravishda kichik va sifatli siqilgan GGUF modelini tortib oladi
    model_path = "Qwen/Qwen2.5-1.5B-Instruct-GGUF"
    model_file = "qwen2.5-1.5b-instruct-q4_k_m.gguf"
    
    try:
        llm = Llama.from_pretrained(
            repo_id=model_path,
            filename=model_file,
            n_ctx=2048,
            n_threads=4, # CPU yadrolari soni
            verbose=False
        )
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    print(f"Model loaded. Time taken: {time.time() - start_time:.2f} seconds")
    print(f"\nPrompt: '{prompt}'\nGenerating response...")
    
    start_inference = time.time()
    output = llm(
        prompt,
        max_tokens=max_tokens,
        temperature=0.7,
        stop=["<|im_end|>"],
        echo=False
    )
    
    response = output["choices"][0]["text"].strip()
    print("-" * 50)
    print(response)
    print("-" * 50)
    print(f"Generation finished in {time.time() - start_inference:.2f} seconds.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Offline Local LLM Microservice")
    parser.add_argument("--prompt", type=str, default="Explain what MLOps is in 3 sentences.", help="Input prompt")
    parser.add_argument("--tokens", type=int, default=150, help="Max tokens to generate")
    args = parser.parse_args()
    main(args.prompt, args.tokens)