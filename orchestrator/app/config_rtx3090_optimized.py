# Configuration RTX3090 Optimise - NextGeneration
import os
from typing import Dict, Any

# Configuration GPU RTX 3090
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'

class RTX3090OptimizedConfig:
    """Configuration optimise pour RTX3090 avec modles valids"""
    
    # Modles RTX3090 optimiss (valids par benchmarks)
    OLLAMA_MODELS = {
        "speed": {
            "model": "nous-hermes-2-mistral-7b-dpo:latest",
            "performance": "6.4 tokens/s",
            "vram_gb": 4.1,
            "use_case": "Rponses rapides, interactions temps rel"
        },
        "quality": {
            "model": "mixtral:8x7b-instruct-v0.1-q3_k_m", 
            "performance": "5.4 tokens/s",
            "vram_gb": 22.0,
            "use_case": "Qualit maximale, quantization Q3_K optimise"
        },
        "balanced": {
            "model": "llama3:8b-instruct-q6_k",
            "performance": "4.9 tokens/s", 
            "vram_gb": 6.6,
            "use_case": "Usage quotidien quilibr"
        },
        "code": {
            "model": "qwen-coder-32b:latest",
            "performance": "Spcialis dveloppement",
            "vram_gb": 19.0,
            "use_case": "Code professionnel, debugging"
        }
    }
    
    # Configuration RTX3090
    GPU_CONFIG = {
        "device_id": 1,  # RTX 3090 sur bus PCI 1
        "total_vram_gb": 24,
        "reserved_vram_gb": 2,  # Rserver 2GB pour systme
        "available_vram_gb": 22,
        "cuda_visible_devices": "1",
        "cuda_device_order": "PCI_BUS_ID"
    }
    
    # Slecteur intelligent de modles
    MODEL_SELECTOR = {
        "quick_tasks": "speed",      # Tches rapides
        "complex_analysis": "quality",  # Analyses complexes
        "daily_usage": "balanced",   # Usage quotidien
        "code_tasks": "code",        # Dveloppement
        "default": "balanced"        # Par dfaut
    }
    
    # Configuration Ollama
    OLLAMA_CONFIG = {
        "base_url": "http://localhost:11434",
        "timeout": 300,
        "num_gpu": 1,
        "gpu_memory_fraction": 0.9,  # Utiliser 90% VRAM disponible
        "temperature": 0.7,
        "max_tokens": 4096
    }

# Configuration globale
settings = RTX3090OptimizedConfig()




