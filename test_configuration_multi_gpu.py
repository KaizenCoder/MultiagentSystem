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
    """Test la détection de votre configuration multi-GPU."""
    print("🎮 DÉTECTION CONFIGURATION MULTI-GPU")
    print("=" * 50)
    
    # Test nvidia-smi
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total,pci.bus_id', '--format=csv,noheader,nounits'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            gpu_lines = result.stdout.strip().split('\n')
            print(f"📊 {len(gpu_lines)} GPU(s) détectée(s):")
            
            for i, line in enumerate(gpu_lines):
                name, memory, bus_id = line.split(', ')
                print(f"   GPU {i}: {name} ({memory}MB) - Bus {bus_id}")
                
                if "RTX 5060" in name:
                    print(f"      ⚠️  RTX 5060 Ti détectée (non compatible PyTorch)")
                elif "RTX 3090" in name:
                    print(f"      ✅ RTX 3090 détectée (GPU principale)")
            
            return True
        else:
            print("❌ nvidia-smi non disponible")
            return False
            
    except Exception as e:
        print(f"❌ Erreur nvidia-smi: {e}")
        return False

def test_pytorch_gpu():
    """Test PyTorch avec configuration RTX 3090."""
    print("\n🔥 TEST PYTORCH AVEC RTX 3090")
    print("=" * 50)
    
    if not torch_available:
        print("❌ PyTorch non installé")
        return False
    
    # Test CUDA disponible
    if not torch.cuda.is_available():
        print("❌ CUDA non disponible dans PyTorch")
        return False
    
    print(f"✅ CUDA disponible dans PyTorch")
    
    # Test configuration GPU
    device_count = torch.cuda.device_count()
    print(f"📊 {device_count} GPU(s) visible(s) par PyTorch")
    
    if device_count == 0:
        print("❌ Aucune GPU visible")
        return False
    
    # Test GPU active (doit être RTX 3090)
    current_device = torch.cuda.current_device()
    gpu_name = torch.cuda.get_device_name(current_device)
    gpu_props = torch.cuda.get_device_properties(current_device)
    
    print(f"🎮 GPU active: {gpu_name}")
    print(f"   Compute Capability: {gpu_props.major}.{gpu_props.minor}")
    print(f"   VRAM: {gpu_props.total_memory / 1024**3:.1f}GB")
    
    # Validation RTX 3090
    if "RTX 3090" in gpu_name:
        print("✅ RTX 3090 correctement configurée pour PyTorch")
        
        # Test allocation simple
        try:
            test_tensor = torch.randn(1000, 1000, device='cuda')
            result = torch.matmul(test_tensor, test_tensor.t())
            del test_tensor, result
            torch.cuda.empty_cache()
            print("✅ Test allocation GPU réussi")
            return True
        except Exception as e:
            print(f"❌ Erreur allocation GPU: {e}")
            return False
    else:
        print(f"❌ GPU incorrecte détectée: {gpu_name} (RTX 3090 attendue)")
        return False

async def test_ollama_service():
    """Test le service Ollama."""
    print("\n🦙 TEST SERVICE OLLAMA")
    print("=" * 50)
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:11434/api/tags")
            
        if response.status_code == 200:
            models_data = response.json()
            models = models_data.get("models", [])
            
            print(f"✅ Ollama connecté")
            print(f"📋 {len(models)} modèle(s) installé(s):")
            
            # Vos modèles recommandés
            your_models = {
                "nous-hermes-2-mistral-7b-dpo": "Vitesse",
                "llama3:8b-instruct-q6_k": "Usage quotidien", 
                "mixtral-8x7b": "Qualité maximum",
                "qwen-coder-32b": "Code spécialisé",
                "qwen2.5-coder:1.5b": "Tests rapides"
            }
            
            available_models = [m["name"] for m in models]
            
            for model_name, description in your_models.items():
                if any(model_name in available for available in available_models):
                    print(f"   ✅ {description}: {model_name}")
                else:
                    print(f"   ❌ {description}: {model_name} (absent)")
            
            return len(models) > 0
            
        else:
            print(f"❌ Ollama erreur: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ollama non accessible: {e}")
        print("💡 Vérifiez qu'Ollama est démarré: ollama serve")
        return False

