# 🎮 CONTEXTE CONFIGURATION DOUBLE GPU RTX 3090 - MODÈLES LLM LOCAUX
## Guide Contexte et Workflow pour Assistants IA

---

**Projet :** NextGeneration Multi-Agent System  
**Configuration :** Double GPU RTX 3090 (Port Secondaire)  
**Date :** 17 Juin 2025  
**Version :** 1.0 CONTEXTE COMPLET  
**Statut :** Document de Référence Principal  

---

## 🎯 OBJECTIF PRINCIPAL

**Utiliser des modèles LLM locaux pour alimenter les assistants du système multi-agent NextGeneration** en exploitant la configuration double GPU RTX 3090 optimisée pour les performances IA.

### 🎮 **Vision Système**
- **Indépendance** : Modèles LLM hébergés localement, aucune dépendance cloud
- **Performance** : Exploitation optimale de la RTX 3090 (24GB VRAM)
- **Flexibilité** : Sélection dynamique de modèles selon les besoins des assistants
- **Évolutivité** : Capacité d'ajout de nouveaux modèles selon les besoins

---

## 🏗️ ARCHITECTURE CONFIGURATION DOUBLE GPU

### 🎮 **Configuration Matérielle Actuelle**

```
┌─────────────────────────────────────────────────────────────┐
│                    CONFIGURATION SYSTÈME                    │
├─────────────────────────────────────────────────────────────┤
│  🎮 GPU Principal (Port Secondaire - Bus PCI 1)           │
│      ├─ NVIDIA GeForce RTX 3090                            │
│      ├─ VRAM: 24GB GDDR6X                                  │
│      ├─ Compute Capability: SM_86                          │
│      └─ Usage: IA/ML EXCLUSIF (SuperWhisper V6 Standards)  │
│                                                             │
│  🎮 GPU Secondaire (Port Principal - Bus PCI 0)           │
│      ├─ NVIDIA GeForce RTX 5060 Ti                         │
│      ├─ VRAM: 16GB GDDR6X                                  │
│      ├─ Compute Capability: SM_120                         │
│      └─ Usage: INTERDIT pour IA (Incompatibilité CUDA)    │
│                                                             │
│  💾 Stockage Modèles LLM                                   │
│      └─ Répertoire: D:\modeles_llm\                        │
└─────────────────────────────────────────────────────────────┘
```

### 🔧 **Mapping GPU et Standards**

```python
# Configuration GPU OBLIGATOIRE pour NextGeneration
os.environ['CUDA_VISIBLE_DEVICES'] = '1'        # RTX 3090 (Bus PCI 1) UNIQUEMENT
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'  # Force ordre bus physique
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:1024'

# Après mapping CUDA:
# CUDA:0 → RTX 3090 (24GB) - GPU IA Principal
# RTX 5060 Ti → INVISIBLE et INUTILISABLE (Standards Projet)
```

---

## 📚 RÉFÉRENCES DOCUMENTAIRES OBLIGATOIRES

### � **Documentation Standards GPU (LECTURE OBLIGATOIRE)**

| 📖 **Document** | 🎯 **Contenu** | 💡 **Usage** |
|-----------------|----------------|--------------|
| **[standards_gpu_rtx3090_definitifs.md](./standards_gpu_rtx3090_definitifs.md)** | Standards GPU absolus du projet | Configuration code OBLIGATOIRE |
| **[guide_developpement_gpu_rtx3090.md](./guide_developpement_gpu_rtx3090.md)** | Guide développement pratique | Workflow développement |
| **[RTX_5060_CUDA_PYTORCH_INCOMPATIBILITE.md](./RTX_5060_CUDA_PYTORCH_INCOMPATIBILITE.md)** | Problématique RTX 5060 | Justification exclusion RTX 5060 |

### � **Documentation Configuration Ollama (RÉFÉRENCE TECHNIQUE)**

| 📖 **Document** | 🎯 **Contenu** | 💡 **Usage** |
|-----------------|----------------|--------------|
| **[GUIDE_EXPLOITATION_OLLAMA_RTX3090_OPTIMISE.md](./GUIDE_EXPLOITATION_OLLAMA_RTX3090_OPTIMISE.md)** | Exploitation optimale Ollama | Configuration modèles locaux |
| **[CONFIGURATION_OLLAMA_RTX3090_NEXTGENERATION.md](./CONFIGURATION_OLLAMA_RTX3090_NEXTGENERATION.md)** | Configuration spécifique projet | Paramétrage Ollama |

### 📋 **Scripts et Outils de Validation**

