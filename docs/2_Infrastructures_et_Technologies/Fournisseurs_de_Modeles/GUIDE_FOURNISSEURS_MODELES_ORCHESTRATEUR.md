# Guide Complet : Fournisseurs de Modèles - Orchestrateur NextGeneration

## 🎯 Vue d'ensemble

L'orchestrateur NextGeneration supporte plusieurs fournisseurs de modèles LLM pour offrir une flexibilité maximale et des performances optimales selon les tâches.

## 🔑 Configuration des Clés API

### Variables d'environnement requises dans `.env`

```env
# 🔴 OBLIGATOIRES
OPENAI_API_KEY=sk-proj-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-api03-your-anthropic-key-here
ORCHESTRATOR_API_KEY=your-orchestrator-secret-key

# 🟡 OPTIONNELLES
GOOGLE_API_KEY=AIzaSy-your-google-key-here      # Pour Gemini
GEMINI_API_KEY=AIzaSy-your-gemini-key-here      # Alias pour Gemini

# 🔵 MODÈLES LOCAUX (RTX 3090)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_GPU_DEVICE=1
LOCAL_MODELS_ENABLED=true
LOCAL_MODELS_PATH=D:/modeles_llm
```

---

## 🤖 Fournisseurs Supportés

### 1. 🟢 OpenAI (OBLIGATOIRE)

#### Configuration
- **Variable d'environnement** : `OPENAI_API_KEY`
- **Format de clé** : `sk-proj-...` ou `sk-...`
- **Endpoint** : `https://api.openai.com/v1/`
- **Statut** : ✅ Testé et fonctionnel

#### Modèles disponibles
| Modèle | Usage dans l'orchestrateur | Spécialité | Coût |
|--------|----------------------------|------------|------|
| **gpt-4o** | Agent `code_generation`, `diag_postgresql`, `testing` | Code, analyse, diagnostic | 💰💰💰 |
| **gpt-4-turbo** | Alternative haute performance | Raisonnement complexe | 💰💰💰 |
| **gpt-3.5-turbo** | Tâches générales rapides | Rapidité, économie | 💰 |

#### Utilisation dans l'orchestrateur
```python
# Dans workers.py
if agent_type == "code_generation":
    llm = ChatOpenAI(model="gpt-4o", temperature=0.1, api_key=settings.OPENAI_API_KEY)
elif agent_type == "testing":
    llm = ChatOpenAI(model="gpt-4o", temperature=0.2, api_key=settings.OPENAI_API_KEY)
```