async def test_ollama_performance():
    """Test performance Ollama avec vos modèles."""
    print("\n⚡ TEST PERFORMANCE OLLAMA")
    print("=" * 50)
    
    # Modèles à tester par ordre de vitesse
    test_models = [
        ("qwen2.5-coder:1.5b", "Test ultra-rapide"),
        ("llama3:8b-instruct-q6_k", "Test quotidien"),
        ("nous-hermes-2-mistral-7b-dpo", "Test vitesse")
    ]
    
    for model_name, description in test_models:
        print(f"\n🔍 {description}: {model_name}")
        
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
                
                # Métriques de performance
                eval_count = result.get("eval_count", 0)
                eval_duration = result.get("eval_duration", 0) / 1e9  # ns to s
                tokens_per_sec = eval_count / eval_duration if eval_duration > 0 else 0
                
                print(f"   ✅ Réponse: {response_text}")
                print(f"   ⏱️  Temps total: {duration:.2f}s")
                print(f"   🚀 Vitesse: {tokens_per_sec:.1f} tokens/sec")
                
            else:
                print(f"   ❌ Erreur: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
        
        # Pause entre tests
        await asyncio.sleep(1)

async def test_ollama_worker():
    """Test du worker Ollama intégré."""
    print("\n🤖 TEST WORKER OLLAMA INTÉGRÉ")
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
        
        # Test santé
        health = await worker.health_check()
        print(f"🏥 Santé: {health.get('status', 'unknown')}")
        print(f"📊 Modèles disponibles: {health.get('our_models_available', 0)}/{health.get('our_models_total', 0)}")
        
        # Test traitement
        if health.get('status') == 'healthy':
            test_tasks = [
                ("Dis bonjour", ["fast"]),
                ("Écris une fonction Python pour additionner", ["code"]),
                ("Analyse les avantages de l'IA", ["quality"])
            ]
            
            for task, requirements in test_tasks:
                print(f"\n🧪 Test: {task}")
                result = await worker.process_task(task, requirements)
                
                if result.get('success'):
                    print(f"   ✅ Modèle: {result.get('model_category')} ({result.get('model_used')})")
                    print(f"   ⏱️  Temps: {result.get('processing_time', 0):.2f}s")
                    print(f"   💬 Réponse: {result.get('result', '')[:100]}...")
                else:
                    print(f"   ❌ Erreur: {result.get('error', 'Inconnue')}")
                
                await asyncio.sleep(2)
        
        return health.get('status') == 'healthy'
        
    except Exception as e:
        print(f"❌ Erreur worker: {e}")
        return False

async def main():
    """Test complet de votre configuration."""
    print("🎯 TEST CONFIGURATION MULTI-GPU RTX 3090 + OLLAMA")
    print("🎮 NextGeneration - Configuration Particulière")
    print("=" * 70)
    
    results = {}
    
    # Test 1: Détection GPU
    results['gpu_detection'] = test_gpu_detection()
    
    # Test 2: PyTorch GPU
    results['pytorch_gpu'] = test_pytorch_gpu()
    
    # Test 3: Service Ollama
    results['ollama_service'] = await test_ollama_service()
    
    # Test 4: Performance Ollama
    if results['ollama_service']:
        await test_ollama_performance()
    
    # Test 5: Worker intégré
    results['ollama_worker'] = await test_ollama_worker()
    
    # Résumé final
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ CONFIGURATION")
    print("=" * 70)
    
    print(f"🎮 Détection GPU: {'✅' if results['gpu_detection'] else '❌'}")
    print(f"🔥 PyTorch RTX 3090: {'✅' if results['pytorch_gpu'] else '❌'}")
    print(f"🦙 Service Ollama: {'✅' if results['ollama_service'] else '❌'}")
    print(f"🤖 Worker Ollama: {'✅' if results['ollama_worker'] else '❌'}")
    
    all_ok = all(results.values())
    
    if all_ok:
        print("\n🎉 CONFIGURATION PARFAITE !")
        print("💡 Votre setup multi-GPU RTX 3090 + Ollama est opérationnel")
        print("🚀 Prêt pour l'intégration avec l'orchestrateur NextGeneration")
        
        print("\n📋 Modèles recommandés selon usage:")
        print("   ⚡ Vitesse: nous-hermes-2-mistral-7b-dpo")
        print("   💻 Code: qwen-coder-32b") 
        print("   🌟 Qualité: mixtral-8x7b")
        print("   📱 Quotidien: llama3:8b-instruct-q6_k")
    else:
        print("\n⚠️ CONFIGURATION À CORRIGER")
        print("💡 Vérifiez les éléments marqués ❌ ci-dessus")
        
        if not results['ollama_service']:
            print("   - Démarrez Ollama: ollama serve")
        if not results['pytorch_gpu']:
            print("   - Vérifiez configuration CUDA/PyTorch")

if __name__ == "__main__":
    asyncio.run(main())
