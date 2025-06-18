# 🚀 PROMPT D'IMPLÉMENTATION : AGENT FACTORY PATTERN POUR NEXTGENERATION

## ⚠️ **OBLIGATION ABSOLUE D'UTILISATION DE CE CODE**

**ATTENTION** : Ce prompt contient du code **OBLIGATOIRE** et **EXHAUSTIF** qui DOIT être implémenté exactement tel que spécifié. Toute modification ou omission pourrait compromettre l'intégration avec l'architecture NextGeneration existante.

**CONTRAINTES IMPÉRATIVES** :
- ✅ **UTILISER EXACTEMENT** le code fourni sans modification
- ✅ **RESPECTER STRICTEMENT** l'ordre d'implémentation des phases
- ✅ **INTÉGRER OBLIGATOIREMENT** avec l'architecture FastAPI + LangGraph existante
- ✅ **TESTER CHAQUE PHASE** avant de passer à la suivante
- ✅ **DOCUMENTER TOUTES** les modifications apportées

---

## 📋 **CONTEXTE ET OBJECTIFS**

### **Situation Actuelle**
Le projet NextGeneration dispose d'une architecture multi-agents mature basée sur :
- **FastAPI + LangGraph** (orchestrator/app/main.py - 1990+ lignes)
- **3 agents existants** : documentaliste, génie logiciel, hardware
- **Supervisor pattern** avec routing intelligent
- **Infrastructure production-ready**

### **Objectif**
Implémenter un **Agent Factory Pattern** pour :
- **Réduire de 80%** le temps de création d'agents (2-3h → 3-5min)
- **Automatiser** la génération d'agents spécialisés
- **Standardiser** l'architecture multi-agents
- **Améliorer** la maintenabilité et réutilisabilité

---

## 🎯 **PLAN D'IMPLÉMENTATION RECOMMANDÉ**

### **📅 PHASE 1 : AGENT FACTORY CORE (4-6h)**
- Création du `NextGenAgentFactory`
- Templates pour les 3 agents existants
- Intégration avec supervisor.py

### **📅 PHASE 2 : TEMPLATES SYSTEM (2-3h)**
- Bibliothèque de templates extensible
- Configuration-driven generation
- Tests d'intégration

### **📅 PHASE 3 : OPTIMIZATION (1-2h)**
- Caching des templates
- Validation automatique
- Documentation complète

**ROI ESTIMÉ** : +300% productivité, -80% temps développement

---

## 🏗️ **PHASE 1 : AGENT FACTORY CORE**

### **1.1 Structure des Fichiers à Créer**

```
nextgeneration/orchestrator/app/
├── agents/
│   ├── __init__.py
│   ├── agent_factory.py          # ← NOUVEAU
│   ├── agent_templates.py        # ← NOUVEAU
│   ├── base_agent.py            # ← NOUVEAU
│   └── templates/               # ← NOUVEAU DOSSIER
│       ├── __init__.py
│       ├── documentaliste.json
│       ├── genie_logiciel.json
│       └── hardware.json
├── config/
│   └── agent_config.py          # ← NOUVEAU
└── tests/
    └── test_agent_factory.py    # ← NOUVEAU
```

### **1.2 CODE OBLIGATOIRE : BaseAgent**

**Fichier** : `nextgeneration/orchestrator/app/agents/base_agent.py`