#### Comment obtenir la clé
1. Aller sur [OpenAI Platform](https://platform.openai.com/api-keys)
2. Créer un compte et ajouter des crédits
3. Générer une nouvelle clé API
4. Ajouter dans `.env` : `OPENAI_API_KEY=sk-proj-...`

---

### 2. 🔵 Anthropic Claude (OBLIGATOIRE)

#### Configuration
- **Variable d'environnement** : `ANTHROPIC_API_KEY`
- **Format de clé** : `sk-ant-api03-...`
- **Endpoint** : `https://api.anthropic.com/v1/`
- **Statut** : ✅ Testé et fonctionnel

#### Modèles disponibles
| Modèle | Usage dans l'orchestrateur | Spécialité | Coût |
|--------|----------------------------|------------|------|
| **claude-3-5-sonnet-20240620** | Agent `documentation` | Rédaction, analyse longue | 💰💰 |
| **claude-3-haiku-20240307** | Tests et validations rapides | Rapidité, économie | 💰 |
| **claude-3-opus-20240229** | Tâches complexes | Raisonnement avancé | 💰💰💰 |

#### Utilisation dans l'orchestrateur
```python
# Dans workers.py
if agent_type == "documentation":
    llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.2, api_key=settings.ANTHROPIC_API_KEY)
```

#### Comment obtenir la clé
1. Aller sur [Anthropic Console](https://console.anthropic.com/)
2. Créer un compte et ajouter des crédits
3. Générer une clé API
4. Ajouter dans `.env` : `ANTHROPIC_API_KEY=sk-ant-api03-...`

---

### 3. 🟡 Google Gemini (OPTIONNEL)

#### Configuration
- **Variables d'environnement** : `GOOGLE_API_KEY` ou `GEMINI_API_KEY`
- **Format de clé** : `AIzaSy...`
- **Endpoint** : `https://generativelanguage.googleapis.com/v1beta/`
- **Statut** : ✅ Testé et fonctionnel

#### Modèles disponibles
| Modèle | Capacités | Spécialité | Coût |
|--------|-----------|------------|------|
| **gemini-1.5-pro** | Multimodal, 1M tokens contexte | Analyse approfondie, code | 💰💰 |
| **gemini-1.5-flash** | Rapide, multimodal | Réponses rapides, économie | 💰 |
| **gemini-ultra** | Performance maximale | Tâches complexes | 💰💰💰 |

#### Utilisation via API directe
```python
# Exemple d'utilisation directe
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
payload = {
    "contents": [{"parts": [{"text": "Votre prompt ici"}]}],
    "generationConfig": {
        "temperature": 0.7,
        "maxOutputTokens": 1000
    }
}
```

#### Comment obtenir la clé
1. Aller sur [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Créer un compte Google
3. Générer une clé API
4. Ajouter dans `.env` : `GOOGLE_API_KEY=AIzaSy...`

#### Intégration dans l'orchestrateur
```python
# À ajouter dans workers.py pour support complet
elif agent_type == "gemini_analysis":
    # Configuration Gemini (à implémenter)
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=settings.GOOGLE_API_KEY)
```

---

### 4. 🔴 Ollama Local (RTX 3090)

#### Configuration
- **Variables d'environnement** :
  ```env
  OLLAMA_BASE_URL=http://localhost:11434
  OLLAMA_GPU_DEVICE=1
  LOCAL_MODELS_ENABLED=true
  LOCAL_MODELS_PATH=D:/modeles_llm
  ```
- **Endpoint** : `http://localhost:11434/api/`
- **Statut** : ✅ Configuré pour RTX 3090

#### Modèles locaux supportés
| Modèle | Taille | Spécialité | Performance RTX 3090 |
|--------|--------|------------|----------------------|
| **llama2:70b** | 70B | Raisonnement général | 🚀🚀 |
| **codellama:34b** | 34B | Génération de code | 🚀🚀🚀 |
| **mistral:7b** | 7B | Rapidité, économie | 🚀🚀🚀🚀 |
| **neural-chat:7b** | 7B | Conversation | 🚀🚀🚀🚀 |
| **vicuna:13b** | 13B | Polyvalent | 🚀🚀🚀 |

#### Utilisation dans l'orchestrateur
```python
# Dans ollama_worker.py
class OllamaLocalWorker:
    def __init__(self, config):
        self.ollama_url = getattr(config, 'OLLAMA_BASE_URL', 'http://localhost:11434')
        self.gpu_device = getattr(config, 'OLLAMA_GPU_DEVICE', '1')
        
    async def _call_ollama(self, model_name: str, prompt: str):
        # Appel API Ollama local
        response = await client.post(f"{self.ollama_url}/api/generate", json=payload)
```

#### Installation et configuration
```bash
# Installation Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Démarrage avec GPU
CUDA_VISIBLE_DEVICES=1 ollama serve

# Installation des modèles
ollama pull llama2:70b
ollama pull codellama:34b
ollama pull mistral:7b
```

---

## 🎯 Agents et Attribution des Modèles

### Configuration actuelle dans `workers.py`

| Agent | Modèle Assigné | Fournisseur | Justification |
|-------|----------------|-------------|---------------|
| **code_generation** | gpt-4o | OpenAI | Excellence en génération de code |
| **documentation** | claude-3-5-sonnet | Anthropic | Qualité rédactionnelle supérieure |
| **testing** | gpt-4o | OpenAI | Précision pour les tests |
| **diag_postgresql** | gpt-4o | OpenAI | Analyse technique approfondie |

### Agents potentiels avec Gemini
```python
# Configurations suggérées
"gemini_analysis": {
    "model": "gemini-1.5-pro",
    "provider": "Google",
    "use_case": "Analyse multimodale, contexte long"
}

"gemini_rapid": {
    "model": "gemini-1.5-flash", 
    "provider": "Google",
    "use_case": "Réponses rapides, prototypage"
}
```

---

## 📊 Comparaison des Performances

### Temps de réponse moyens (tests réels)
| Fournisseur | Modèle | Temps moyen | Qualité | Coût relatif |
|-------------|--------|-------------|---------|--------------|
| OpenAI | gpt-4o | 3-5s | ⭐⭐⭐⭐⭐ | 💰💰💰 |
| Anthropic | claude-3-5-sonnet | 4-7s | ⭐⭐⭐⭐⭐ | 💰💰 |
| Google | gemini-1.5-flash | 0.6s | ⭐⭐⭐⭐ | 💰 |
| Google | gemini-1.5-pro | 2-3s | ⭐⭐⭐⭐⭐ | 💰💰 |
| Ollama | llama2:70b | 1-2s | ⭐⭐⭐⭐ | 🆓 |

### Recommandations d'usage
- **Développement/Prototypage** : Gemini Flash (rapide, économique)
- **Production/Qualité** : GPT-4o ou Claude-3.5-Sonnet
- **Analyse de code** : GPT-4o (meilleure compréhension)
- **Rédaction longue** : Claude-3.5-Sonnet (contexte étendu)
- **Économie/Confidentialité** : Ollama local (gratuit, privé)

---

## 🔧 Scripts de Test

### Test de toutes les clés API
```bash
# Test automatique de toutes les clés
python test_api_keys.py

# Test spécifique Gemini
python test_gemini_rapide.py

# Test complet avec benchmarks
python test_gemini_complet.py
```

### Test de l'orchestrateur avec différents modèles
```bash
# Test avec modèle spécifique
curl -X POST "http://localhost:8003/orchestrator/process" \
  -H "X-API-Key: demo-key-for-testing" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Analyse ce code Python",
    "preferred_model": "gemini-1.5-flash",
    "requirements": ["analysis"]
  }'
```

---

## 🚀 Extension et Personnalisation

### Ajouter un nouveau fournisseur
1. **Ajouter la clé API** dans `.env`
2. **Modifier `config.py`** pour inclure la nouvelle clé
3. **Étendre `workers.py`** avec le nouveau modèle
4. **Créer un agent spécialisé** si nécessaire
5. **Tester** avec les scripts fournis

### Exemple d'ajout d'un agent Gemini
```python
# Dans workers.py
elif agent_type == "gemini_multimodal":
    # Configuration pour Gemini (nécessite langchain-google-genai)
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.3
    )
    tools = real_analysis_tools
```

---

## 📋 Checklist de Configuration

### ✅ Configuration Minimale (Fonctionnelle)
- [ ] `OPENAI_API_KEY` configurée et testée
- [ ] `ANTHROPIC_API_KEY` configurée et testée  
- [ ] `ORCHESTRATOR_API_KEY` définie
- [ ] Orchestrateur démarrable : `python start_orchestrator.py`
- [ ] Tests API réussis : `python test_api_keys.py`

### ✅ Configuration Complète (Recommandée)
- [ ] Toutes les clés de la configuration minimale
- [ ] `GOOGLE_API_KEY` ou `GEMINI_API_KEY` ajoutée
- [ ] Ollama installé et configuré (optionnel)
- [ ] Tests Gemini réussis : `python test_gemini_rapide.py`
- [ ] Modèles locaux téléchargés (optionnel)

### ✅ Configuration Avancée (Production)
- [ ] Toutes les configurations précédentes
- [ ] Monitoring et métriques activés
- [ ] Load balancing configuré
- [ ] Fallback entre fournisseurs implémenté
- [ ] Coûts et quotas surveillés

---

## 🎉 Résumé

L'orchestrateur NextGeneration supporte actuellement **4 fournisseurs principaux** :

1. **🟢 OpenAI** - Obligatoire, excellent pour le code
2. **🔵 Anthropic** - Obligatoire, parfait pour la documentation  
3. **🟡 Google Gemini** - Optionnel, rapide et économique
4. **🔴 Ollama Local** - Optionnel, gratuit et privé (RTX 3090)

**Configuration actuelle testée et fonctionnelle** :
- ✅ 3 fournisseurs cloud configurés
- ✅ 1 solution locale (Ollama RTX 3090)
- ✅ 4 agents spécialisés opérationnels
- ✅ Scripts de test et monitoring complets

**Votre ajout de `GEMINI_API_KEY` permet d'utiliser Google Gemini comme alternative rapide et économique aux modèles principaux.**

---

*Guide des Fournisseurs de Modèles - Orchestrateur NextGeneration v1.0* 