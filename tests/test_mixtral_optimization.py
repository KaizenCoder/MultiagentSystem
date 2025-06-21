#!/usr/bin/env python3
"""
Test optimisation Mixtral RTX3090
"""

import os
os.environ['CUDA_VISIBLE_DEVICES'] = '1'

import asyncio
import httpx

async def test_mixtral_variants():
    """Test diffrentes variantes Mixtral"""
    
    models_to_test = [
        "mixtral:8x7b-instruct-v0.1-q3_k_m",  # Version optimise
        "llama3.1:70b-instruct-q4_k_m",       # Alternative qualit
    ]
    
    for model in models_to_test:
        print(f"Test modle: {model}")
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                # Test disponibilit
                response = await client.get("http://localhost:11434/api/tags")
                if response.status_code == 200:
                    available = any(model in m["name"] for m in response.json()["models"])
                    print(f"Disponible: {available}")
                    
                    if available:
                        # Test simple
                        payload = {
                            "model": model,
                            "prompt": "Dis bonjour en une phrase",
                            "stream": False
                        }
                        
                        test_response = await client.post(
                            "http://localhost:11434/api/generate",
                            json=payload
                        )
                        
                        if test_response.status_code == 200:
                            print(f"[CHECK] {model}: Fonctionnel")
                        else:
                            print(f"[CROSS] {model}: Erreur {test_response.status_code}")
                    else:
                        print(f" {model}: Non install")
                        
        except Exception as e:
            print(f"[CROSS] {model}: Exception {e}")

if __name__ == "__main__":
    asyncio.run(test_mixtral_variants())