```python
"""
Base Agent Class pour NextGeneration
OBLIGATOIRE : Ce code doit être utilisé exactement tel que spécifié
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class AgentStatus(Enum):
    """États possibles d'un agent"""
    IDLE = "idle"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"
    DISABLED = "disabled"

@dataclass
class AgentMetadata:
    """Métadonnées d'un agent"""
    id: str
    name: str
    role: str
    domain: str
    version: str
    created_at: datetime
    last_updated: datetime
    capabilities: List[str]
    tools: List[str]
    dependencies: List[str]

class BaseAgent(ABC):
    """
    Classe de base pour tous les agents NextGeneration
    OBLIGATOIRE : Tous les nouveaux agents DOIVENT hériter de cette classe
    """
    
    def __init__(
        self,
        name: str,
        role: str,
        domain: str = "general",
        tools: List[str] = None,
        capabilities: List[str] = None,
        config: Dict[str, Any] = None
    ):
        self.metadata = AgentMetadata(
            id=str(uuid.uuid4()),
            name=name,
            role=role,
            domain=domain,
            version="1.0.0",
            created_at=datetime.now(),
            last_updated=datetime.now(),
            capabilities=capabilities or [],
            tools=tools or [],
            dependencies=[]
        )
        
        self.status = AgentStatus.IDLE
        self.config = config or {}
        self.context = {}
        self.performance_metrics = {
            "tasks_completed": 0,
            "success_rate": 0.0,
            "avg_processing_time": 0.0,
            "last_execution_time": None
        }
        
        logger.info(f"Initialized agent: {self.metadata.name} ({self.metadata.role})")
    
    @abstractmethod
    async def process(self, input_data: Any, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Traite une requête
        OBLIGATOIRE : Chaque agent DOIT implémenter cette méthode
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        Retourne les capacités de l'agent
        OBLIGATOIRE : Chaque agent DOIT implémenter cette méthode
        """
        pass
    
    async def validate_input(self, input_data: Any) -> bool:
        """Valide les données d'entrée"""
        return input_data is not None
    
    async def pre_process(self, input_data: Any, context: Dict[str, Any] = None):
        """Hook de pré-traitement"""
        self.status = AgentStatus.PROCESSING
        self.context.update(context or {})
        logger.debug(f"Pre-processing started for agent {self.metadata.name}")
    
    async def post_process(self, result: Dict[str, Any]):
        """Hook de post-traitement"""
        self.status = AgentStatus.COMPLETED
        self.performance_metrics["tasks_completed"] += 1
        self.metadata.last_updated = datetime.now()
        logger.debug(f"Post-processing completed for agent {self.metadata.name}")
        return result
    
    def get_info(self) -> Dict[str, Any]:
        """Retourne les informations de l'agent"""
        return {
            "metadata": self.metadata.__dict__,
            "status": self.status.value,
            "performance": self.performance_metrics
        }
    
    def update_config(self, new_config: Dict[str, Any]):
        """Met à jour la configuration"""
        self.config.update(new_config)
        self.metadata.last_updated = datetime.now()
    
    def add_tool(self, tool_name: str):
        """Ajoute un outil à l'agent"""
        if tool_name not in self.metadata.tools:
            self.metadata.tools.append(tool_name)
            self.metadata.last_updated = datetime.now()
    
    def add_capability(self, capability: str):
        """Ajoute une capacité à l'agent"""
        if capability not in self.metadata.capabilities:
            self.metadata.capabilities.append(capability)
            self.metadata.last_updated = datetime.now()
```

### **1.3 CODE OBLIGATOIRE : Agent Templates**

**Fichier** : `nextgeneration/orchestrator/app/agents/agent_templates.py`

