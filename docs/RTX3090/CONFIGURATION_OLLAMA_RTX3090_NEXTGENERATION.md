# 🎮 Configuration Ollama RTX 3090 - NextGeneration

## 🚨 Configuration Spéciale Multi-GPU

Votre système a une configuration particulière :
- **RTX 5060 Ti** (Bus PCI 0) - Non compatible PyTorch/CUDA actuel
- **RTX 3090** (Bus PCI 1) - GPU principale pour IA/ML

## 🔧 Configuration Ollama pour RTX 3090

### 1. Variables d'Environnement Ollama

```powershell
# Configuration pour forcer Ollama sur RTX 3090 uniquement
$env:CUDA_VISIBLE_DEVICES = "1"
$env:OLLAMA_GPU_DEVICE = "1"
$env:OLLAMA_NUM_GPU = "1"
$env:OLLAMA_MODELS = "D:\modeles_llm"

# Redémarrer Ollama avec cette configuration
Stop-Process -Name "ollama" -Force -ErrorAction SilentlyContinue
Start-Sleep 2
ollama serve
```

### 2. Configuration Système Permanente

```powershell
# Créer script de démarrage Ollama RTX 3090
$script = @"
@echo off
echo 🎮 Configuration Ollama RTX 3090 NextGeneration
set CUDA_VISIBLE_DEVICES=1
set OLLAMA_GPU_DEVICE=1
set OLLAMA_NUM_GPU=1
set OLLAMA_MODELS=D:\modeles_llm
echo ✅ Variables configurées pour RTX 3090
ollama serve
"@

$script | Out-File -FilePath "D:\modeles_llm\start_ollama_rtx3090.bat" -Encoding ASCII
```

## 🎯 Modèles Recommandés pour Votre RTX 3090

Avec vos modèles existants + recommandations spécifiques :

### ✅ **Gardez Ces Excellents Modèles :**

1. **Mixtral-8x7B** (26GB) - Votre modèle "qualité maximum"
2. **Qwen-Coder-32B** (19GB) - Excellent pour code  
3. **Llama3:8B** (6.6GB) - Usage quotidien parfait
4. **Nous-Hermes-2-Mistral 7B** (4.1GB) - Vitesse excellente

### 🚀 **Ajout Recommandé :**

```powershell
# Modèle ultime qualité pour RTX 3090
ollama pull llama3.1:70b-instruct-q4_k_m
```

### ❌ **Supprimez pour Optimiser :**

```powershell
# Libérer ~25GB d'espace
ollama rm deepseek-coder:1.3b deepseek-coder:6.7b deepseek-coder:33b
ollama rm starcoder2:3b code-stral:latest
ollama rm llama3.2:1b llama3.2:latest
```

## 🔗 Intégration Orchestrateur NextGeneration

### Configuration dans .env

```env
# Ajout configuration modèles locaux
LOCAL_MODELS_ENABLED=true
LOCAL_MODELS_PATH=D:/modeles_llm
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_GPU_DEVICE=1

# Force RTX 3090 pour tout le système
CUDA_VISIBLE_DEVICES=1
CUDA_DEVICE_ORDER=PCI_BUS_ID
```

### Worker Ollama pour l'Orchestrateur

