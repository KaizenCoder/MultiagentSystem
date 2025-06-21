#!/usr/bin/env python3
"""
Test configuration multi-GPU RTX 3090 + Ollama - NextGeneration
Valide votre setup particulier avec RTX 5060 Ti + RTX 3090.
"""

import os
import asyncio
import httpx
import subprocess
import time

# Configuration RTX 3090 selon standards SuperWhisper V6
os.environ['CUDA_VISIBLE_DEVICES'] = '1'  # RTX 3090 uniquement
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:1024'

try:
    import torch
    torch_available = True
except ImportError:
    torch_available = False

def test_gpu_detection():
    """Test la dtection de votre configuration multi-GPU."""
    print(" DTECTION CONFIGURATION MULTI-GPU")
    print("=" * 50)
    
    # Test nvidia-smi
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total,pci.bus_id', '--format=csv,noheader,nounits'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            gpu_lines = result.stdout.strip().split('\n')
            print(f"[CHART] {len(gpu_lines)} GPU(s) dtecte(s):")
            
            for i, line in enumerate(gpu_lines):
                name, memory, bus_id = line.split(', ')
                print(f"   GPU {i}: {name} ({memory}MB) - Bus {bus_id}")
                
                if "RTX 5060" in name:
                    print(f"        RTX 5060 Ti dtecte (non compatible PyTorch)")
                elif "RTX 3090" in name:
                    print(f"      [CHECK] RTX 3090 dtecte (GPU principale)")
            
            return True
        else:
            print("[CROSS] nvidia-smi non disponible")
            return False
            
    except Exception as e:
        print(f"[CROSS] Erreur nvidia-smi: {e}")
        return False

def test_pytorch_gpu():
    """Test PyTorch avec configuration RTX 3090."""
    print("\n TEST PYTORCH AVEC RTX 3090")
    print("=" * 50)
    
    if not torch_available:
        print("[CROSS] PyTorch non install")
        return False
    
    # Test CUDA disponible
    if not torch.cuda.is_available():
        print("[CROSS] CUDA non disponible dans PyTorch")
        return False
    
    print(f"[CHECK] CUDA disponible dans PyTorch")
    
    # Test configuration GPU
    device_count = torch.cuda.device_count()
    print(f"[CHART] {device_count} GPU(s) visible(s) par PyTorch")
    
    if device_count == 0:
        print("[CROSS] Aucune GPU visible")
        return False
    
    # Test GPU active (doit tre RTX 3090)
    current_device = torch.cuda.current_device()
    gpu_name = torch.cuda.get_device_name(current_device)
    gpu_props = torch.cuda.get_device_properties(current_device)
    
    print(f" GPU active: {gpu_name}")
    print(f"   Compute Capability: {gpu_props.major}.{gpu_props.minor}")
    print(f"   VRAM: {gpu_props.total_memory / 1024**3:.1f}GB")
    
    # Validation RTX 3090
    if "RTX 3090" in gpu_name:
        print("[CHECK] RTX 3090 correctement configure pour PyTorch")
        
        # Test allocation simple
        try:
            test_tensor = torch.randn(1000, 1000, device='cuda')
            result = torch.matmul(test_tensor, test_tensor.t())
            del test_tensor, result
            torch.cuda.empty_cache()
            print("[CHECK] Test allocation GPU russi")
            return True
        except Exception as e:
            print(f"[CROSS] Erreur allocation GPU: {e}")
            return False
    else:
        print(f"[CROSS] GPU incorrecte dtecte: {gpu_name} (RTX 3090 attendue)")
        return False

async def test_ollama_service():
    """Test le service Ollama."""
    print("\n TEST SERVICE OLLAMA")
    print("=" * 50)
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:11434/api/tags")
            
        if response.status_code == 200:
            models_data = response.json()
            models = models_data.get("models", [])
            
            print(f"[CHECK] Ollama connect")
            print(f"[CLIPBOARD] {len(models)} modle(s) install(s):")
            
            # Vos modles recommands
            your_models = {
                "nous-hermes-2-mistral-7b-dpo": "Vitesse",
                "llama3:8b-instruct-q6_k": "Usage quotidien", 
                "mixtral-8x7b": "Qualit maximum",
                "qwen-coder-32b": "Code spcialis",
                "qwen2.5-coder:1.5b": "Tests rapides"
            }
            
            available_models = [m["name"] for m in models]
            
            for model_name, description in your_models.items():
                if any(model_name in available for available in available_models):
                    print(f"   [CHECK] {description}: {model_name}")
                else:
                    print(f"   [CROSS] {description}: {model_name} (absent)")
            
            return len(models) > 0
            
        else:
            print(f"[CROSS] Ollama erreur: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"[CROSS] Ollama non accessible: {e}")
        print("[BULB] Vrifiez qu'Ollama est dmarr: ollama serve")
        return False

async def test_ollama_performance():
    """Test performance Ollama avec vos modles."""
    print("\n[LIGHTNING] TEST PERFORMANCE OLLAMA")
    print("=" * 50)
    
    # Modles  tester par ordre de vitesse
    test_models = [
        ("qwen2.5-coder:1.5b", "Test ultra-rapide"),
        ("llama3:8b-instruct-q6_k", "Test quotidien"),
        ("nous-hermes-2-mistral-7b-dpo", "Test vitesse")
    ]
    
    for model_name, description in test_models:
        print(f"\n[SEARCH] {description}: {model_name}")
        
        payload = {
            "model": model_name,
            "prompt": "Dis 'Bonjour RTX 3090' en une ligne",
            "stream": False,
            "options": {
                "num_gpu": 1,
                "gpu_layers": -1,
                "temperature": 0.7
            }
        }
        
        try:
            start_time = time.time()
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "http://localhost:11434/api/generate",
                    json=payload
                )
            
            duration = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get("response", "").strip()
                
                # Mtriques de performance
                eval_count = result.get("eval_count", 0)
                eval_duration = result.get("eval_duration", 0) / 1e9  # ns to s
                tokens_per_sec = eval_count / eval_duration if eval_duration > 0 else 0
                
                print(f"   [CHECK] Rponse: {response_text}")
                print(f"     Temps total: {duration:.2f}s")
                print(f"   [ROCKET] Vitesse: {tokens_per_sec:.1f} tokens/sec")
                
            else:
                print(f"   [CROSS] Erreur: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   [CROSS] Erreur: {e}")
        
        # Pause entre tests
        await asyncio.sleep(1)