```python
"""
Templates pour la génération automatique d'agents
OBLIGATOIRE : Ce système de templates est requis pour le fonctionnement du Factory
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)

@dataclass
class AgentTemplate:
    """Template pour la création d'agents"""
    name: str
    role: str
    domain: str
    base_class: str
    capabilities: List[str]
    tools: List[str]
    default_config: Dict[str, Any]
    supervisor_route: str
    description: str
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

class TemplateManager:
    """
    Gestionnaire de templates pour NextGeneration
    OBLIGATOIRE : Utilisé par l'AgentFactory pour charger les templates
    """
    
    def __init__(self, templates_dir: str = None):
        self.templates_dir = Path(templates_dir) if templates_dir else Path(__file__).parent / "templates"
        self.templates_cache: Dict[str, AgentTemplate] = {}
        self._load_builtin_templates()
    
    def _load_builtin_templates(self):
        """Charge les templates intégrés"""
        builtin_templates = {
            "documentaliste": AgentTemplate(
                name="documentaliste",
                role="analyzer",
                domain="documentation",
                base_class="DocumentalisteAgent",
                capabilities=[
                    "document_analysis",
                    "text_extraction", 
                    "summary_generation",
                    "classification",
                    "metadata_extraction"
                ],
                tools=[
                    "file_reader",
                    "text_processor",
                    "classifier",
                    "summarizer"
                ],
                default_config={
                    "max_file_size": 50000000,  # 50MB
                    "supported_formats": [".txt", ".md", ".pdf", ".docx"],
                    "summary_length": "medium",
                    "classification_threshold": 0.7
                },
                supervisor_route="document_analysis",
                description="Agent spécialisé dans l'analyse et le traitement de documents"
            ),
            
            "genie_logiciel": AgentTemplate(
                name="genie_logiciel",
                role="engineer",
                domain="software_engineering",
                base_class="GeniLogicielAgent",
                capabilities=[
                    "code_analysis",
                    "architecture_review",
                    "bug_detection",
                    "performance_optimization",
                    "documentation_generation"
                ],
                tools=[
                    "code_analyzer",
                    "static_analyzer",
                    "performance_profiler",
                    "doc_generator"
                ],
                default_config={
                    "supported_languages": ["python", "javascript", "typescript", "java"],
                    "analysis_depth": "deep",
                    "performance_threshold": 0.8,
                    "documentation_style": "sphinx"
                },
                supervisor_route="software_engineering",
                description="Agent spécialisé en génie logiciel et analyse de code"
            ),
            
            "hardware": AgentTemplate(
                name="hardware",
                role="specialist",
                domain="hardware_analysis",
                base_class="HardwareAgent",
                capabilities=[
                    "system_diagnostics",
                    "performance_monitoring",
                    "hardware_profiling",
                    "compatibility_check",
                    "optimization_recommendations"
                ],
                tools=[
                    "psutil",
                    "gpu_monitor",
                    "disk_analyzer",
                    "network_tester"
                ],
                default_config={
                    "monitoring_interval": 30,
                    "performance_baseline": "auto",
                    "alert_threshold": 0.9,
                    "report_format": "detailed"
                },
                supervisor_route="hardware_analysis",
                description="Agent spécialisé dans l'analyse et le monitoring hardware"
            )
        }
        
        self.templates_cache.update(builtin_templates)
        logger.info(f"Loaded {len(builtin_templates)} builtin templates")
    
    def load_template(self, template_name: str) -> Optional[AgentTemplate]:
        """
        Charge un template par son nom
        OBLIGATOIRE : Utilisé par l'AgentFactory
        """
        # Vérifier le cache d'abord
        if template_name in self.templates_cache:
            return self.templates_cache[template_name]
        
        # Charger depuis le fichier
        template_file = self.templates_dir / f"{template_name}.json"
        if template_file.exists():
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
                
                template = AgentTemplate(**template_data)
                self.templates_cache[template_name] = template
                logger.info(f"Loaded template: {template_name}")
                return template
                
            except Exception as e:
                logger.error(f"Error loading template {template_name}: {e}")
                return None
        
        logger.warning(f"Template not found: {template_name}")
        return None
    
    def save_template(self, template: AgentTemplate) -> bool:
        """Sauvegarde un template"""
        try:
            self.templates_dir.mkdir(parents=True, exist_ok=True)
            template_file = self.templates_dir / f"{template.name}.json"
            
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(template), f, indent=2, ensure_ascii=False)
            
            self.templates_cache[template.name] = template
            logger.info(f"Saved template: {template.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving template {template.name}: {e}")
            return False
    
    def list_templates(self) -> List[str]:
        """Liste tous les templates disponibles"""
        templates = list(self.templates_cache.keys())
        
        # Ajouter les templates depuis les fichiers
        if self.templates_dir.exists():
            for file in self.templates_dir.glob("*.json"):
                template_name = file.stem
                if template_name not in templates:
                    templates.append(template_name)
        
        return sorted(templates)
    
    def create_custom_template(
        self,
        name: str,
        role: str,
        domain: str,
        capabilities: List[str],
        tools: List[str],
        config: Dict[str, Any] = None,
        description: str = ""
    ) -> AgentTemplate:
        """Crée un template personnalisé"""
        template = AgentTemplate(
            name=name,
            role=role,
            domain=domain,
            base_class=f"{name.title()}Agent",
            capabilities=capabilities,
            tools=tools,
            default_config=config or {},
            supervisor_route=f"{role}_{domain}",
            description=description or f"Agent {name} personnalisé"
        )
        
        self.templates_cache[name] = template
        logger.info(f"Created custom template: {name}")
        return template
``` 
### **1.4 CODE OBLIGATOIRE : Agent Factory Principal**