```python
# orchestrator/app/agents/ollama_worker.py

import httpx
import os
from typing import Dict, Any, List
from .base_worker import BaseWorker

class OllamaLocalWorker(BaseWorker):
    """Worker pour modèles Ollama locaux sur RTX 3090."""
    
    def __init__(self, config):
        super().__init__(config)
        self.ollama_url = "http://localhost:11434"
        
        # Modèles optimisés pour votre RTX 3090
        self.available_models = {
            "speed": "nous-hermes-2-mistral-7b-dpo",
            "quality": "mixtral-8x7b",
            "code": "qwen-coder-32b", 
            "daily": "llama3:8b-instruct-q6_k",
            "ultra_quality": "llama3.1:70b-instruct-q4_k_m"
        }
    
    async def can_handle_task(self, task: str, requirements: List[str]) -> bool:
        """Gère les tâches locales pour confidentialité/vitesse."""
        
        # Priorité aux modèles locaux pour confidentialité
        if "local" in requirements or "confidential" in requirements:
            return True
        
        # Modèles locaux souvent plus rapides que API
        if "fast" in requirements or "quick" in requirements:
            return True
            
        # Code spécialisé
        if "code" in task.lower() and "code" in requirements:
            return True
            
        return False
    
    async def process_task(self, task: str, requirements: List[str] = None) -> Dict[str, Any]:
        """Traite avec le modèle optimal selon la tâche."""
        
        if requirements is None:
            requirements = []
        
        # Sélection intelligente du modèle
        if "ultra" in requirements or "complex" in requirements:
            model = self.available_models["ultra_quality"]
        elif "code" in task.lower() or "code" in requirements:
            model = self.available_models["code"]
        elif "fast" in requirements or "quick" in requirements:
            model = self.available_models["speed"]
        elif "quality" in requirements:
            model = self.available_models["quality"]
        else:
            model = self.available_models["daily"]
        
        try:
            response = await self._call_ollama(model, task)
            
            return {
                "result": response,
                "model_used": model,
                "agent_type": "ollama_local",
                "privacy": "local_processing",
                "cost": "free",
                "gpu_used": "RTX 3090",
                "confidence": 0.95
            }
            
        except Exception as e:
            return {
                "result": f"Erreur modèle local: {str(e)}",
                "success": False,
                "agent_type": "ollama_local"
            }
    
    async def _call_ollama(self, model: str, prompt: str) -> str:
        """Appel à Ollama configuré pour RTX 3090."""
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_ctx": 4096,
                "num_gpu": 1,  # Force 1 GPU (RTX 3090)
                "gpu_layers": -1  # Toutes les couches sur GPU
            }
        }
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.ollama_url}/api/generate",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["response"]
            else:
                raise Exception(f"Ollama error: {response.status_code} - {response.text}")
```

## 🧪 Test de Configuration

### Script de Test Complet

```python
#!/usr/bin/env python3
"""
Test configuration Ollama RTX 3090 - NextGeneration
"""

import os
import httpx
import asyncio

# Force RTX 3090 (configuration SuperWhisper V6)
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'

async def test_ollama_rtx3090():
    """Test Ollama avec configuration RTX 3090."""
    
    print("🎮 Test Ollama sur RTX 3090")
    print("=" * 40)
    
    # Test modèles disponibles
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:11434/api/tags")
        
        if response.status_code == 200:
            models = response.json()["models"]
            print(f"✅ {len(models)} modèles trouvés")
            
            # Test vos meilleurs modèles
            test_models = [
                "nous-hermes-2-mistral-7b-dpo",  # Rapidité
                "llama3:8b-instruct-q6_k",       # Équilibre  
                "qwen-coder-32b"                 # Code
            ]
            
            for model_name in test_models:
                if any(model_name in m["name"] for m in models):
                    await test_model_performance(model_name)
                else:
                    print(f"⚠️ Modèle {model_name} non trouvé")

async def test_model_performance(model_name: str):
    """Test performance d'un modèle."""
    
    payload = {
        "model": model_name,
        "prompt": "Dis 'Bonjour RTX 3090' en une ligne",
        "stream": False,
        "options": {"num_gpu": 1, "gpu_layers": -1}
    }
    
    try:
        start_time = asyncio.get_event_loop().time()
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json=payload
            )
        
        end_time = asyncio.get_event_loop().time()
        duration = end_time - start_time
        
        if response.status_code == 200:
            result = response.json()
            response_text = result["response"].strip()
            print(f"✅ {model_name}: {response_text} ({duration:.2f}s)")
        else:
            print(f"❌ {model_name}: Erreur {response.status_code}")
            
    except Exception as e:
        print(f"❌ {model_name}: {e}")

if __name__ == "__main__":
    asyncio.run(test_ollama_rtx3090())
```

## 🎯 Recommandation Finale

**Avec votre configuration multi-GPU particulière :**

1. **Utilisez exclusivement la RTX 3090** pour les LLM
2. **Gardez vos excellents modèles** (Mixtral, Qwen-Coder, Llama3)  
3. **Ajoutez Llama3.1:70B** pour la qualité ultime
4. **Intégrez avec l'orchestrateur** via le worker Ollama

**Avantages de votre setup :**
- 🔒 **Confidentialité totale** (modèles locaux)
- ⚡ **Ultra-rapide** (RTX 3090 24GB)
- 💰 **Coût zéro** (pas d'API)
- 🎯 **4 modèles optimisés** pour tous cas d'usage

Voulez-vous que je vous aide à configurer et tester cette intégration ?
