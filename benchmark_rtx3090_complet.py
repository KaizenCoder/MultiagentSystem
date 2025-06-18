#!/usr/bin/env python3
"""
Benchmark RTX3090 Complet - NextGeneration
"""

import asyncio
import httpx
import time
import json
import os
from datetime import datetime

os.environ['CUDA_VISIBLE_DEVICES'] = '1'

async def benchmark_model(model_name, test_prompts):
    """Benchmark un modle"""
    print(f" Test: {model_name}")
    
    results = []
    
    async with httpx.AsyncClient(timeout=60) as client:
        for prompt in test_prompts:
            try:
                start_time = time.time()
                
                payload = {
                    "model": model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.7, "num_gpu": 1}
                }
                
                response = await client.post("http://localhost:11434/api/generate", json=payload)
                
                if response.status_code == 200:
                    end_time = time.time()
                    result_data = response.json()
                    response_text = result_data.get("response", "")
                    
                    processing_time = end_time - start_time
                    tokens = len(response_text.split())
                    tokens_per_sec = tokens / processing_time if processing_time > 0 else 0
                    
                    results.append({
                        "prompt": prompt[:30] + "...",
                        "time": processing_time,
                        "tokens": tokens,
                        "tokens_per_sec": tokens_per_sec
                    })
                    
                    print(f"   {processing_time:.1f}s, {tokens_per_sec:.1f} t/s")
                    
            except Exception as e:
                print(f"   Erreur: {e}")
    
    return results

async def main():
    """Benchmark principal"""
    print(" BENCHMARK RTX3090 COMPLET")
    print("=" * 40)
    
    models_to_test = [
        "nous-hermes-2-mistral-7b-dpo:latest",
        "mixtral:8x7b-instruct-v0.1-q3_k_m",
        "llama3:8b-instruct-q6_k"
    ]
    
    test_prompts = [
        "Explique l'IA en 2 phrases",
        "cris une fonction Python",
        "Analyse les avantages du cloud"
    ]
    
    benchmark_results = {
        "timestamp": datetime.now().isoformat(),
        "gpu": "RTX 3090",
        "models": {}
    }
    
    for model in models_to_test:
        results = await benchmark_model(model, test_prompts)
        if results:
            avg_time = sum(r["time"] for r in results) / len(results)
            avg_tokens_per_sec = sum(r["tokens_per_sec"] for r in results) / len(results)
            
            benchmark_results["models"][model] = {
                "avg_time": avg_time,
                "avg_tokens_per_sec": avg_tokens_per_sec,
                "tests": results
            }
            
            print(f"[CHART] {model}: {avg_tokens_per_sec:.1f} tokens/s moyenne")
    
    # Sauvegarde
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"benchmark_rtx3090_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(benchmark_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n[DOCUMENT] Rsultats: {filename}")

if __name__ == "__main__":
    asyncio.run(main())