**Fichier** : `nextgeneration/orchestrator/app/agents/agent_factory.py`

```python
"""
NextGeneration Agent Factory - Générateur automatique d'agents
OBLIGATOIRE : Ce factory est le cœur du système de génération d'agents
"""

from typing import Dict, List, Any, Optional, Type
import logging
import importlib
import inspect
from pathlib import Path

from .base_agent import BaseAgent, AgentMetadata
from .agent_templates import TemplateManager, AgentTemplate

logger = logging.getLogger(__name__)

class AgentFactory:
    """
    Factory pour la création automatique d'agents NextGeneration
    OBLIGATOIRE : Utilisé pour générer tous les nouveaux agents
    """
    
    def __init__(self, template_manager: TemplateManager = None):
        self.template_manager = template_manager or TemplateManager()
        self.registered_agents: Dict[str, BaseAgent] = {}
        self.agent_classes: Dict[str, Type[BaseAgent]] = {}
        self._load_existing_agents()
    
    def _load_existing_agents(self):
        """Charge les agents existants du projet NextGeneration"""
        try:
            # Importer les agents existants depuis l'architecture actuelle
            # OBLIGATOIRE : Adapter ces imports selon votre structure exacte
            
            agents_module_path = Path(__file__).parent.parent
            logger.info(f"Loading existing agents from: {agents_module_path}")
            
            # Ici, vous devez adapter selon vos agents existants
            # Exemple pour l'architecture NextGeneration :
            
            # from ..supervisor import agent_documentaliste, agent_genie_logiciel, agent_hardware
            
            # self.registered_agents.update({
            #     "documentaliste": agent_documentaliste,
            #     "genie_logiciel": agent_genie_logiciel,
            #     "hardware": agent_hardware
            # })
            
            logger.info(f"Loaded {len(self.registered_agents)} existing agents")
            
        except Exception as e:
            logger.warning(f"Could not load existing agents: {e}")
    
    async def create_agent(
        self,
        template_name: str,
        custom_config: Dict[str, Any] = None,
        name_suffix: str = ""
    ) -> Optional[BaseAgent]:
        """
        Crée un agent à partir d'un template
        OBLIGATOIRE : Méthode principale de création d'agents
        
        Args:
            template_name: Nom du template à utiliser
            custom_config: Configuration personnalisée
            name_suffix: Suffixe pour le nom de l'agent
            
        Returns:
            BaseAgent: Instance de l'agent créé
        """
        
        template = self.template_manager.load_template(template_name)
        if not template:
            logger.error(f"Template not found: {template_name}")
            return None
        
        try:
            # Générer le nom unique de l'agent
            agent_name = f"{template.name}{name_suffix}" if name_suffix else template.name
            
            # Fusionner la configuration
            final_config = template.default_config.copy()
            if custom_config:
                final_config.update(custom_config)
            
            # Créer l'agent dynamiquement
            agent = await self._instantiate_agent(template, agent_name, final_config)
            
            if agent:
                # Enregistrer l'agent
                self.registered_agents[agent_name] = agent
                logger.info(f"Created agent: {agent_name} from template {template_name}")
                
                return agent
            
        except Exception as e:
            logger.error(f"Error creating agent from template {template_name}: {e}")
            return None
    
    async def _instantiate_agent(
        self,
        template: AgentTemplate,
        agent_name: str,
        config: Dict[str, Any]
    ) -> Optional[BaseAgent]:
        """
        Instancie un agent à partir d'un template
        OBLIGATOIRE : Logique de création dynamique
        """
        
        # Créer la classe d'agent dynamiquement
        class DynamicAgent(BaseAgent):
            """Agent généré dynamiquement par l'AgentFactory"""
            
            def __init__(self, name: str, template: AgentTemplate, config: Dict[str, Any]):
                super().__init__(
                    name=name,
                    role=template.role,
                    domain=template.domain,
                    tools=template.tools.copy(),
                    capabilities=template.capabilities.copy(),
                    config=config
                )
                self.template = template
            
            async def process(self, input_data: Any, context: Dict[str, Any] = None) -> Dict[str, Any]:
                """Traitement générique basé sur le template"""
                await self.pre_process(input_data, context)
                
                # Logique de traitement basée sur le rôle
                result = await self._role_based_processing(input_data, context or {})
                
                return await self.post_process(result)
            
            async def _role_based_processing(self, input_data: Any, context: Dict[str, Any]) -> Dict[str, Any]:
                """Traitement spécialisé selon le rôle"""
                
                if self.template.role == "analyzer":
                    return await self._analyze_data(input_data, context)
                elif self.template.role == "engineer":
                    return await self._engineer_solution(input_data, context)
                elif self.template.role == "specialist":
                    return await self._specialist_analysis(input_data, context)
                else:
                    return await self._generic_processing(input_data, context)
            
            async def _analyze_data(self, input_data: Any, context: Dict[str, Any]) -> Dict[str, Any]:
                """Traitement pour les agents analystes"""
                return {
                    "agent": self.metadata.name,
                    "role": "analyzer",
                    "analysis": f"Analyse effectuée sur les données d'entrée",
                    "capabilities_used": self.metadata.capabilities,
                    "tools_used": self.metadata.tools,
                    "input_summary": str(input_data)[:200] if input_data else "No input",
                    "context": context,
                    "recommendations": []
                }
            
            async def _engineer_solution(self, input_data: Any, context: Dict[str, Any]) -> Dict[str, Any]:
                """Traitement pour les agents ingénieurs"""
                return {
                    "agent": self.metadata.name,
                    "role": "engineer",
                    "solution": f"Solution technique proposée",
                    "capabilities_used": self.metadata.capabilities,
                    "tools_used": self.metadata.tools,
                    "technical_analysis": str(input_data)[:200] if input_data else "No input",
                    "context": context,
                    "implementation_steps": []
                }
            
            async def _specialist_analysis(self, input_data: Any, context: Dict[str, Any]) -> Dict[str, Any]:
                """Traitement pour les agents spécialistes"""
                return {
                    "agent": self.metadata.name,
                    "role": "specialist",
                    "specialist_report": f"Rapport spécialisé en {self.metadata.domain}",
                    "capabilities_used": self.metadata.capabilities,
                    "tools_used": self.metadata.tools,
                    "domain_analysis": str(input_data)[:200] if input_data else "No input",
                    "context": context,
                    "expert_recommendations": []
                }
            
            async def _generic_processing(self, input_data: Any, context: Dict[str, Any]) -> Dict[str, Any]:
                """Traitement générique"""
                return {
                    "agent": self.metadata.name,
                    "role": self.template.role,
                    "processing_result": f"Traitement effectué",
                    "capabilities_used": self.metadata.capabilities,
                    "tools_used": self.metadata.tools,
                    "input_data": str(input_data)[:200] if input_data else "No input",
                    "context": context
                }
            
            def get_capabilities(self) -> List[str]:
                """Retourne les capacités définies dans le template"""
                return self.metadata.capabilities.copy()
        
        # Instancier l'agent
        agent = DynamicAgent(agent_name, template, config)
        return agent
    
    async def bulk_create_agents(
        self,
        agent_specs: List[Dict[str, Any]]
    ) -> Dict[str, BaseAgent]:
        """
        Création en lot d'agents
        OBLIGATOIRE : Pour créer plusieurs agents simultanément
        
        Args:
            agent_specs: Liste des spécifications d'agents
                Format: [{"template": "nom", "config": {}, "suffix": ""}]
        
        Returns:
            Dict[str, BaseAgent]: Dictionnaire des agents créés
        """
        created_agents = {}
        
        for spec in agent_specs:
            template_name = spec.get("template")
            custom_config = spec.get("config", {})
            name_suffix = spec.get("suffix", "")
            
            if not template_name:
                logger.warning("Agent spec missing template name, skipping")
                continue
            
            agent = await self.create_agent(template_name, custom_config, name_suffix)
            if agent:
                created_agents[agent.metadata.name] = agent
        
        logger.info(f"Bulk created {len(created_agents)} agents")
        return created_agents
    
    def get_agent(self, agent_name: str) -> Optional[BaseAgent]:
        """Récupère un agent par son nom"""
        return self.registered_agents.get(agent_name)
    
    def list_agents(self) -> List[str]:
        """Liste tous les agents enregistrés"""
        return list(self.registered_agents.keys())
    
    def list_templates(self) -> List[str]:
        """Liste tous les templates disponibles"""
        return self.template_manager.list_templates()
    
    def remove_agent(self, agent_name: str) -> bool:
        """Supprime un agent"""
        if agent_name in self.registered_agents:
            del self.registered_agents[agent_name]
            logger.info(f"Removed agent: {agent_name}")
            return True
        return False
    
    def get_factory_stats(self) -> Dict[str, Any]:
        """Statistiques du factory"""
        return {
            "total_agents": len(self.registered_agents),
            "available_templates": len(self.template_manager.list_templates()),
            "registered_agents": list(self.registered_agents.keys()),
            "available_templates_list": self.template_manager.list_templates()
        }

# Instance globale du factory (OBLIGATOIRE)
agent_factory = AgentFactory()
```
### **1.5 CODE OBLIGATOIRE : Configuration**

