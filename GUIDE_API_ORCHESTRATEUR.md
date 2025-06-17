# Guide Complet : Configuration et Utilisation des APIs LLM

## 🎯 Vue d'ensemble

Ce guide explique comment :
- ✅ Configurer et tester les clés API (OpenAI, Anthropic, Google Gemini)
- 🚀 Démarrer et utiliser l'orchestrateur multi-agent
- 🔧 Tester les APIs métiers
- 🛠️ Développer des agents personnalisés

## 📋 1. Configuration des Clés API

### Clés requises dans `.env` :

```env
# LLMs principaux
OPENAI_API_KEY=sk-proj-... (obligatoire)
ANTHROPIC_API_KEY=sk-ant-api03-... (obligatoire)
GOOGLE_API_KEY=AIzaSy... (optionnel)

# Sécurité orchestrateur
ORCHESTRATOR_API_KEY=your-secret-key
```

### Comment obtenir les clés :

1. **OpenAI** : https://platform.openai.com/api-keys
2. **Anthropic** : https://console.anthropic.com/
3. **Google Gemini** : https://makersuite.google.com/app/apikey

### Test des clés :

```powershell
# Test toutes les clés
python test_api_keys.py

# Test spécifique Gemini
python test_gemini_api.py
```

## 🚀 2. Démarrage de l'Orchestrateur

### Méthode 1 : Script Python (Recommandé pour développement)

```powershell
# Démarrage simple
python start_orchestrator.py

# L'orchestrateur sera disponible sur http://localhost:8002
```

### Méthode 2 : Docker (Production)

```powershell
# Démarrage complet
docker-compose up -d

# Logs
docker-compose logs -f orchestrator
```

### Vérification du démarrage :

```powershell
# Test santé
curl http://localhost:8002/health

# Test configuration
curl http://localhost:8002/
```

## 🔧 3. Test des APIs Métiers

### A. Test de traitement simple

```powershell
# Test POST avec curl
curl -X POST "http://localhost:8002/orchestrator/process" `
  -H "Content-Type: application/json" `
  -H "X-API-Key: demo-key-for-testing" `
  -d '{"task": "Écris un bonjour en français", "requirements": []}'
```

### B. Test avec script Python

```python
import httpx
import json

def test_orchestrator_process():
    """Test l'endpoint de traitement principal."""
    
    url = "http://localhost:8002/orchestrator/process"
    headers = {
        "X-API-Key": "demo-key-for-testing",
        "Content-Type": "application/json"
    }
    
    # Tâche simple
    payload = {
        "task": "Génère un petit poème en français sur l'IA",
        "requirements": [],
        "preferred_model": "gpt-4"  # ou "claude-3-sonnet", "gemini-pro"
    }
    
    try:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Succès!")
            print(f"📝 Résultat: {result.get('result', 'Pas de résultat')}")
            print(f"🤖 Agent utilisé: {result.get('agent_used', 'N/A')}")
            print(f"⏱️ Temps: {result.get('execution_time', 'N/A')}s")
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
    
    except Exception as e:
        print(f"❌ Erreur: {e}")

# Exécution
test_orchestrator_process()
```

### C. Test avec différents modèles

```python
# Test OpenAI GPT-4
payload_gpt = {
    "task": "Explique l'informatique quantique en 2 phrases",
    "preferred_model": "gpt-4"
}

# Test Anthropic Claude
payload_claude = {
    "task": "Résume les avantages du cloud computing",
    "preferred_model": "claude-3-sonnet"
}

# Test Google Gemini
payload_gemini = {
    "task": "Écris un haiku sur la technologie",
    "preferred_model": "gemini-pro"
}
```

## 🛠️ 4. Développement d'Agents Personnalisés

### Structure d'un Agent

```python
# orchestrator/app/workers/my_custom_agent.py

from typing import Dict, Any, List
from .base_worker import BaseWorker

class MyCustomAgent(BaseWorker):
    """Agent personnalisé pour traiter des tâches spécialisées."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.agent_type = "custom_specialist"
        self.supported_tasks = ["custom_task", "specialized_analysis"]
    
    async def can_handle_task(self, task: str, requirements: List[str]) -> bool:
        """Détermine si cet agent peut traiter la tâche."""
        task_lower = task.lower()
        
        # Conditions personnalisées
        if any(keyword in task_lower for keyword in ["analyse", "rapport", "données"]):
            return True
        
        if "custom" in requirements:
            return True
            
        return False
    
    async def process_task(self, task: str, requirements: List[str] = None) -> Dict[str, Any]:
        """Traite la tâche avec la logique métier spécialisée."""
        
        try:
            # 1. Analyse de la tâche
            analysis = await self._analyze_task(task)
            
            # 2. Traitement spécialisé
            if "analyse" in task.lower():
                result = await self._perform_analysis(task)
            elif "rapport" in task.lower():
                result = await self._generate_report(task)
            else:
                result = await self._default_processing(task)
            
            # 3. Retour structuré
            return {
                "result": result,
                "agent_type": self.agent_type,
                "analysis": analysis,
                "confidence": 0.9,
                "metadata": {
                    "processing_method": "specialized",
                    "task_category": self._categorize_task(task)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erreur dans MyCustomAgent: {e}")
            return {
                "result": f"Erreur lors du traitement: {str(e)}",
                "success": False,
                "agent_type": self.agent_type
            }
    
    async def _analyze_task(self, task: str) -> Dict[str, Any]:
        """Analyse préliminaire de la tâche."""
        return {
            "complexity": "medium",
            "estimated_time": 30,
            "requires_llm": True
        }
    
    async def _perform_analysis(self, task: str) -> str:
        """Logique d'analyse spécialisée."""
        # Utilisation du LLM configuré
        prompt = f"""
        Effectue une analyse détaillée de la demande suivante :
        {task}
        
        Fournis une réponse structurée avec :
        - Analyse du problème
        - Recommandations
        - Conclusion
        """
        
        return await self._call_llm(prompt)
    
    async def _generate_report(self, task: str) -> str:
        """Génération de rapport spécialisé."""
        prompt = f"""
        Génère un rapport professionnel pour :
        {task}
        
        Format demandé :
        # Rapport d'Analyse
        
        ## Contexte
        [Description du contexte]
        
        ## Analyse
        [Analyse détaillée]
        
        ## Recommandations
        [Recommandations concrètes]
        
        ## Conclusion
        [Conclusion et prochaines étapes]
        """
        
        return await self._call_llm(prompt)
    
    async def _default_processing(self, task: str) -> str:
        """Traitement par défaut."""
        prompt = f"Traite cette tâche de manière professionnelle : {task}"
        return await self._call_llm(prompt)
    
    def _categorize_task(self, task: str) -> str:
        """Catégorise la tâche."""
        task_lower = task.lower()
        
        if "analyse" in task_lower:
            return "analysis"
        elif "rapport" in task_lower:
            return "reporting"
        elif "données" in task_lower:
            return "data_processing"
        else:
            return "general"