| 🔧 **Script** | 🎯 **Fonction** | 💡 **Utilisation** |
|---------------|----------------|-------------------|
| **[monitor_rtx3090.py](./monitor_rtx3090.py)** | Monitoring RTX 3090 temps réel | Surveillance performances |
| **[selecteur_ollama_rtx3090.py](./selecteur_ollama_rtx3090.py)** | Sélection automatique modèles | Optimisation usage modèles |
| **[test_configuration_multi_gpu.py](./test_configuration_multi_gpu.py)** | Validation configuration | Tests configuration système |

---

## 🗂️ MODÈLES LLM LOCAUX - STOCKAGE ET GESTION

### **📁 Localisation des Modèles**

```
Répertoire Principal : D:\modeles_llm\
│
├── ollama\                     # Modèles Ollama (format .gguf)
│   ├── mixtral-8x7b\          # Modèle qualité maximum (26GB)
│   ├── qwen-coder-32b\        # Spécialiste code (19GB)
│   ├── llama3-8b-instruct\    # Usage quotidien (6.6GB)
│   ├── nous-hermes-7b\        # Ultra rapide (4.1GB)
│   └── qwen2.5-coder-1.5b\    # Tests express (1GB)
│
├── transformers\              # Modèles HuggingFace
│   ├── microsoft-dialoGPT\    # Modèles conversationnels
│   ├── codellama\             # Modèles spécialisés code
│   └── mistral-7b\            # Modèles Mistral
│
├── custom\                    # Modèles personnalisés
│   ├── fine-tuned\            # Modèles fine-tunés
│   └── specialized\           # Modèles spécialisés métier
│
└── cache\                     # Cache modèles temporaires
    ├── downloads\             # Téléchargements en cours
    └── converted\             # Modèles convertis
```

### **📊 Modèles Actuellement Disponibles (Validés RTX 3090)**

| Modèle | Taille | VRAM Requise | Usage Recommandé | Performance |
|--------|--------|--------------|------------------|-------------|
| **mixtral-8x7b:latest** | 26GB | 26GB (100% RTX 3090) | Analyses complexes | ⭐⭐⭐⭐⭐ |
| **qwen-coder-32b:latest** | 19GB | 19GB (80% RTX 3090) | Développement code | ⭐⭐⭐⭐⭐ |
| **llama3:8b-instruct-q6_k** | 6.6GB | 6.6GB (28% RTX 3090) | Usage quotidien | ⭐⭐⭐⭐ |
| **nous-hermes-2-mistral-7b-dpo** | 4.1GB | 4.1GB (17% RTX 3090) | Réponses rapides | ⭐⭐⭐⭐ |
| **qwen2.5-coder:1.5b** | 1GB | 1GB (4% RTX 3090) | Tests express | ⭐⭐⭐ |

---

## ⚠️ PROCÉDURE OBLIGATOIRE POUR NOUVEAUX MODÈLES

### **🔍 Étape 1 : Consultation Liste Modèles Disponibles**

**AVANT** tout téléchargement, **OBLIGATOIREMENT** consulter :

```bash
# Lister modèles Ollama disponibles
ollama list

# Rechercher modèles par critère
ollama search [nom_modele]

# Afficher informations détaillées
ollama show [nom_modele]
```

### **📋 Étape 2 : Validation Compatibilité RTX 3090**

**Critères obligatoires** :
- **VRAM requise** ≤ 24GB (RTX 3090)
- **Format compatible** : GGUF, GGML, ou Transformers
- **Architecture supportée** : Llama, Mistral, Qwen, etc.
- **Quantization** : Q4_K_M minimum (équilibre qualité/taille)

### **📥 Étape 3 : Téléchargement Autorisé**

```bash
# Téléchargement Ollama (recommandé)
ollama pull [nom_modele]

# Exemple
ollama pull llama3.1:8b-instruct-q4_k_m
```

### **✅ Étape 4 : Test et Validation**

```python
# Test avec script de validation
python selecteur_ollama_rtx3090.py

# Test performance spécifique
python test_nouveau_modele.py [nom_modele]
```

---

## 🚀 INTÉGRATION AVEC ASSISTANTS NEXTGENERATION

### **🤖 Architecture Assistants Locaux**

```python
# Configuration assistant avec modèle local
class AssistantLocal:
    def __init__(self, model_name="llama3:8b-instruct-q6_k"):
        # Configuration RTX 3090 obligatoire
        os.environ['CUDA_VISIBLE_DEVICES'] = '1'
        self.model_name = model_name
        self.ollama_url = "http://localhost:11434"
        
    async def process_query(self, query: str, context: dict = None):
        """Traite une requête avec modèle local RTX 3090"""
        # Sélection modèle optimal selon contexte
        optimal_model = self.select_optimal_model(query, context)
        
        # Traitement sur RTX 3090
        response = await self.call_local_model(optimal_model, query)
        
        return response
```