**Fichier** : `nextgeneration/orchestrator/app/config/agent_config.py`

```python
"""
Configuration pour le système Agent Factory
OBLIGATOIRE : Extension de la configuration NextGeneration existante
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseSettings, Field
import os

class AgentFactoryConfig(BaseSettings):
    """
    Configuration pour l'Agent Factory Pattern
    OBLIGATOIRE : À intégrer avec la configuration existante
    """
    
    # Configuration Factory
    AGENT_FACTORY_ENABLED: bool = Field(True, description="Active le système Agent Factory")
    AUTO_AGENT_DISCOVERY: bool = Field(True, description="Découverte automatique des agents")
    
    # Chemins
    AGENT_TEMPLATES_PATH: str = Field("orchestrator/app/agents/templates", description="Répertoire des templates")
    AGENT_LOGS_PATH: str = Field("logs/agents", description="Répertoire des logs d'agents")
    
    # Limites
    MAX_AGENTS_PER_DOMAIN: int = Field(10, description="Nombre maximum d'agents par domaine")
    MAX_CONCURRENT_AGENTS: int = Field(5, description="Nombre maximum d'agents concurrent")
    AGENT_TIMEOUT_SECONDS: int = Field(300, description="Timeout par défaut pour les agents")
    
    # Cache
    ENABLE_TEMPLATE_CACHE: bool = Field(True, description="Cache des templates")
    CACHE_TTL_SECONDS: int = Field(3600, description="Durée de vie du cache")
    
    # Monitoring
    ENABLE_AGENT_METRICS: bool = Field(True, description="Métriques des agents")
    METRICS_COLLECTION_INTERVAL: int = Field(60, description="Intervalle de collecte des métriques")
    
    # Sécurité
    AGENT_SANDBOX_MODE: bool = Field(False, description="Mode sandbox pour les agents")
    ALLOWED_DOMAINS: List[str] = Field(
        ["documentation", "software_engineering", "hardware_analysis", "security", "testing"],
        description="Domaines autorisés pour les agents"
    )
    
    # Intégration avec supervisor existant
    SUPERVISOR_INTEGRATION_ENABLED: bool = Field(True, description="Intégration avec le supervisor")
    AUTO_REGISTER_WITH_SUPERVISOR: bool = Field(True, description="Enregistrement automatique avec supervisor")
    
    # Templates par défaut
    DEFAULT_AGENT_TEMPLATES: Dict[str, Dict[str, Any]] = Field(
        default={
            "documentaliste": {
                "priority": "high",
                "auto_load": True
            },
            "genie_logiciel": {
                "priority": "high", 
                "auto_load": True
            },
            "hardware": {
                "priority": "medium",
                "auto_load": True
            }
        },
        description="Configuration des templates par défaut"
    )
    
    class Config:
        env_prefix = "AGENT_FACTORY_"
        case_sensitive = True

# Instance globale de configuration
agent_factory_config = AgentFactoryConfig()
```
### **1.6 CODE OBLIGATOIRE : Fichiers d'initialisation**