```

### Enregistrement de l'Agent

```python
# orchestrator/app/core/orchestrator.py

# Ajouter dans la méthode __init__ de OrchestrationService :

from ..workers.my_custom_agent import MyCustomAgent

async def _initialize_workers(self):
    """Initialise tous les workers disponibles."""
    
    # Agents existants
    self.workers.append(GeneralAgent(self.config))
    self.workers.append(CodeAgent(self.config))
    self.workers.append(AnalysisAgent(self.config))
    
    # Nouvel agent personnalisé
    self.workers.append(MyCustomAgent(self.config))
    
    self.logger.info(f"Initialized {len(self.workers)} workers")
```

### Test de l'Agent Personnalisé

```python
# test_custom_agent.py

import httpx

def test_custom_agent():
    """Test de l'agent personnalisé."""
    
    url = "http://localhost:8002/orchestrator/process"
    headers = {
        "X-API-Key": "demo-key-for-testing",
        "Content-Type": "application/json"
    }
    
    # Tâche qui déclenche l'agent personnalisé
    payload = {
        "task": "Effectue une analyse détaillée de l'impact de l'IA sur le marché du travail",
        "requirements": ["custom", "analysis"]
    }
    
    with httpx.Client(timeout=120.0) as client:
        response = client.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Agent utilisé: {result.get('agent_used')}")
        print(f"📊 Résultat: {result.get('result')}")
    else:
        print(f"❌ Erreur: {response.text}")

if __name__ == "__main__":
    test_custom_agent()
```

## 📊 5. Monitoring et Débogage

### Logs de l'orchestrateur

```powershell
# Logs en temps réel
python start_orchestrator.py

# Les logs montrent :
# - Sélection d'agent
# - Temps d'exécution  
# - Erreurs
# - Performances
```

### Endpoint de debug

```powershell
# Statut détaillé
curl "http://localhost:8002/orchestrator/status" `
  -H "X-API-Key: demo-key-for-testing"

# Liste des agents disponibles
curl "http://localhost:8002/orchestrator/agents" `
  -H "X-API-Key: demo-key-for-testing"
```

## 🎉 6. Exemples Complets d'Utilisation

### Exemple 1 : Analyse de données

```json
{
  "task": "Analyse les tendances du marché cryptocurrency pour Bitcoin et Ethereum sur les 6 derniers mois",
  "requirements": ["analysis", "data"],
  "preferred_model": "gpt-4"
}
```

### Exemple 2 : Génération de code

```json
{
  "task": "Crée une fonction Python pour calculer la moyenne mobile d'une série temporelle",
  "requirements": ["code", "python"],
  "preferred_model": "claude-3-sonnet"
}
```

### Exemple 3 : Rédaction créative

```json
{
  "task": "Écris un article de blog sur les meilleures pratiques en cybersécurité pour les PME",
  "requirements": ["creative", "business"],
  "preferred_model": "gemini-pro"
}
```

## 🔧 7. Résolution de Problèmes

### Problèmes courants

1. **Clé API invalide**
   ```
   Solution: Vérifiez vos clés avec test_api_keys.py
   ```

2. **Orchestrateur ne démarre pas**
   ```
   Solution: Vérifiez les dépendances avec pip install -r requirements.txt
   ```

3. **Timeout lors des requêtes**
   ```
   Solution: Augmentez les timeouts dans la configuration
   ```

4. **Agent non trouvé**
   ```
   Solution: Vérifiez l'enregistrement dans orchestrator.py
   ```

### Scripts de diagnostic

```powershell
# Test complet du système
python test_orchestrator_complete.py

# Test spécifique d'un modèle
python test_gemini_api.py
python test_api_keys.py
```

---

## 📚 Ressources Supplémentaires

- **Documentation OpenAI** : https://platform.openai.com/docs
- **Documentation Anthropic** : https://docs.anthropic.com/
- **Documentation Gemini** : https://ai.google.dev/docs
- **FastAPI** : https://fastapi.tiangolo.com/
- **Docker** : https://docs.docker.com/

---

*Ce guide vous permet de maîtriser complètement l'orchestrateur multi-agent NextGeneration !* 🚀