### **⚡ Sélection Automatique de Modèles**

```python
# Intégration sélecteur intelligent
from selecteur_ollama_rtx3090 import RTX3090OllamaSelector

class SmartAssistant:
    def __init__(self):
        self.selector = RTX3090OllamaSelector()
        
    async def intelligent_response(self, task: str, priority: str = "auto"):
        """Réponse avec sélection automatique de modèle"""
        # Analyse tâche et sélection modèle optimal
        analysis = self.selector.analyze_task(task, priority)
        
        # Traitement avec modèle sélectionné
        result = await self.selector.process_task(task, priority)
        
        return result
```

---

## 📊 WORKFLOWS OPTIMISÉS PAR USAGE

### **🔧 Développement & Code**

```python
# Assistant spécialisé développement
async def code_assistant(query: str):
    """Assistant développement avec Qwen-Coder 32B"""
    model = "qwen-coder-32b:latest"  # 19GB VRAM
    # Spécialisé : Python, JavaScript, Debug, Architecture
    
    enhanced_prompt = f"""
    Tu es un expert développeur sur RTX 3090.
    Contexte: Projet NextGeneration multi-agent.
    Standards: SuperWhisper V6 avec GPU RTX 3090.
    
    Tâche: {query}
    
    Fournis du code propre, documenté et optimisé.
    """
    
    return await call_ollama_model(model, enhanced_prompt)
```

### **🧠 Analyses Complexes**

```python
# Assistant analyse avec Mixtral 8x7B
async def analysis_assistant(content: str):
    """Assistant analyse avec Mixtral (qualité maximum)"""
    model = "mixtral-8x7b:latest"  # 26GB VRAM (100% RTX 3090)
    
    enhanced_prompt = f"""
    Tu es un expert analyste utilisant toute la capacité RTX 3090.
    Contexte: Système multi-agent NextGeneration.
    
    Analyse approfondie: {content}
    
    Fournis une analyse détaillée, structurée et argumentée.
    """
    
    return await call_ollama_model(model, enhanced_prompt)
```

### **⚡ Réponses Rapides**

```python
# Assistant rapide avec Nous-Hermes
async def quick_assistant(question: str):
    """Assistant ultra-rapide pour interactions en temps réel"""
    model = "nous-hermes-2-mistral-7b-dpo:latest"  # 4.1GB VRAM
    
    return await call_ollama_model(model, question)
```

---

## 💾 GESTION MODÈLES LLM LOCAUX

### 📁 **Répertoire de Stockage Principal**

```
D:\modeles_llm\
├── README.md                           # Documentation répertoire
├── modeles_ollama\                     # Modèles Ollama (gestion automatique)
│   ├── mistral-7b-instruct\
│   ├── llama3-8b-instruct\
│   ├── qwen-coder-32b\
│   ├── mixtral-8x7b\
│   └── nous-hermes-2-mistral-7b-dpo\
├── modeles_huggingface\               # Modèles HuggingFace manuels
│   ├── microsoft--DialoGPT-medium\
│   ├── sentence-transformers--all-MiniLM-L6-v2\
│   └── ... autres modèles HF
├── modeles_custom\                    # Modèles personnalisés/fine-tunés
│   └── (réservé pour développements futurs)
└── cache\                             # Cache temporaire modèles
    ├── tokenizers\
    ├── transformers\
    └── ollama_cache\
```

### 📋 **Modèles Disponibles et Validés**

#### 🦙 **Modèles Ollama (Prêts à l'Usage)**
```yaml
modeles_ollama_valides:
  speed_model:
    nom: "nous-hermes-2-mistral-7b-dpo:latest"
    vram: "4.1GB"
    vitesse: "⚡ Ultra-rapide (6 tokens/sec)"
    usage: "Réponses rapides, brainstorming, dev"
    
  quality_model:
    nom: "mixtral-8x7b:latest"
    vram: "26GB (100% RTX 3090)"
    vitesse: "🏆 Qualité max (1 token/sec)"
    usage: "Analyses complexes, raisonnement avancé"
    
  code_model:
    nom: "qwen-coder-32b:latest"
    vram: "19GB (80% RTX 3090)"
    vitesse: "🔧 Spécialisé (2 tokens/sec)"
    usage: "Génération code, debug, architecture"
    
  daily_model:
    nom: "llama3:8b-instruct-q6_k"
    vram: "6.6GB (28% RTX 3090)"
    vitesse: "📱 Équilibré (4 tokens/sec)"
    usage: "Usage quotidien, chat, résumés"
    
  mini_model:
    nom: "qwen2.5-coder:1.5b"
    vram: "1GB (4% RTX 3090)"
    vitesse: "🧪 Express (10 tokens/sec)"
    usage: "Tests rapides, prototypage"
```