async def test_ollama_worker():
    """Test du worker Ollama intgr."""
    print("\n[ROBOT] TEST WORKER OLLAMA INTGR")
    print("=" * 50)
    
    try:
        # Import du worker
        import sys
        sys.path.append('orchestrator')
        
        from orchestrator.app.agents.ollama_worker import OllamaLocalWorker
        
        class MockConfig:
            OLLAMA_BASE_URL = "http://localhost:11434"
            OLLAMA_GPU_DEVICE = "1"
        
        worker = OllamaLocalWorker(MockConfig())
        
        # Test sant
        health = await worker.health_check()
        print(f" Sant: {health.get('status', 'unknown')}")
        print(f"[CHART] Modles disponibles: {health.get('our_models_available', 0)}/{health.get('our_models_total', 0)}")
        
        # Test traitement
        if health.get('status') == 'healthy':
            test_tasks = [
                ("Dis bonjour", ["fast"]),
                ("cris une fonction Python pour additionner", ["code"]),
                ("Analyse les avantages de l'IA", ["quality"])
            ]
            
            for task, requirements in test_tasks:
                print(f"\n Test: {task}")
                result = await worker.process_task(task, requirements)
                
                if result.get('success'):
                    print(f"   [CHECK] Modle: {result.get('model_category')} ({result.get('model_used')})")
                    print(f"     Temps: {result.get('processing_time', 0):.2f}s")
                    print(f"    Rponse: {result.get('result', '')[:100]}...")
                else:
                    print(f"   [CROSS] Erreur: {result.get('error', 'Inconnue')}")
                
                await asyncio.sleep(2)
        
        return health.get('status') == 'healthy'
        
    except Exception as e:
        print(f"[CROSS] Erreur worker: {e}")
        return False

async def main():
    """Test complet de votre configuration."""
    print("[TARGET] TEST CONFIGURATION MULTI-GPU RTX 3090 + OLLAMA")
    print(" NextGeneration - Configuration Particulire")
    print("=" * 70)
    
    results = {}
    
    # Test 1: Dtection GPU
    results['gpu_detection'] = test_gpu_detection()
    
    # Test 2: PyTorch GPU
    results['pytorch_gpu'] = test_pytorch_gpu()
    
    # Test 3: Service Ollama
    results['ollama_service'] = await test_ollama_service()
    
    # Test 4: Performance Ollama
    if results['ollama_service']:
        await test_ollama_performance()
    
    # Test 5: Worker intgr
    results['ollama_worker'] = await test_ollama_worker()
    
    # Rsum final
    print("\n" + "=" * 70)
    print("[CHART] RSUM CONFIGURATION")
    print("=" * 70)
    
    print(f" Dtection GPU: {'[CHECK]' if results['gpu_detection'] else '[CROSS]'}")
    print(f" PyTorch RTX 3090: {'[CHECK]' if results['pytorch_gpu'] else '[CROSS]'}")
    print(f" Service Ollama: {'[CHECK]' if results['ollama_service'] else '[CROSS]'}")
    print(f"[ROBOT] Worker Ollama: {'[CHECK]' if results['ollama_worker'] else '[CROSS]'}")
    
    all_ok = all(results.values())
    
    if all_ok:
        print("\n CONFIGURATION PARFAITE !")
        print("[BULB] Votre setup multi-GPU RTX 3090 + Ollama est oprationnel")
        print("[ROCKET] Prt pour l'intgration avec l'orchestrateur NextGeneration")
        
        print("\n[CLIPBOARD] Modles recommands selon usage:")
        print("   [LIGHTNING] Vitesse: nous-hermes-2-mistral-7b-dpo")
        print("    Code: qwen-coder-32b") 
        print("    Qualit: mixtral-8x7b")
        print("    Quotidien: llama3:8b-instruct-q6_k")
    else:
        print("\n CONFIGURATION  CORRIGER")
        print("[BULB] Vrifiez les lments marqus [CROSS] ci-dessus")
        
        if not results['ollama_service']:
            print("   - Dmarrez Ollama: ollama serve")
        if not results['pytorch_gpu']:
            print("   - Vrifiez configuration CUDA/PyTorch")

if __name__ == "__main__":
    asyncio.run(main())