**Fichier** : `nextgeneration/orchestrator/app/agents/__init__.py`

```python
"""
Module agents pour NextGeneration
OBLIGATOIRE : Expose les composants principaux du système Agent Factory
"""

from .base_agent import BaseAgent, AgentStatus, AgentMetadata
from .agent_factory import AgentFactory, agent_factory
from .agent_templates import AgentTemplate, TemplateManager

__all__ = [
    "BaseAgent",
    "AgentStatus", 
    "AgentMetadata",
    "AgentFactory",
    "agent_factory",
    "AgentTemplate",
    "TemplateManager"
]
```

**Fichier** : `nextgeneration/orchestrator/app/agents/templates/__init__.py`

```python
"""
Templates d'agents pour NextGeneration
OBLIGATOIRE : Module pour les templates JSON
"""

# Ce module contient les templates JSON pour la génération d'agents
```
### **1.7 CODE OBLIGATOIRE : Templates JSON**

**Fichier** : `nextgeneration/orchestrator/app/agents/templates/documentaliste.json`

```json
{
    "name": "documentaliste",
    "role": "analyzer",
    "domain": "documentation",
    "base_class": "DocumentalisteAgent",
    "capabilities": [
        "document_analysis",
        "text_extraction",
        "summary_generation",
        "classification",
        "metadata_extraction"
    ],
    "tools": [
        "file_reader",
        "text_processor",
        "classifier",
        "summarizer"
    ],
    "default_config": {
        "max_file_size": 50000000,
        "supported_formats": [".txt", ".md", ".pdf", ".docx"],
        "summary_length": "medium",
        "classification_threshold": 0.7
    },
    "supervisor_route": "document_analysis",
    "description": "Agent spécialisé dans l'analyse et le traitement de documents",
    "dependencies": []
}
```

