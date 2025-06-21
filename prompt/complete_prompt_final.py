"""
Script final pour complter le prompt Agent Factory Pattern
"""

def generate_implementation_phases():
    """Gnre les phases d'implmentation"""
    
    phases = '''

---

##  **PHASES D'IMPLMENTATION OBLIGATOIRES**

### **Phase 1 : Fondations (OBLIGATOIRE)**

**Dure estime** : 2-3 heures

**tapes** :
1. **Crer la structure de dossiers** :
   ```bash
   mkdir -p orchestrator/app/agents/templates
   mkdir -p orchestrator/app/config
   ```

2. **Implmenter BaseAgent** (code obligatoire fourni)
3. **Implmenter AgentTemplate** (code obligatoire fourni)
4. **Crer les templates JSON** (obligatoires)

**Vrification** :
```python
# Test de la phase 1
from orchestrator.app.agents import BaseAgent, AgentTemplate
print("[CHECK] Phase 1 complte")
```

### **Phase 2 : Agent Factory (OBLIGATOIRE)**

**Dure estime** : 3-4 heures

**tapes** :
1. **Implmenter AgentFactory** (code obligatoire fourni)
2. **Configurer AgentFactoryConfig** (code obligatoire fourni) 
3. **Crer les fichiers __init__.py** (obligatoires)

**Test Phase 2** :
```python
# Fichier: test_phase2.py
import asyncio
from orchestrator.app.agents import agent_factory

async def test_factory():
    # Test cration d'agent
    agent = await agent_factory.create_agent("documentaliste")
    print(f"[CHECK] Agent cr: {agent.metadata.name}")
    
    # Test statistiques
    stats = agent_factory.get_factory_stats()
    print(f"[CHECK] Stats: {stats}")

asyncio.run(test_factory())
```

### **Phase 3 : Intgration Supervisor (OBLIGATOIRE)**

**Dure estime** : 2-3 heures

**Code d'intgration obligatoire** :

```python
# Fichier: orchestrator/app/supervisor/factory_integration.py
"""
Intgration du Agent Factory avec le Supervisor existant
OBLIGATOIRE : Ce code doit tre utilis tel quel
"""

from typing import Dict, Any, List
from ..agents import agent_factory, BaseAgent
from ..core.supervisor import SupervisorNode  # Adapter selon votre structure

class FactoryIntegratedSupervisor(SupervisorNode):
    """
    Supervisor tendu avec le Factory Pattern
    OBLIGATOIRE : Extension du supervisor existant
    """
    
    def __init__(self):
        super().__init__()
        self.factory = agent_factory
        
    async def dynamic_agent_creation(self, request: Dict[str, Any]) -> BaseAgent:
        """Cration dynamique d'agents via Factory"""
        
        template_name = request.get("template")
        config = request.get("config", {})
        
        if not template_name:
            raise ValueError("Template name required")
            
        agent = await self.factory.create_agent(template_name, config)
        if not agent:
            raise RuntimeError(f"Failed to create agent from template: {template_name}")
            
        return agent
        
    async def route_with_factory(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Routage avec possibilit de crer des agents  la demande"""
        
        # Logique existante du supervisor
        routing_decision = await self.determine_routing(query, context)
        
        # Si aucun agent existant ne peut traiter, crer dynamiquement
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

# Instance globale intgre
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
        """Test cration d'agents"""
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
        
        print("[CHECK] Test cration d'agents : PASSED")
    
    async def test_agent_processing(self):
        """Test traitement par les agents"""
        agent = await agent_factory.create_agent("documentaliste")
        
        test_input = "Analyser ce document de spcifications"
        result = await agent.process(test_input)
        
        assert "analysis" in result
        assert result["agent"] == "documentaliste"
        assert result["role"] == "analyzer"
        
        print("[CHECK] Test traitement d'agents : PASSED")
    
    async def test_bulk_creation(self):
        """Test cration en lot"""
        specs = [
            {"template": "documentaliste", "suffix": "_batch1"},
            {"template": "genie_logiciel", "suffix": "_batch1"},
            {"template": "hardware", "suffix": "_batch1"}
        ]
        
        agents = await agent_factory.bulk_create_agents(specs)
        assert len(agents) == 3
        assert "documentaliste_batch1" in agents
        
        print("[CHECK] Test cration en lot : PASSED")
    
    async def test_supervisor_integration(self):
        """Test intgration avec supervisor"""
        # Test routage avec cration dynamique
        result = await factory_supervisor.route_with_factory(
            "Analyser ce code Python", 
            {"create_agent": True, "suggested_template": "genie_logiciel"}
        )
        
        assert "solution" in result or "processing_result" in result
        
        print("[CHECK] Test intgration supervisor : PASSED")

async def run_all_tests():
    """Excution de tous les tests obligatoires"""
    test_suite = TestAgentFactory()
    
    print(" Dmarrage des tests obligatoires...")
    
    await test_suite.test_agent_creation()
    await test_suite.test_agent_processing()
    await test_suite.test_bulk_creation()
    await test_suite.test_supervisor_integration()
    
    print(" TOUS LES TESTS OBLIGATOIRES ONT RUSSI !")

if __name__ == "__main__":
    asyncio.run(run_all_tests())
```

### **Phase 5 : Dploiement (OBLIGATOIRE)**

**Script de dploiement** :

```python
# Fichier: deploy_agent_factory.py
"""
Script de dploiement pour le Agent Factory Pattern
OBLIGATOIRE : Excuter aprs l'implmentation
"""

import os
import shutil
import subprocess
from pathlib import Path

def deploy_agent_factory():
    """Dploiement complet du systme"""
    
    print("[ROCKET] Dploiement du Agent Factory Pattern...")
    
    # 1. Vrifier la structure
    required_files = [
        "orchestrator/app/agents/base_agent.py",
        "orchestrator/app/agents/agent_factory.py", 
        "orchestrator/app/agents/agent_templates.py",
        "orchestrator/app/config/agent_config.py"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            raise FileNotFoundError(f"Fichier obligatoire manquant: {file}")
    
    print("[CHECK] Structure de fichiers valide")
    
    # 2. Installer les dpendances si ncessaire
    try:
        subprocess.run(["pip", "install", "pydantic", "typing-extensions"], check=True)
        print("[CHECK] Dpendances installes")
    except subprocess.CalledProcessError:
        print(" Erreur installation dpendances - vrifier manuellement")
    
    # 3. Crer les rpertoires de logs
    os.makedirs("logs/agents", exist_ok=True)
    print("[CHECK] Rpertoires de logs crs")
    
    # 4. Test de dploiement
    try:
        from orchestrator.app.agents import agent_factory
        stats = agent_factory.get_factory_stats()
        print(f"[CHECK] Factory oprationnel: {stats}")
    except ImportError as e:
        raise RuntimeError(f"Erreur d'import: {e}")
    
    print(" DPLOIEMENT TERMIN AVEC SUCCS !")

if __name__ == "__main__":
    deploy_agent_factory()
```

---

## [CHART] **MTRIQUES DE SUCCS OBLIGATOIRES**

L'implmentation sera considre comme **RUSSIE** uniquement si :

[CHECK] **Tous les tests de la Phase 4 passent**  
[CHECK] **Le script de dploiement s'excute sans erreur**  
[CHECK] **Factory peut crer tous les types d'agents (documentaliste, genie_logiciel, hardware)**  
[CHECK] **Intgration avec le supervisor existant fonctionne**  
[CHECK] **Aucune rgression sur le code existant**  

---

##  **RAPPEL CRITIQUE**

Ce prompt contient du code **OBLIGATOIRE** qui doit tre implment **EXACTEMENT** tel que spcifi. Toute modification pourrait compromettre l'intgration avec l'architecture NextGeneration.

**EN CAS DE PROBLME** : Reprendre depuis la Phase 1 et suivre exactement les instructions.

---

## [TARGET] **OBJECTIF FINAL**

 la fin de cette implmentation, vous aurez :
- [CHECK] Un systme de gnration automatique d'agents
- [CHECK] Une intgration transparente avec l'architecture existante  
- [CHECK] La capacit de crer de nouveaux agents  la demande
- [CHECK] Un systme extensible et maintenable

**BONNE IMPLMENTATION !** [ROCKET]
'''
    
    return phases

def append_to_prompt_file(content):
    """Ajoute du contenu au fichier prompt existant"""
    prompt_file = "prompt/IMPLEMENTATION_AGENT_FACTORY_PATTERN.md"
    
    with open(prompt_file, 'a', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[CHECK] Contenu ajout au prompt : {len(content)} caractres")

def main():
    """Complte le prompt avec les phases finales"""
    print("[TOOL] Compltion du prompt Agent Factory Pattern...")
    
    phases_content = generate_implementation_phases()
    append_to_prompt_file(phases_content)
    
    print(" Prompt complet gnr !")
    print("[DOCUMENT] Fichier final : prompt/IMPLEMENTATION_AGENT_FACTORY_PATTERN.md")

if __name__ == "__main__":
    main() 