#### 🤗 **Modèles HuggingFace (Configuration Manuelle)**
```yaml
modeles_huggingface_disponibles:
  conversational:
    nom: "microsoft/DialoGPT-medium"
    taille: "345MB"
    usage: "Chat conversationnel"
    
  embeddings:
    nom: "sentence-transformers/all-MiniLM-L6-v2"
    taille: "80MB"
    usage: "Embeddings texte, similarity"
    
  multilingual:
    nom: "Helsinki-NLP/opus-mt-fr-en"
    taille: "300MB"
    usage: "Traduction FR-EN"
```

---

## 🔄 WORKFLOW D'UTILISATION POUR ASSISTANTS

### 🤖 **Intégration avec Système Multi-Agent**

```python
# Exemple d'intégration dans un assistant NextGeneration
class AssistantAvecModelesLocaux:
    """Assistant utilisant modèles LLM locaux via RTX 3090"""
    
    def __init__(self):
        # Configuration GPU RTX 3090 OBLIGATOIRE
        os.environ['CUDA_VISIBLE_DEVICES'] = '1'
        os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
        
        self.model_selector = RTX3090OllamaSelector()
        self.models_path = "D:\\modeles_llm"
        
    async def process_request(self, task: str, priority: str = "auto"):
        """Traite une requête avec sélection automatique de modèle"""
        
        # Sélection automatique selon tâche
        analysis = self.model_selector.analyze_task(task, priority)
        selected_model = analysis["recommended_model"]
        
        # Traitement avec modèle optimal
        response = await self.model_selector.process_task(
            task=task,
            priority=priority,
            model=selected_model
        )
        
        return {
            "response": response["content"],
            "model_used": response["model"],
            "performance": response["performance"],
            "confidence": analysis["confidence"]
        }
```

### 🎯 **Sélection Automatique par Type d'Assistant**

```python
# Mapping assistants → modèles optimaux
ASSISTANT_MODEL_MAPPING = {
    "peer_review_agent": "quality_model",      # Mixtral-8x7B pour analyses
    "code_agent": "code_model",                # Qwen-Coder pour développement
    "documentation_agent": "daily_model",      # Llama3 pour rédaction
    "security_agent": "quality_model",         # Mixtral pour analyses sécurité
    "performance_agent": "code_model",         # Qwen-Coder pour optimisations
    "chat_agent": "speed_model",              # Nous-Hermes pour rapidité
    "test_agent": "mini_model"                # Qwen-Mini pour tests rapides
}
```

---

## 📥 PROCÉDURE AJOUT NOUVEAUX MODÈLES

### ⚠️ **RÈGLE OBLIGATOIRE - CONSULTATION PRÉALABLE**

> **🚨 ATTENTION : Avant de télécharger un nouveau modèle, vous DEVEZ consulter la liste des modèles disponibles pour éviter les doublons et valider la compatibilité.**

### 📋 **Étapes d'Ajout d'un Nouveau Modèle**

#### **1. Consultation Obligatoire**
```bash
# Lister modèles Ollama disponibles
ollama list

# Lister modèles locaux existants
ls -la D:\modeles_llm\modeles_ollama\

# Vérifier espace disque disponible
df -h D:\
```

#### **2. Recherche et Validation**
```bash
# Rechercher modèles compatibles
ollama search <nom_modele>

# Vérifier taille et compatibilité RTX 3090
ollama show <nom_modele>
```

#### **3. Téléchargement Sécurisé**
```bash
# Télécharger avec validation GPU
CUDA_VISIBLE_DEVICES=1 ollama pull <nom_modele>

# Exemple
CUDA_VISIBLE_DEVICES=1 ollama pull codellama:7b-instruct
```

#### **4. Test et Validation**
```python
# Script de test nouveau modèle
async def test_nouveau_modele(model_name: str):
    """Test complet nouveau modèle sur RTX 3090"""
    
    # Test basique
    response = await process_with_model(
        model=model_name,
        prompt="Test RTX 3090 NextGeneration",
        max_tokens=100
    )
    
    # Validation performance
    benchmark = await benchmark_model_performance(model_name)
    
    return {
        "status": "validated" if benchmark["success"] else "failed",
        "vram_usage": benchmark["vram_gb"],
        "tokens_per_sec": benchmark["speed"],
        "compatibility": "rtx3090_compatible"
    }
```