**Fichier** : `nextgeneration/orchestrator/app/agents/templates/genie_logiciel.json`

```json
{
    "name": "genie_logiciel",
    "role": "engineer",
    "domain": "software_engineering",
    "base_class": "GeniLogicielAgent",
    "capabilities": [
        "code_analysis",
        "architecture_review",
        "bug_detection",
        "performance_optimization",
        "documentation_generation"
    ],
    "tools": [
        "code_analyzer",
        "static_analyzer",
        "performance_profiler",
        "doc_generator"
    ],
    "default_config": {
        "supported_languages": ["python", "javascript", "typescript", "java"],
        "analysis_depth": "deep",
        "performance_threshold": 0.8,
        "documentation_style": "sphinx"
    },
    "supervisor_route": "software_engineering",
    "description": "Agent spécialisé en génie logiciel et analyse de code",
    "dependencies": []
}
```

**Fichier** : `nextgeneration/orchestrator/app/agents/templates/hardware.json`

```json
{
    "name": "hardware",
    "role": "specialist",
    "domain": "hardware_analysis",
    "base_class": "HardwareAgent",
    "capabilities": [
        "system_diagnostics",
        "performance_monitoring",
        "hardware_profiling",
        "compatibility_check",
        "optimization_recommendations"
    ],
    "tools": [
        "psutil",
        "gpu_monitor",
        "disk_analyzer",
        "network_tester"
    ],
    "default_config": {
        "monitoring_interval": 30,
        "performance_baseline": "auto",
        "alert_threshold": 0.9,
        "report_format": "detailed"
    },
    "supervisor_route": "hardware_analysis",
    "description": "Agent spécialisé dans l'analyse et le monitoring hardware",
    "dependencies": []
}
```

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
