# 🚀 Guide des Modèles LLM Locaux pour RTX 3090

## 🎯 Recommandations Optimisées RTX 3090 (24GB VRAM)

### 🏆 Modèles TOP Recommandés

#### 1. **Llama 3.1 8B Instruct** (Recommandé #1)
```bash
Taille: ~5GB VRAM
Performance: Excellent rapport qualité/vitesse
Temps: ~2-5 tokens/seconde
Usage VRAM: 20-25% (très économe)
```
**Pourquoi :** Modèle Meta ultra-optimisé, excellent pour la plupart des tâches

#### 2. **Mistral 7B Instruct v0.3** (Recommandé #2)
```bash
Taille: ~4.5GB VRAM
Performance: Très bon, spécialisé code
Temps: ~3-6 tokens/seconde
Usage VRAM: 18-22%
```
**Pourquoi :** Excellent pour le code, moins censuré, très rapide

#### 3. **CodeLlama 13B Instruct** (Spécialisé Code)
```bash
Taille: ~8GB VRAM
Performance: Excellent pour programmation
Temps: ~1-3 tokens/seconde
Usage VRAM: 35-40%
```
**Pourquoi :** Spécialement conçu pour la génération de code

#### 4. **Llama 3.1 70B Instruct (Quantized 4-bit)** (Maximum Qualité)
```bash
Taille: ~20-22GB VRAM
Performance: Qualité proche GPT-4
Temps: ~0.5-1 token/seconde
Usage VRAM: 85-95%
```
**Pourquoi :** Maximum de qualité possible sur RTX 3090

### 📊 Tableau Comparatif

| Modèle | VRAM | Vitesse | Qualité | Spécialité |
|--------|------|---------|---------|------------|
| **Llama 3.1 8B** | 5GB | ⚡⚡⚡ | 🌟🌟🌟🌟 | Généraliste |
| **Mistral 7B** | 4.5GB | ⚡⚡⚡⚡ | 🌟🌟🌟 | Code/Tech |
| **CodeLlama 13B** | 8GB | ⚡⚡ | 🌟🌟🌟🌟 | Programmation |
| **Llama 70B (4-bit)** | 22GB | ⚡ | 🌟🌟🌟🌟🌟 | Qualité Max |

---

## 🛠️ Installation et Configuration

### 1. Installation d'Ollama (Recommandé)

```powershell
# Installation Ollama (gestionnaire modèles local)
# Télécharger depuis: https://ollama.ai/download/windows

# Après installation, télécharger les modèles:
ollama pull llama3.1:8b-instruct-q4_K_M
ollama pull mistral:7b-instruct-v0.3
ollama pull codellama:13b-instruct
```

### 2. Alternative : LM Studio (Interface Graphique)

```bash
# Télécharger LM Studio: https://lmstudio.ai/
# Interface graphique conviviale
# Gestion automatique VRAM
# Compatible RTX 3090
```

### 3. Répertoire de Stockage

```powershell
# Créer le répertoire
New-Item -ItemType Directory -Path "D:\modeles_llm" -Force

# Configuration Ollama pour utiliser ce répertoire
$env:OLLAMA_MODELS = "D:\modeles_llm"
```

---

## 🔧 Configuration Optimale RTX 3090

### Paramètres GPU Recommandés

```json
{
  "gpu_layers": -1,
  "context_length": 4096,
  "batch_size": 512,
  "threads": 8,
  "gpu_memory_fraction": 0.9,
  "quantization": "q4_K_M"
}
```

### Scripts de Benchmark

```python
# test_gpu_performance.py
import time
import psutil
import GPUtil

def benchmark_model(model_name):
    """Benchmark d'un modèle local."""
    
    prompts = [
        "Explique l'intelligence artificielle en 2 phrases",
        "Écris une fonction Python pour trier une liste",
        "Analyse les avantages du cloud computing"
    ]
    
    for prompt in prompts:
        start_time = time.time()
        
        # Appel au modèle local (via Ollama)
        response = call_local_model(model_name, prompt)
        
        end_time = time.time()
        tokens = len(response.split())
        speed = tokens / (end_time - start_time)
        
        print(f"Model: {model_name}")
        print(f"Prompt: {prompt[:30]}...")
        print(f"Speed: {speed:.1f} tokens/sec")
        print(f"VRAM: {get_gpu_usage():.1f}%")
        print("-" * 40)
```

---

## ⚡ Optimisations Spécifiques RTX 3090

### 1. Configuration CUDA

```bash
# Vérifier CUDA
nvidia-smi

# Variables d'environnement optimales
set CUDA_VISIBLE_DEVICES=0
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:1024
```