#### **5. Documentation et Intégration**
```python
# Ajouter dans selecteur_ollama_rtx3090.py
nouveaux_modeles = {
    "custom_model": {
        "name": "nom-modele:version",
        "vram_gb": 8.5,
        "tokens_per_sec": 3,
        "quality_score": 8,
        "speciality": "Usage spécialisé",
        "use_cases": ["custom", "specific", "domain"],
        "temperature_optimal": 0.4,
        "max_tokens_optimal": 1024
    }
}
```

---

## 🛠️ OUTILS DE GESTION ET MONITORING

### 📊 **Scripts de Monitoring Disponibles**

```python
# Monitoring utilisation modèles en temps réel
from monitor_rtx3090 import RTX3090Monitor

monitor = RTX3090Monitor()
stats = monitor.get_model_usage_stats()

print(f"Modèle actif: {stats['active_model']}")
print(f"VRAM utilisée: {stats['vram_used_gb']:.1f}GB / 24GB")
print(f"Température: {stats['temperature']}°C")
print(f"Utilisation: {stats['gpu_utilization']}%")
```

### 🔧 **Maintenance et Optimisation**

```bash
# Nettoyage cache modèles
ollama prune

# Libération mémoire GPU
python -c "
import torch
torch.cuda.empty_cache()
print('✅ Cache GPU nettoyé')
"

# Vérification santé modèles
python test_configuration_multi_gpu.py
```

---

## 🎯 EXEMPLES D'USAGE PRATIQUES

### 🤖 **Assistant Peer-Review (Qualité Maximale)**
```python
# Utilise Mixtral-8x7B pour analyses approfondies
peer_review_agent = AssistantAvecModelesLocaux()

review = await peer_review_agent.process_request(
    task="Analyser ce code Python et identifier les vulnérabilités de sécurité",
    priority="quality"  # Force Mixtral-8x7B
)

print(f"Review: {review['response']}")
print(f"Modèle utilisé: {review['model_used']}")
```

### 💻 **Assistant Code (Spécialisé Développement)**
```python
# Utilise Qwen-Coder-32B pour génération code
code_agent = AssistantAvecModelesLocaux()

code = await code_agent.process_request(
    task="Génère une classe Python pour gérer une base de données PostgreSQL",
    priority="code"  # Force Qwen-Coder-32B
)

print(f"Code généré: {code['response']}")
```

### ⚡ **Assistant Chat (Ultra-Rapide)**
```python
# Utilise Nous-Hermes pour réponses instantanées
chat_agent = AssistantAvecModelesLocaux()

response = await chat_agent.process_request(
    task="Salut ! Comment ça va ?",
    priority="speed"  # Force Nous-Hermes
)

print(f"Réponse: {response['response']}")
```

---

## 📋 CHECKLIST DE DÉPLOIEMENT

### ✅ **Validation Configuration Système**
- [ ] RTX 3090 détectée sur Bus PCI 1
- [ ] RTX 5060 Ti exclue (Bus PCI 0)
- [ ] Configuration GPU standards respectée
- [ ] Répertoire `D:\modeles_llm` accessible
- [ ] Ollama service démarré et fonctionnel

### ✅ **Validation Modèles Locaux**
- [ ] Modèles Ollama listés et fonctionnels
- [ ] Sélecteur automatique configuré
- [ ] Tests performance RTX 3090 réussis
- [ ] Monitoring actif et opérationnel

### ✅ **Intégration Assistants**
- [ ] Mapping assistants → modèles défini
- [ ] Scripts d'intégration validés
- [ ] Procédures ajout nouveaux modèles documentées
- [ ] Workflow complet testé et fonctionnel

---

## 🚀 PROCHAINES ÉTAPES RECOMMANDÉES

1. **Tester l'intégration** avec vos assistants existants
2. **Calibrer les paramètres** selon vos besoins spécifiques
3. **Monitorer les performances** en conditions réelles d'usage
4. **Documenter les retours** d'expérience pour optimisations futures
5. **Évaluer l'ajout** de modèles spécialisés selon besoins émergents

---

**Ce document constitue la référence principale pour l'utilisation des modèles LLM locaux dans votre système multi-agent NextGeneration. Consultez régulièrement les documents de référence cités pour maintenir la conformité avec les standards du projet.**

🎮✨ **Configuration Double GPU RTX 3090 + Modèles Locaux = Puissance IA Maximale !**
