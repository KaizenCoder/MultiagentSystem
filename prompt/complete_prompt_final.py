"""
Script final pour compléter le prompt Agent Factory Pattern
"""

def generate_implementation_phases():
    """Génère les phases d'implémentation"""
    
    phases = '''

---

## 🔄 **PHASES D'IMPLÉMENTATION OBLIGATOIRES**

### **Phase 1 : Fondations (OBLIGATOIRE)**

**Durée estimée** : 2-3 heures

**Étapes** :
1. **Créer la structure de dossiers** :
   ```bash
   mkdir -p orchestrator/app/agents/templates
   mkdir -p orchestrator/app/config
   ```

2. **Implémenter BaseAgent** (code obligatoire fourni)
3. **Implémenter AgentTemplate** (code obligatoire fourni)
4. **Créer les templates JSON** (obligatoires)

**Vérification** :
```python
# Test de la phase 1
from orchestrator.app.agents import BaseAgent, AgentTemplate
print("✅ Phase 1 complète")
```

### **Phase 2 : Agent Factory (OBLIGATOIRE)**

**Durée estimée** : 3-4 heures

**Étapes** :
1. **Implémenter AgentFactory** (code obligatoire fourni)
2. **Configurer AgentFactoryConfig** (code obligatoire fourni) 
3. **Créer les fichiers __init__.py** (obligatoires)

**Test Phase 2** :
```python
# Fichier: test_phase2.py
import asyncio
from orchestrator.app.agents import agent_factory

async def test_factory():
    # Test création d'agent
    agent = await agent_factory.create_agent("documentaliste")
    print(f"✅ Agent créé: {agent.metadata.name}")
    
    # Test statistiques
    stats = agent_factory.get_factory_stats()
    print(f"✅ Stats: {stats}")

asyncio.run(test_factory())
```

### **Phase 3 : Intégration Supervisor (OBLIGATOIRE)**

**Durée estimée** : 2-3 heures

**Code d'intégration obligatoire** :

```python
# Fichier: orchestrator/app/supervisor/factory_integration.py
"""
Intégration du Agent Factory avec le Supervisor existant
OBLIGATOIRE : Ce code doit être utilisé tel quel
"""

from typing import Dict, Any, List
from ..agents import agent_factory, BaseAgent
from ..core.supervisor import SupervisorNode  # Adapter selon votre structure

class FactoryIntegratedSupervisor(SupervisorNode):
    """
    Supervisor étendu avec le Factory Pattern
    OBLIGATOIRE : Extension du supervisor existant
    """
    
    def __init__(self):
        super().__init__()
        self.factory = agent_factory
        
    async def dynamic_agent_creation(self, request: Dict[str, Any]) -> BaseAgent:
        """Création dynamique d'agents via Factory"""
        
        template_name = request.get("template")
        config = request.get("config", {})
        
        if not template_name:
            raise ValueError("Template name required")
            
        agent = await self.factory.create_agent(template_name, config)
        if not agent:
            raise RuntimeError(f"Failed to create agent from template: {template_name}")
            
        return agent
        
    async def route_with_factory(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Routage avec possibilité de créer des agents à la demande"""
        
        # Logique existante du supervisor
        routing_decision = await self.determine_routing(query, context)
        
        # Si aucun agent existant ne peut traiter, créer dynamiquement
        if routing_decision.get("create_agent"):
            template = routing_decision.get("suggested_template")
            new_agent = await self.dynamic_agent_creation({
                "template": template,
                "config": routing_decision.get("config", {})
            })
            
            # Traiter avec le nouvel agent
            return await new_agent.process(query, context)
        
        # Sinon utiliser le routage existant
        return await super().route(query, context)

# Instance globale intégrée
factory_supervisor = FactoryIntegratedSupervisor()
```

### **Phase 4 : Tests et Validation (OBLIGATOIRE)**

**Test complet obligatoire** :

```python
# Fichier: test_agent_factory_complete.py
"""
Tests complets du Agent Factory Pattern
OBLIGATOIRE : Ces tests doivent tous passer
"""

import asyncio
import pytest
from orchestrator.app.agents import agent_factory, BaseAgent
from orchestrator.app.supervisor.factory_integration import factory_supervisor

class TestAgentFactory:
    """Tests obligatoires pour le Factory Pattern"""
    
    async def test_agent_creation(self):
        """Test création d'agents"""
        # Test documentaliste
        doc_agent = await agent_factory.create_agent("documentaliste")
        assert doc_agent is not None
        assert doc_agent.metadata.name == "documentaliste"
        assert doc_agent.metadata.role == "analyzer"
        
        # Test genie_logiciel
        eng_agent = await agent_factory.create_agent("genie_logiciel")
        assert eng_agent is not None
        assert eng_agent.metadata.name == "genie_logiciel"
        assert eng_agent.metadata.role == "engineer"
        
        print("✅ Test création d'agents : PASSED")
    
    async def test_agent_processing(self):
        """Test traitement par les agents"""
        agent = await agent_factory.create_agent("documentaliste")
        
        test_input = "Analyser ce document de spécifications"
        result = await agent.process(test_input)
        
        assert "analysis" in result
        assert result["agent"] == "documentaliste"
        assert result["role"] == "analyzer"
        
        print("✅ Test traitement d'agents : PASSED")
    
    async def test_bulk_creation(self):
        """Test création en lot"""
        specs = [
            {"template": "documentaliste", "suffix": "_batch1"},
            {"template": "genie_logiciel", "suffix": "_batch1"},
            {"template": "hardware", "suffix": "_batch1"}
        ]
        
        agents = await agent_factory.bulk_create_agents(specs)
        assert len(agents) == 3
        assert "documentaliste_batch1" in agents
        
        print("✅ Test création en lot : PASSED")
    
    async def test_supervisor_integration(self):
        """Test intégration avec supervisor"""
        # Test routage avec création dynamique
        result = await factory_supervisor.route_with_factory(
            "Analyser ce code Python", 
            {"create_agent": True, "suggested_template": "genie_logiciel"}
        )
        
        assert "solution" in result or "processing_result" in result
        
        print("✅ Test intégration supervisor : PASSED")

async def run_all_tests():
    """Exécution de tous les tests obligatoires"""
    test_suite = TestAgentFactory()
    
    print("🧪 Démarrage des tests obligatoires...")
    
    await test_suite.test_agent_creation()
    await test_suite.test_agent_processing()
    await test_suite.test_bulk_creation()
    await test_suite.test_supervisor_integration()
    
    print("🎉 TOUS LES TESTS OBLIGATOIRES ONT RÉUSSI !")

if __name__ == "__main__":
    asyncio.run(run_all_tests())
```

### **Phase 5 : Déploiement (OBLIGATOIRE)**

**Script de déploiement** :

```python
# Fichier: deploy_agent_factory.py
"""
Script de déploiement pour le Agent Factory Pattern
OBLIGATOIRE : Exécuter après l'implémentation
"""

import os
import shutil
import subprocess
from pathlib import Path

def deploy_agent_factory():
    """Déploiement complet du système"""
    
    print("🚀 Déploiement du Agent Factory Pattern...")
    
    # 1. Vérifier la structure
    required_files = [
        "orchestrator/app/agents/base_agent.py",
        "orchestrator/app/agents/agent_factory.py", 
        "orchestrator/app/agents/agent_templates.py",
        "orchestrator/app/config/agent_config.py"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            raise FileNotFoundError(f"Fichier obligatoire manquant: {file}")
    
    print("✅ Structure de fichiers validée")
    
    # 2. Installer les dépendances si nécessaire
    try:
        subprocess.run(["pip", "install", "pydantic", "typing-extensions"], check=True)
        print("✅ Dépendances installées")
    except subprocess.CalledProcessError:
        print("⚠️ Erreur installation dépendances - vérifier manuellement")
    
    # 3. Créer les répertoires de logs
    os.makedirs("logs/agents", exist_ok=True)
    print("✅ Répertoires de logs créés")
    
    # 4. Test de déploiement
    try:
        from orchestrator.app.agents import agent_factory
        stats = agent_factory.get_factory_stats()
        print(f"✅ Factory opérationnel: {stats}")
    except ImportError as e:
        raise RuntimeError(f"Erreur d'import: {e}")
    
    print("🎉 DÉPLOIEMENT TERMINÉ AVEC SUCCÈS !")

if __name__ == "__main__":
    deploy_agent_factory()
```

---

## 📊 **MÉTRIQUES DE SUCCÈS OBLIGATOIRES**

L'implémentation sera considérée comme **RÉUSSIE** uniquement si :

✅ **Tous les tests de la Phase 4 passent**  
✅ **Le script de déploiement s'exécute sans erreur**  
✅ **Factory peut créer tous les types d'agents (documentaliste, genie_logiciel, hardware)**  
✅ **Intégration avec le supervisor existant fonctionne**  
✅ **Aucune régression sur le code existant**  

---

## ⚠️ **RAPPEL CRITIQUE**

Ce prompt contient du code **OBLIGATOIRE** qui doit être implémenté **EXACTEMENT** tel que spécifié. Toute modification pourrait compromettre l'intégration avec l'architecture NextGeneration.

**EN CAS DE PROBLÈME** : Reprendre depuis la Phase 1 et suivre exactement les instructions.

---

## 🎯 **OBJECTIF FINAL**

À la fin de cette implémentation, vous aurez :
- ✅ Un système de génération automatique d'agents
- ✅ Une intégration transparente avec l'architecture existante  
- ✅ La capacité de créer de nouveaux agents à la demande
- ✅ Un système extensible et maintenable

**BONNE IMPLÉMENTATION !** 🚀
'''
    
    return phases

def append_to_prompt_file(content):
    """Ajoute du contenu au fichier prompt existant"""
    prompt_file = "prompt/IMPLEMENTATION_AGENT_FACTORY_PATTERN.md"
    
    with open(prompt_file, 'a', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Contenu ajouté au prompt : {len(content)} caractères")

def main():
    """Complète le prompt avec les phases finales"""
    print("🔧 Complétion du prompt Agent Factory Pattern...")
    
    phases_content = generate_implementation_phases()
    append_to_prompt_file(phases_content)
    
    print("🎉 Prompt complet généré !")
    print("📄 Fichier final : prompt/IMPLEMENTATION_AGENT_FACTORY_PATTERN.md")

if __name__ == "__main__":
    main() 