### 2. Paramètres Mémoire

```python
# Configuration optimale pour 24GB
config = {
    "max_memory": "22GB",  # Garde 2GB pour le système
    "offload_folder": "D:/temp_offload",
    "quantization": "4bit",  # Économise 50% VRAM
    "attention_implementation": "flash_attention_2"
}
```

### 3. Modèles Multiples Simultanés

Avec 24GB, vous pouvez faire tourner :
- **2 modèles 7B simultanément** (pour comparaison)
- **1 modèle 13B + 1 modèle 7B**
- **1 seul modèle 70B quantized pour qualité max**

---

## 🔗 Intégration avec l'Orchestrateur

### Configuration dans config.py

```python
# Ajouter dans orchestrator/app/config.py

class Settings(BaseSettings):
    # ...existing code...
    
    # Configuration modèles locaux
    LOCAL_MODELS_ENABLED: bool = True
    LOCAL_MODELS_PATH: str = "D:/modeles_llm"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    
    # Modèles disponibles
    LOCAL_MODELS: List[str] = [
        "llama3.1:8b-instruct-q4_K_M",
        "mistral:7b-instruct-v0.3", 
        "codellama:13b-instruct"
    ]
```

### Worker Local

```python
# orchestrator/app/agents/local_worker.py

import httpx
from typing import Dict, Any

class LocalLLMWorker(BaseWorker):
    """Worker pour modèles LLM locaux via Ollama."""
    
    def __init__(self, config):
        super().__init__(config)
        self.ollama_url = config.OLLAMA_BASE_URL
        self.available_models = config.LOCAL_MODELS
    
    async def can_handle_task(self, task: str, requirements: List[str]) -> bool:
        """Préfère les modèles locaux pour confidentialité."""
        
        if "local" in requirements:
            return True
        if "confidential" in requirements:
            return True
        if "fast" in requirements:
            return True  # Modèles locaux souvent plus rapides
            
        return False
    
    async def process_task(self, task: str, requirements: List[str] = None) -> Dict[str, Any]:
        """Traite avec modèle local optimal."""
        
        # Sélection modèle selon tâche
        if "code" in task.lower():
            model = "codellama:13b-instruct"
        elif "quick" in requirements:
            model = "mistral:7b-instruct-v0.3"
        else:
            model = "llama3.1:8b-instruct-q4_K_M"
        
        try:
            response = await self._call_ollama(model, task)
            
            return {
                "result": response,
                "model_used": model,
                "agent_type": "local_llm",
                "privacy": "local_processing",
                "cost": "free"
            }
            
        except Exception as e:
            return {
                "result": f"Erreur modèle local: {str(e)}",
                "success": False
            }
    
    async def _call_ollama(self, model: str, prompt: str) -> str:
        """Appel à Ollama."""
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_ctx": 4096
            }
        }
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.ollama_url}/api/generate",
                json=payload
            )
            
            result = response.json()
            return result["response"]
```

---

## 📋 Plan d'Installation Étape par Étape

### Étape 1: Préparation
```powershell
# Créer répertoire
New-Item -ItemType Directory -Path "D:\modeles_llm" -Force

# Vérifier CUDA
nvidia-smi
```

### Étape 2: Installation Ollama
```powershell
# Télécharger et installer Ollama
# https://ollama.ai/download/windows

# Configurer répertoire
$env:OLLAMA_MODELS = "D:\modeles_llm"
```

### Étape 3: Téléchargement Modèles
```powershell
# Modèles recommandés (dans l'ordre)
ollama pull llama3.1:8b-instruct-q4_K_M      # ~5GB
ollama pull mistral:7b-instruct-v0.3          # ~4.5GB  
ollama pull codellama:13b-instruct            # ~8GB
```

### Étape 4: Tests
```powershell
# Test basique
ollama run llama3.1:8b-instruct-q4_K_M "Bonjour, peux-tu me dire l'heure ?"
```

---

## 🎯 Recommandation Finale

**Pour commencer, je recommande :**

1. **Llama 3.1 8B Instruct** - Le meilleur équilibre qualité/vitesse
2. **Mistral 7B** - Excellent pour le code et très rapide
3. Si vous avez besoin de qualité max : **Llama 70B quantized**

**Avantages des modèles locaux :**
- 🔒 **Confidentialité totale** (rien ne sort de votre machine)
- 💰 **Coût zéro** (pas de frais API)
- ⚡ **Latence réduite** (pas d'appels réseau)
- 🛠️ **Contrôle total** (paramètres, prompts, etc.)

Voulez-vous que je vous aide à installer et configurer l'un de ces modèles ?
